from flask import Blueprint, request

from core.entrypoint.uow import UnitOfWork

from core.api import utils
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import queries as pmt_qry
from core.payment.domain import exceptions as pmt_ex
from core.payment.entrypoint import exceptions as pmt_cmd_ex
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.domain.model import UserType
from core.marketing.entrypoint import commands as mktg_cmd
from core.marketing.domain import exceptions as mktg_ex
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.domain import exceptions as auth_ex
from core.authentication.entrypoint import exceptions as auth_cmd_ex


cardpay_app = Blueprint("cardpay_app", __name__, url_prefix="/api/v1")


@cardpay_app.route("/create-user", methods=["POST"])
@utils.handle_missing_payload
@utils.validate_json_payload(
    required_parameters=[
        "personal_email",
        "password",
        "phone_number",
        "user_type",
        "full_name",
        "location",
    ]
)
def create_user():
    """Create a new user account"""
    req = request.get_json(force=True)

    uow = UnitOfWork()
    auth_cmd.create_user(
        personal_email=req["personal_email"],
        password=req["password"],
        phone_number=req["phone_number"],
        user_type=req["user_type"],
        full_name=req["full_name"],
        location=req["location"],
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="User created successfully",
        status_code=201,
    ).__dict__


@cardpay_app.route("/create-customer", methods=["POST"])
@utils.handle_missing_payload
@utils.validate_json_payload(
    required_parameters=[
        "personal_email",
        "password",
        "phone_number",
        "full_name",
        "location",
    ]
)
def create_customer():
    """
    Create a new user account of type customer

    phone_number = '03333462677'
    """
    req = request.get_json(force=True)

    uow = UnitOfWork()
    event_code, user_id = auth_cmd.create_user(
        personal_email=req["personal_email"],
        password=req["password"],
        phone_number=req["phone_number"],
        user_type="CUSTOMER",
        full_name=req["full_name"],
        location=req["location"],
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="User created successfully",
        status_code=201,
        event_code=event_code.name,
        data={
            "user_id": user_id,
        },
    ).__dict__


