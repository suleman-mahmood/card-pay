import firebase_admin

from flask import Blueprint, request, jsonify

from core.api.utils import (
    authenticate_token,
    authenticate_user_type,
    handle_exceptions_uow,
    handle_missing_payload,
    validate_json_payload,
)
from core.payment.entrypoint import commands as payment_commands
from core.payment.domain.model import (
    TransactionMode,
    TransactionType,
)
from core.authentication.entrypoint import queries as authentication_queries
from core.authentication.domain.model import UserType
from core.marketing.entrypoint import commands as marketing_commands
from core.authentication.entrypoint import commands as authentication_commands

cardpay_app = Blueprint("cardpay_app", __name__, url_prefix="/api/v1")


@cardpay_app.route("/create-user", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["personal_email", "password", "phone_number", "user_type", "full_name", "location"])
def create_user(uow):
    """Create a new user account"""
    req = request.get_json(force=True)

    authentication_commands.create_user(
        personal_email=req["personal_email"],
        password=req["password"],
        phone_number=req["phone_number"],
        user_type=req["user_type"],
        full_name=req["full_name"],
        location=req["location"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "User created successfully",
            }
        ),
        201,
    )


@cardpay_app.route("/create-customer", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["personal_email", "password", "phone_number", "full_name", "location"])
def create_customer(uow):
    """
    Create a new user account of type customer

    phone_number = '03333462677'
    """
    req = request.get_json(force=True)

    event_code, user_id = authentication_commands.create_user(
        personal_email=req["personal_email"],
        password=req["password"],
        phone_number=req["phone_number"],
        user_type="CUSTOMER",
        full_name=req["full_name"],
        location=req["location"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "User created successfully",
                "event_code": event_code.name,
                "user_id": user_id,
            }
        ),
        201,
    )


@cardpay_app.route("/change-name", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["user_id", "new_name"])
def change_name(uow):
    req = request.get_json(force=True)

    authentication_commands.change_name(
        user_id=req["user_id"],
        new_name=req["new_name"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "Name changed successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/change-pin", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["user_id", "new_pin"])
def change_pin(uow):
    req = request.get_json(force=True)

    authentication_commands.change_pin(
        user_id=req["user_id"],
        new_pin=req["new_pin"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "Pin changed successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/user-toggle-active", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["user_id"])
def user_toggle_active(uow):
    req = request.get_json(force=True)

    authentication_commands.user_toggle_active(
        user_id=req["user_id"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "User toggled active successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/verify-otp", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["user_id", "otp"])
def verify_otp(uow):
    req = request.get_json(force=True)

    authentication_commands.verify_otp(
        user_id=req["user_id"],
        otp=req["otp"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "OTP verified successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/verify-phone-number", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["user_id", "otp"])
def verify_phone_number(uow):
    req = request.get_json(force=True)

    authentication_commands.verify_phone_number(
        user_id=req["user_id"],
        otp=req["otp"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "Phone number verified successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/register-closed-loop", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["user_id", "closed_loop_id", "unique_identifier"])
def register_closed_loop(uow):
    req = request.get_json(force=True)

    authentication_commands.register_closed_loop(
        user_id=req["user_id"],
        closed_loop_id=req["closed_loop_id"],
        unique_identifier=req["unique_identifier"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "User registered into loop successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/verify-closed-loop", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["user_id", "closed_loop_id", "unique_identifier_otp"])
def verify_closed_loop(uow):
    req = request.get_json(force=True)

    authentication_commands.verify_closed_loop(
        user_id=req["user_id"],
        closed_loop_id=req["closed_loop_id"],
        unique_identifier_otp=req["unique_identifier_otp"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "Closed loop verified successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/create-deposit-request", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["amount"])
def create_deposit_request(uid, uow):
    req = request.get_json(force=True)

    checkout_url = payment_commands.create_deposit_request(
        user_id=uid,
        amount=req["amount"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "deposit request created successfully",
                "checkout_url": checkout_url,
            }
        ),
        201,
    )


@cardpay_app.route("/execute-p2p-push-transaction", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["recipient_unique_identifier", "amount", "closed_loop_id"])
def execute_p2p_push_transaction(uid, uow):
    req = request.get_json(force=True)

    unique_identifier = authentication_queries.get_unique_identifier_from_user_id(
        user_id=uid, uow=uow
    )
    payment_commands.execute_transaction_unique_identifier(
        sender_unique_identifier=unique_identifier,
        recipient_unique_identifier=req["recipient_unique_identifier"],
        amount=req["amount"],
        closed_loop_id=req["closed_loop_id"],
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "p2p push transaction executed successfully",
            }
        ),
        201,
    )


@cardpay_app.route("/create-p2p-pull-transaction", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["sender_unique_identifier", "amount", "closed_loop_id"])
def create_p2p_pull_transaction(uid, uow):
    req = request.get_json(force=True)

    unique_identifier = authentication_queries.get_unique_identifier_from_user_id(
        user_id=uid, uow=uow
    )
    payment_commands.execute_transaction_unique_identifier(
        sender_unique_identifier=req["sender_unique_identifier"],
        recipient_unique_identifier=unique_identifier,
        amount=req["amount"],
        closed_loop_id=req["closed_loop_id"],
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "p2p pull transaction created successfully",
            }
        ),
        201,
    )


@cardpay_app.route("/accept-p2p-pull-transaction", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["transaction_id"])
def accept_p2p_pull_transaction(uow):
    req = request.get_json(force=True)

    payment_commands.accept_p2p_pull_transaction(
        transaction_id=req["transaction_id"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "p2p pull transaction accepted successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/decline-p2p-pull-transaction", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["transaction_id"])
def decline_p2p_pull_transaction(uow):
    req = request.get_json(force=True)

    payment_commands.decline_p2p_pull_transaction(
        transaction_id=req["transaction_id"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "p2p pull transaction declined successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/generate-voucher", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["sender_wallet_id", "amount"])
def generate_voucher(uow):
    req = request.get_json(force=True)

    payment_commands.generate_voucher(
        sender_wallet_id=req["sender_wallet_id"],
        amount=req["amount"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "voucher generated successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/redeem-voucher", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["recipient_wallet_id", "transaction_id"])
def redeem_voucher(uow):
    req = request.get_json(force=True)

    payment_commands.redeem_voucher(
        recipient_wallet_id=req["recipient_wallet_id"],
        transaction_id=req["transaction_id"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "voucher redeemed successfully",
            }
        ),
        200,
    )


@cardpay_app.route("/use-reference", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["referee_id", "referral_id"])
def use_reference(uow):
    req = request.get_json(force=True)

    marketing_commands.use_reference(
        referee_id=req["referee_id"],
        referral_id=req["referral_id"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "reference used successfully",
            }
        ),
        200,
    )