@cardpay_app.route("/change-name", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["new_name"])
def change_name(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    auth_cmd.change_name(
        user_id=uid,
        new_name=req["new_name"],
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="Name changed successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/change-pin", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["new_pin"])
def change_pin(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    auth_cmd.change_pin(
        user_id=uid,
        new_pin=req["new_pin"],
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="Pin changed successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/user-toggle-active", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["user_id"])
def user_toggle_active(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    auth_cmd.user_toggle_active(
        user_id=uid,
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="User toggled active successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/verify-otp", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["user_id", "otp"])
def verify_otp(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        auth_cmd.verify_otp(
            user_id=uid,
            otp=req["otp"],
            uow=uow,
        )
        uow.commit_close_connection()

    except auth_ex.InvalidOtpException as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="OTP verified successfully",
            status_code=200,
        ).__dict__


@cardpay_app.route("/verify-phone-number", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["otp"])
def verify_phone_number(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        auth_cmd.verify_phone_number(
            user_id=uid,
            otp=req["otp"],
            uow=uow,
        )
        uow.commit_close_connection()

    except auth_ex.VerificationException as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="Phone number verified successfully",
            status_code=200,
        ).__dict__


@cardpay_app.route("/register-closed-loop", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(
    required_parameters=["closed_loop_id", "unique_identifier"]
)
def register_closed_loop(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        auth_cmd.register_closed_loop(
            user_id=uid,
            closed_loop_id=req["closed_loop_id"],
            unique_identifier=req["unique_identifier"],
            uow=uow,
        )
        uow.commit_close_connection()

    except auth_cmd_ex.UniqueIdentifierAlreadyExistsException as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    else:
        return utils.Response(
            message="User registered into loop successfully",
            status_code=200,
        ).__dict__


@cardpay_app.route("/verify-closed-loop", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(
    required_parameters=["closed_loop_id", "unique_identifier_otp"]
)
def verify_closed_loop(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        auth_cmd.verify_closed_loop(
            user_id=uid,
            closed_loop_id=req["closed_loop_id"],
            unique_identifier_otp=req["unique_identifier_otp"],
            uow=uow,
        )
        uow.commit_close_connection()

    except (
        auth_ex.ClosedLoopException,
        auth_ex.VerificationException,
        auth_ex.InvalidOtpException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="Closed loop verified successfully",
            status_code=200,
        ).__dict__


@cardpay_app.route("/create-deposit-request", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["amount"])
def create_deposit_request(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        checkout_url = pmt_cmd.create_deposit_request(
            user_id=uid,
            amount=req["amount"],
            uow=uow,
        )
        uow.commit_close_connection()
    except (
        pmt_cmd_ex.DepositAmountTooSmallException,
        pmt_ex.TransactionNotAllowedException,
        mktg_ex.InvalidReferenceException,
        mktg_ex.NegativeAmountException,
        mktg_ex.InvalidTransactionTypeException,
        mktg_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="Deposit request created successfully",
            status_code=201,
            data={
                "checkout_url": checkout_url,
            },
        ).__dict__


@cardpay_app.route("/execute-p2p-push-transaction", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(
    required_parameters=["recipient_unique_identifier", "amount", "closed_loop_id"]
)
def execute_p2p_push_transaction(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    unique_identifier = auth_qry.get_unique_identifier_from_user_id(
        user_id=uid, uow=uow
    )
    try:
        pmt_cmd.execute_transaction_unique_identifier(
            sender_unique_identifier=unique_identifier,
            recipient_unique_identifier=req["recipient_unique_identifier"],
            amount=req["amount"],
            closed_loop_id=req["closed_loop_id"],
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
            uow=uow,
        )
        uow.commit_close_connection()
    except (
        pmt_ex.TransactionNotAllowedException,
        mktg_ex.InvalidReferenceException,
        mktg_ex.NegativeAmountException,
        mktg_ex.InvalidTransactionTypeException,
        mktg_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="p2p push transaction executed successfully",
            status_code=201,
        ).__dict__


@cardpay_app.route("/create-p2p-pull-transaction", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(
    required_parameters=["sender_unique_identifier", "amount", "closed_loop_id"]
)
def create_p2p_pull_transaction(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    unique_identifier = auth_qry.get_unique_identifier_from_user_id(
        user_id=uid, uow=uow
    )
    try:
        pmt_cmd.execute_transaction_unique_identifier(
            sender_unique_identifier=req["sender_unique_identifier"],
            recipient_unique_identifier=unique_identifier,
            amount=req["amount"],
            closed_loop_id=req["closed_loop_id"],
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
            uow=uow,
        )
        uow.commit_close_connection()
    except (
        pmt_ex.TransactionNotAllowedException,
        mktg_ex.InvalidReferenceException,
        mktg_ex.NegativeAmountException,
        mktg_ex.InvalidTransactionTypeException,
        mktg_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="p2p pull transaction created successfully",
            status_code=201,
        ).__dict__


@cardpay_app.route("/accept-p2p-pull-transaction", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["transaction_id"])
def accept_p2p_pull_transaction(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        pmt_cmd.accept_p2p_pull_transaction(
            transaction_id=req["transaction_id"],
            uow=uow,
        )
        uow.commit_close_connection()
    except (
        pmt_ex.TransactionNotAllowedException,
        mktg_ex.InvalidReferenceException,
        mktg_ex.NegativeAmountException,
        mktg_ex.InvalidTransactionTypeException,
        mktg_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="p2p pull transaction accepted successfully",
            status_code=200,
        ).__dict__


@cardpay_app.route("/decline-p2p-pull-transaction", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["transaction_id"])
def decline_p2p_pull_transaction():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        pmt_cmd.decline_p2p_pull_transaction(
            transaction_id=req["transaction_id"],
            uow=uow,
        )
        uow.commit_close_connection()
    except pmt_ex.TransactionNotAllowedException as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="p2p pull transaction declined successfully",
            status_code=200,
        ).__dict__


@cardpay_app.route("/generate-voucher", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["sender_wallet_id", "amount"])
def generate_voucher():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    pmt_cmd.generate_voucher(
        sender_wallet_id=req["sender_wallet_id"],
        amount=req["amount"],
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="voucher generated successfully",
        status_code=201,
    ).__dict__


@cardpay_app.route("/redeem-voucher", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_json_payload(
    required_parameters=["recipient_wallet_id", "transaction_id"]
)
def redeem_voucher():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        pmt_cmd.redeem_voucher(
            recipient_wallet_id=req["recipient_wallet_id"],
            transaction_id=req["transaction_id"],
            uow=uow,
        )
        uow.commit_close_connection()
    except (
        pmt_ex.TransactionNotAllowedException,
        mktg_ex.InvalidReferenceException,
        mktg_ex.NegativeAmountException,
        mktg_ex.InvalidTransactionTypeException,
        mktg_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="voucher redeemed successfully",
            status_code=200,
        ).__dict__


@cardpay_app.route("/use-reference", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["referee_id", "referral_id"])
def use_reference():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        mktg_cmd.use_reference(
            referee_id=req["referee_id"],
            referral_id=req["referral_id"],
            uow=uow,
        )
        uow.commit_close_connection()
    except (
        mktg_ex.InvalidReferenceException,
        mktg_ex.NotVerifiedException,
        mktg_ex.InvalidWeightageException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    else:
        return utils.Response(
            message="reference used successfully",
            status_code=200,
        ).__dict__


@cardpay_app.route("/get-all-closed-loops", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
def get_all_closed_loops(uid):
    """get all closed loops"""

    uow = UnitOfWork()
    closed_loops = auth_qry.get_all_closed_loops(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All closed loops returned successfully",
        status_code=201,
        data=closed_loops,
    ).__dict__


@cardpay_app.route("/get-user-recent-transactions", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
def get_user_recent_transactions(uid):
    uow = UnitOfWork()
    txs = pmt_qry.get_all_transactions_of_a_user(
        user_id=uid,
        offset=0,
        page_size=50,
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="User recent transactions returned successfully",
        status_code=200,
        data=txs,  # txs is a list of dictionaries
    ).__dict__


@cardpay_app.route("/get-user", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
def get_user(uid):
    uow = UnitOfWork()
    user = auth_qry.get_user_from_user_id(
        user_id=uid,
        uow=uow,
    )
    uow.close_connection()

    user.closed_loops = [c for c in user.closed_loops.values()]

    return utils.Response(
        message="User returned successfully",
        status_code=200,
        data=user.__dict__,
    ).__dict__


@cardpay_app.route("/get-user-balance", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
def get_user_balance(uid):
    uow = UnitOfWork()
    balance = auth_qry.get_user_balance(
        user_id=uid,
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="User balance returned successfully",
        status_code=200,
        data={
            "balance": balance,
        },
    ).__dict__
