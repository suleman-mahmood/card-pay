import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from uuid import uuid4

import requests
from core.api import schemas as sch
from core.api import utils
from core.api.event_codes import EventCode
from core.authentication.adapters import exceptions as auth_repo_ex
from core.authentication.domain import exceptions as auth_mdl_ex
from core.authentication.domain.model import PK_CODE, UserType
from core.authentication.entrypoint import anti_corruption as auth_acl
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import exceptions as auth_svc_ex
from core.authentication.entrypoint import queries as auth_qry
from core.comms.entrypoint import anti_corruption as comms_acl
from core.comms.entrypoint import commands as comms_cmd
from core.comms.entrypoint import exceptions as comms_svc_ex
from core.entrypoint import queries as app_queries
from core.entrypoint.uow import AbstractUnitOfWork, UnitOfWork
from core.event.domain import exceptions as event_mdl_exc
from core.event.domain import model as event_mdl
from core.event.entrypoint import commands as event_cmd
from core.event.entrypoint import queries as event_qry
from core.event.entrypoint import services as event_svc
from core.marketing.adapters import exceptions as mktg_repo_ex
from core.marketing.domain import exceptions as mktg_mdl_ex
from core.marketing.entrypoint import commands as mktg_cmd
from core.payment.domain import exceptions as pmt_mdl_ex
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import paypro_service as pp_svc
from core.payment.entrypoint import queries as pmt_qry
from core.payment.entrypoint import view_models as pmt_vm
from firebase_admin import exceptions as fb_ex
from flask import Blueprint, request

cardpay_app = Blueprint("cardpay_app", __name__, url_prefix="/api/v1")


# TODO: Check and deprecate this
@cardpay_app.route("/create-user", methods=["POST"])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "personal_email": sch.EmailSchema,
        "password": sch.PasswordSchema,
        "phone_number": sch.PhoneNumberSchema,
        "user_type": sch.UserTypeSchema,
        "full_name": sch.UserNameSchema,
        "location": sch.LocationSchema,
    }
)
def create_user():
    """Create a new user account"""
    req = request.get_json(force=True)
    uow = UnitOfWork()
    try:
        _, user_id, should_create_wallet = auth_cmd.create_user(
            personal_email=req["personal_email"],
            password=req["password"],
            raw_phone_number=req["phone_number"],
            user_type=req["user_type"],
            full_name=req["full_name"],
            location=req["location"],
            uow=uow,
            fb_svc=auth_acl.FirebaseService(),
        )
        # if should_create_wallet:
        #     pmt_cmd.create_wallet(user_id=user_id, uow=uow)

        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="User created successfully",
        status_code=201,
    ).__dict__


def register_paypro_customer(
    consumer_id: str, full_name: str, personal_email: str, phone_number: str
):
    try:
        pp_svc.register_customer_paypro(
            consumer_id=consumer_id,
            full_name=full_name,
            personal_email=personal_email,
            phone_number=phone_number,
        )

    except pmt_svc_ex.ConsumerAlreadyExists as e:
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "/register-paypro-customer",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "consumer_id": consumer_id,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        logging.info(
            {
                "message": "Unhandled exception raised",
                "endpoint": "/register-paypro-custome",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "consumer_id": consumer_id,
            },
        )
        raise e


@cardpay_app.route("/create-customer", methods=["POST"])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "personal_email": sch.EmailSchema,
        "password": sch.PasswordSchema,
        "phone_number": sch.PhoneNumberSchema,
        "full_name": sch.UserNameSchema,
        "location": sch.LocationSchema,
    }
)
def create_customer():
    """
    Create a new user account of type customer

    phone_number = '3333462677'
    """
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        event_code, user_id, _ = auth_cmd.create_user(
            personal_email=req["personal_email"],
            password=req["password"],
            raw_phone_number=req["phone_number"],
            user_type="CUSTOMER",
            full_name=req["full_name"],
            location=req["location"],
            uow=uow,
            fb_svc=auth_acl.FirebaseService(),
        )
        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Unhandled exception raised",
                "endpoint": "create-customer",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(
        register_paypro_customer,
        "92" + req["phone_number"],
        req["full_name"],
        req["personal_email"],
        "+92" + req["phone_number"],
    )

    return utils.Response(
        message="User created successfully",
        status_code=201,
        event_code=event_code.name,
        data={
            "user_id": user_id,
        },
    ).__dict__


# TODO: check and deprecate this
@cardpay_app.route("/change-name", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(required_parameters={"new_name": sch.UserNameSchema})
def change_name(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()
    try:
        auth_cmd.change_name(
            user_id=uid,
            new_name=req["new_name"],
            uow=uow,
        )
        uow.commit_close_connection()

    except auth_mdl_ex.InvalidNameException as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="Name changed successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/change-pin", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(required_parameters={"new_pin": sch.PinSchema})
def change_pin(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        auth_cmd.change_pin(
            user_id=uid,
            new_pin=req["new_pin"],
            uow=uow,
        )
        uow.commit_close_connection()

    except auth_mdl_ex.InvalidPinException as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "change-pin",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "change-pin",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="Pin changed successfully",
        status_code=200,
    ).__dict__


# TODO: Check and deprecate this
@cardpay_app.route("/user-toggle-active", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(required_parameters={"user_id": sch.UuidSchema})
def user_toggle_active(uid):
    uow = UnitOfWork()

    try:
        auth_cmd.user_toggle_active(
            user_id=uid,
            uow=uow,
        )
        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="User toggled active successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/verify-phone-number", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(required_parameters={"otp": sch.OtpSchema})
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

    except (
        auth_mdl_ex.VerificationException,
        auth_mdl_ex.InvalidOtpException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "verify-phone-number",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "verify-phone-number",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="Phone number verified successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/register-closed-loop", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "closed_loop_id": sch.UuidSchema,
        # TODO: change this when closed loops other than LUMS are added
        "unique_identifier": sch.LUMSRollNumberOrFacultySchema,
    }
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
            auth_svc=auth_acl.AuthenticationService(),
        )
        uow.commit_close_connection()

    except auth_svc_ex.UniqueIdentifierAlreadyExistsException as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "register-closed-loop",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "register-closed-loop",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="User registered into loop successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/verify-closed-loop", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "closed_loop_id": sch.UuidSchema,
        "unique_identifier_otp": sch.OtpSchema,
    },
    optional_parameters={
        # TODO: change this when closed loops other than LUMS are added
        "referral_unique_identifier": sch.LUMSReferralRollNumberSchema,
    },
)
def verify_closed_loop(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    referral_unique_identifier = ""
    try:
        referral_unique_identifier = req["referral_unique_identifier"]
        referral_unique_identifier = (
            referral_unique_identifier if referral_unique_identifier is not None else ""
        )
    except KeyError:
        pass

    try:
        should_migrate_balance, balance = auth_cmd.verify_closed_loop(
            user_id=uid,
            closed_loop_id=req["closed_loop_id"],
            unique_identifier_otp=req["unique_identifier_otp"],
            ignore_migration=False,
            uow=uow,
            auth_svc=auth_acl.AuthenticationService(),
        )
        cardpay_wallet_id = pmt_qry.get_starred_wallet_id(uow=uow)
        if should_migrate_balance:
            try:
                pmt_cmd._execute_transaction(
                    tx_id=str(uuid4()),
                    sender_wallet_id=cardpay_wallet_id,
                    recipient_wallet_id=uid,
                    amount=balance,
                    transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
                    transaction_type=pmt_mdl.TransactionType.CARD_PAY,
                    uow=uow,
                    auth_svc=pmt_acl.AuthenticationService(),
                )
            except pmt_svc_ex.TransactionFailedException:
                pass

        if referral_unique_identifier != "":
            wallet_id = pmt_qry.get_wallet_id_from_unique_identifier_and_closed_loop_id(
                unique_identifier=referral_unique_identifier,
                closed_loop_id=req["closed_loop_id"],
                uow=uow,
            )
            mktg_cmd.use_reference(
                referee_id=uid,
                referral_id=wallet_id,
                uow=uow,
            )
        uow.commit_close_connection()
    except (
        auth_mdl_ex.ClosedLoopException,
        auth_mdl_ex.VerificationException,
        auth_mdl_ex.InvalidOtpException,
        pmt_mdl_ex.TransactionNotAllowedException,
        pmt_svc_ex.UserDoesNotExistException,
        mktg_repo_ex.UserNotExists,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
        mktg_mdl_ex.InvalidReferenceException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "/verify-closed-loop",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except AssertionError:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "/verify-closed-loop",
                "invoked_by": "cardpay_app",
                "exception_type": "AssertionError",
                "exception_message": "User is already verified",
                "json_request": req,
            },
        )
        raise utils.CustomException("User is already verified")

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "/verify-closed-loop",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="Closed loop verified successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/create-deposit-request", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(required_parameters={"amount": sch.AmountSchema})
def create_deposit_request(uid):
    req = request.get_json(force=True)

    uow = UnitOfWork()

    user = uow.users.get(user_id=uid)
    tx_id = str(uuid4())
    amount = req["amount"]

    try:
        pmt_cmd.create_deposit_request(
            tx_id=tx_id,
            user_id=uid,
            amount=amount,
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
            pp_svc=pmt_acl.PayproService(),
        )
        uow.commit_close_connection()

    except (
        pmt_mdl_ex.DepositAmountTooSmallException,
        pmt_svc_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "create-deposit-request",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Unhandled exception raised",
                "endpoint": "create-deposit-request",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    paypro_id = ""
    checkout_url = ""
    try:
        # Slow AF API
        checkout_url, paypro_id = pp_svc.get_deposit_checkout_url_and_paypro_id(
            amount=amount,
            transaction_id=tx_id,
            full_name=user.full_name,
            phone_number=user.phone_number.value,
            email=user.personal_email.value,
            consumer_id=user.phone_number.consumer_id,
        )
    except requests.exceptions.Timeout as e:
        uow = UnitOfWork()
        pmt_cmd.mark_as_ghost(tx_id=tx_id, uow=uow)
        uow.commit_close_connection()

        logging.info(
            {
                "message": "Timeout exception raised",
                "endpoint": "create-deposit-request",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException("PayPro's request timed out, retry again please!")
    except pmt_svc_ex.PaymentUrlNotFoundException as e:
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "create-deposit-request",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    uow = UnitOfWork()
    pmt_cmd.add_paypro_id(tx_id=tx_id, paypro_id=paypro_id, uow=uow)
    uow.commit_close_connection()

    return utils.Response(
        message="Deposit request created successfully",
        status_code=201,
        data={"checkout_url": checkout_url},
    ).__dict__


@cardpay_app.route("/execute-p2p-push-transaction", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "recipient_unique_identifier": sch.LUMSRollNumberSchema,
        "amount": sch.AmountSchema,
        "closed_loop_id": sch.UuidSchema,
    }
)
def execute_p2p_push_transaction(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()
    unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
        user_id=uid,
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
    )

    try:
        pmt_cmd.execute_transaction_unique_identifier(
            tx_id=str(uuid4()),
            sender_unique_identifier=unique_identifier,
            recipient_unique_identifier=req["recipient_unique_identifier"],
            amount=req["amount"],
            closed_loop_id=req["closed_loop_id"],
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
            pmt_svc=pmt_acl.PaymentService(),
        )
        uow.commit_close_connection()

    except pmt_svc_ex.TransactionFailedException as e:
        uow.commit_close_connection()  # save the failed transactions
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "/execute-p2p-push-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except (
        pmt_mdl_ex.TransactionNotAllowedException,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
        pmt_svc_ex.UserDoesNotExistException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "/execute-p2p-push-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except (
        Exception,
        AssertionError,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "/execute-p2p-push-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    # Send notification
    uow = UnitOfWork()
    try:
        recipient_wallet_id = pmt_qry.get_wallet_id_from_unique_identifier_and_closed_loop_id(
            unique_identifier=req["recipient_unique_identifier"],
            closed_loop_id=req["closed_loop_id"],
            uow=uow,
        )
        sender = uow.users.get(user_id=uid)
        comms_cmd.send_notification(
            user_id=recipient_wallet_id,
            title="Recieved transfer",
            body=f"{req['amount']} received from {sender.full_name}",
            uow=uow,
            comms_svc=comms_acl.CommunicationService(),
        )
        uow.close_connection()
    except comms_svc_ex.FcmTokenNotFound as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "/execute-p2p-push-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
                "silent": True,
            },
        )
    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Unhandled exception raised",
                "endpoint": "/execute-p2p-push-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
                "silent": True,
            },
        )

    return utils.Response(
        message="p2p push transaction executed successfully",
        status_code=201,
    ).__dict__


@cardpay_app.route("/create-p2p-pull-transaction", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "sender_unique_identifier": sch.LUMSRollNumberSchema,
        "amount": sch.AmountSchema,
        "closed_loop_id": sch.UuidSchema,
    }
)
def create_p2p_pull_transaction(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()
    unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
        user_id=uid,
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
    )

    try:
        pmt_cmd.execute_transaction_unique_identifier(
            tx_id=str(uuid4()),
            sender_unique_identifier=req["sender_unique_identifier"],
            recipient_unique_identifier=unique_identifier,
            amount=req["amount"],
            closed_loop_id=req["closed_loop_id"],
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
            pmt_svc=pmt_acl.PaymentService(),
        )
        uow.commit_close_connection()
    except (
        pmt_svc_ex.NotVerifiedException,
        pmt_svc_ex.UserDoesNotExistException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except (
        Exception,
        AssertionError,
    ) as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="p2p pull transaction created successfully",
        status_code=201,
    ).__dict__


@cardpay_app.route("/accept-p2p-pull-transaction", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(required_parameters={"transaction_id": sch.UuidSchema})
def accept_p2p_pull_transaction(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        pmt_cmd.accept_p2p_pull_transaction(transaction_id=req["transaction_id"], uow=uow)
        uow.commit_close_connection()

    except pmt_svc_ex.TransactionFailedException as e:
        uow.commit_close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "accept-p2p-pull-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except (
        pmt_mdl_ex.TransactionNotAllowedException,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "accept-p2p-pull-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "accept-p2p-pull-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="p2p pull transaction accepted successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/decline-p2p-pull-transaction", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(required_parameters={"transaction_id": sch.UuidSchema})
def decline_p2p_pull_transaction(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        pmt_cmd.decline_p2p_pull_transaction(
            transaction_id=req["transaction_id"],
            uow=uow,
        )
        uow.commit_close_connection()

    except pmt_mdl_ex.TransactionNotAllowedException as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "decline-p2p-pull-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "decline-p2p-pull-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="p2p pull transaction declined successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/generate-voucher", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "sender_wallet_id": sch.UuidSchema,
        "amount": sch.AmountSchema,
    }
)
def generate_voucher(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        pmt_cmd.generate_voucher(
            tx_id=str(uuid4()),
            sender_wallet_id=req["sender_wallet_id"],
            amount=req["amount"],
            uow=uow,
        )
        uow.commit_close_connection()

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "generate-voucher",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="voucher generated successfully",
        status_code=201,
    ).__dict__


@cardpay_app.route("/redeem-voucher", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "recipient_wallet_id": sch.UuidSchema,
        "transaction_id": sch.UuidSchema,
    }
)
def redeem_voucher(uid):
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
        pmt_mdl_ex.TransactionNotAllowedException,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "redeem-voucher",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "redeem-voucher",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="voucher redeemed successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/execute-qr-transaction", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "qr_id": sch.UuidSchema,
        "amount": sch.AmountSchema,
        "v": sch.VersionSchema,
    }
)
def execute_qr_transaction(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        pmt_cmd.execute_qr_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=uid,
            recipient_qr_id=req["qr_id"],
            amount=req["amount"],
            version=req["v"],
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
            pmt_svc=pmt_acl.PaymentService(),
        )
        uow.commit_close_connection()

    except pmt_svc_ex.TransactionFailedException as e:
        uow.commit_close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "execute-qr-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except (
        pmt_svc_ex.InvalidQRCodeException,
        pmt_svc_ex.InvalidQRVersionException,
        pmt_svc_ex.InvalidUserTypeException,
        pmt_mdl_ex.TransactionNotAllowedException,
        mktg_mdl_ex.InvalidReferenceException,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "execute-qr-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "/execute-qr-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="QR transaction executed successfully",
        status_code=201,
    ).__dict__


@cardpay_app.route("/use-reference", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER, UserType.ADMIN])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "referee_id": sch.UuidSchema,
        "referral_id": sch.UuidSchema,
    }
)
def use_reference(uid):
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
        mktg_mdl_ex.NotVerifiedException,
        mktg_mdl_ex.InvalidReferenceException,
        mktg_mdl_ex.InvalidWeightageException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "use-reference",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "use-reference",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

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


def check_last_deposit_transaction(uid: str):
    uow = UnitOfWork()
    try:
        deposit_tx = pmt_qry.get_last_deposit_transaction(user_id=uid, uow=uow)
        uow.close_connection()

    except pmt_svc_ex.NoUserDepositRequest:
        uow.close_connection()
        return

    logging.info(
        {
            "message": "last deposit transaction was called",
            "endpoint": "/get-user-recent-transactions",
            "deposit_tx": deposit_tx.status.name,
        },
    )

    if deposit_tx.status != pmt_mdl.TransactionStatus.PENDING:
        return

    logging.info(
        {
            "message": "last deposit transaction was pending",
            "endpoint": "/get-user-recent-transactions",
            "invoked_by": "cardpay_app",
        },
    )

    # Slow AF API
    if not pp_svc.invoice_paid(paypro_id=deposit_tx.paypro_id):
        return

    logging.info(
        {
            "message": "last invoice was paid",
            "endpoint": "/get-user-recent-transactions",
            "invoked_by": "cardpay_app",
        },
    )
    user_name = os.environ.get("PAYPRO_USERNAME")
    user_name = user_name if user_name is not None else ""

    password = os.environ.get("PAYPRO_PASSWORD")
    password = password if password is not None else ""

    uow = UnitOfWork()
    success_invoice_ids, not_found_invoice_ids = pp_svc.pay_pro_callback(
        user_name=user_name,
        password=password,
        csv_invoice_ids=deposit_tx.id,
        uow=uow,
    )
    uow.commit_close_connection()

    logging.info(
        {
            "message": "manual callback finished",
            "endpoint": "/get-user-recent-transactions",
            "invoked_by": "cardpay_app",
            "success_invoice_ids": success_invoice_ids,
            "not_found_invoice_ids": not_found_invoice_ids,
        },
    )


@cardpay_app.route("/get-user-recent-transactions", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
def get_user_recent_transactions(uid):
    uow = UnitOfWork()
    txs = pmt_qry.get_all_successful_transactions_of_a_user(
        user_id=uid,
        offset=0,
        page_size=50,
        uow=uow,
    )
    uow.close_connection()

    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(check_last_deposit_transaction, uid)

    return utils.Response(
        message="User recent transactions returned successfully",
        status_code=200,
        data=txs,
    ).__dict__


@cardpay_app.route("/get-user", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
def get_user(uid):
    uow = UnitOfWork()
    user = auth_qry.get_user_from_user_id(user_id=uid, uow=uow)
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


@cardpay_app.route("/get-user-checkpoints", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
def get_user_checkpoint(uid):
    uow = UnitOfWork()

    checkpoints = auth_qry.user_checkpoints(
        user_id=uid,
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="User Checkpoint returned successfully",
        status_code=200,
        data=checkpoints.__dict__,
    ).__dict__


@cardpay_app.route("/get-latest-force-update-version", methods=["GET"])
def get_latest_force_update_version():
    uow = UnitOfWork()
    version = app_queries.get_latest_force_update_version(uow)
    uow.close_connection()

    return utils.Response(
        message="App latest and force update version returned successfully",
        status_code=200,
        data=version,
    ).__dict__


@cardpay_app.route("/get-name-from-unique-identifier-and-closed-loop", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
def get_name_from_unique_identifier_and_closed_loop(uid):
    uow = UnitOfWork()

    try:
        full_name = auth_qry.get_full_name_from_unique_identifier_and_closed_loop(
            unique_identifier=request.args.get("unique_identifier"),
            closed_loop_id=request.args.get("closed_loop_id"),
            uow=uow,
        )
        uow.close_connection()

    except auth_svc_ex.UserNotFoundException as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "get-name-from-unique-identifier-and-closed-loop",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "get-name-from-unique-identifier-and-closed-loop",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
            },
        )
        raise e

    return utils.Response(
        message="User full name returned successfully",
        status_code=200,
        data={"full_name": full_name},
    ).__dict__


""" 
    --- --- --- --- --- --- --- --- --- --- --- ---
    Events
    --- --- --- --- --- --- --- --- --- --- --- ---
"""


@cardpay_app.route("/get-live-events", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
def get_live_events(uid):
    closed_loop_id = request.args.get("closed_loop_id")
    uow = UnitOfWork()

    try:
        events = event_qry.get_live_events(
            closed_loop_id=closed_loop_id,
            uow=uow,
            event_type=event_mdl.EventType.INTERNAL,
        )
        uow.close_connection()

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "get-live-events",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
            },
        )
        raise e

    return utils.Response(
        message="All live events returned successfully", status_code=200, data=events
    ).__dict__


@cardpay_app.route("/get-registered-events", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
def get_registered_events(uid):
    uow = UnitOfWork()

    try:
        events = event_qry.get_registered_events(user_id=uid, uow=uow)
        uow.close_connection()

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "get-registered-events",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
            },
        )
        raise e

    return utils.Response(
        message="All user registered events returned successfully",
        status_code=200,
        data=events,
    ).__dict__


@cardpay_app.route("/register-event", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
@utils.validate_and_sanitize_json_payload(
    required_parameters={"event_id": sch.UuidSchema},
    optional_parameters={"event_form_data": sch.EventFormDataSchema},
)
def register_event(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        user = uow.users.get(user_id=uid)
        event = uow.events.get(event_id=req["event_id"])
        event_form_data = req["event_form_data"] if "event_form_data" in req else {"fields": []}

        paid_registrations_count = event_qry.get_paid_registrations_count(
            event_id=req["event_id"], uow=uow
        )

        event_cmd.register_user_closed_loop(
            event_id=req["event_id"],
            qr_id=str(uuid4()),
            current_time=datetime.now() + timedelta(hours=5),
            event_form_data=event_mdl.Registration.from_json_to_form_data(event_form_data),
            uow=uow,
            user_id=uid,
            users_closed_loop_ids=list(user.closed_loops.keys()),
            paid_registrations_count=int(paid_registrations_count),
        )
        pmt_cmd._execute_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=uid,
            recipient_wallet_id=event.organizer_id,
            amount=event.registration_fee,
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.EVENT_REGISTRATION_FEE,
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
        )
        uow.commit_close_connection()

    except (
        event_mdl_exc.EventNotApproved,
        event_mdl_exc.RegistrationEnded,
        event_mdl_exc.UserInvalidClosedLoop,
        event_mdl_exc.EventCapacityExceeded,
        event_mdl_exc.RegistrationAlreadyExists,
        pmt_svc_ex.TransactionFailedException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "register-event",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "register-event",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="User successfully registered for the event", status_code=200, data={}
    ).__dict__


@cardpay_app.route("/send-otp-to-phone-number", methods=["POST"])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "phone_number": sch.PhoneNumberSchema,
    }
)
def send_otp_to_phone_number():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        user = auth_qry.get_user_from_phone_number(
            phone_number=req["phone_number"],
            uow=uow,
        )

        comms_cmd.send_otp_sms(
            full_name=user.full_name,
            to=req["phone_number"],
            otp_code=user.otp,
        )
        uow.close_connection()
    except (
        auth_svc_ex.UserPhoneNumberNotFound,
        auth_repo_ex.UserNotFoundException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "send-otp-to-phone-number",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))
    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "send-otp-to-phone-number",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message=f"OTP sent successfully to +{PK_CODE + req['phone_number']}",
        status_code=200,
    ).__dict__


@cardpay_app.route("/reset-password", methods=["POST"])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "otp": sch.OtpSchema,
        "phone_number": sch.PhoneNumberSchema,
        "new_password": sch.PasswordSchema,
    }
)
def reset_password():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        user = auth_qry.get_user_from_phone_number(
            phone_number=req["phone_number"],
            uow=uow,
        )
        auth_cmd.verify_otp(
            user_id=user.id,
            otp=req["otp"],
            uow=uow,
        )
        auth_cmd.reset_password(
            raw_phone_number=req["phone_number"],
            new_password=req["new_password"],
            fb_svc=auth_acl.FirebaseService(),
        )
        uow.commit_close_connection()

    except (
        auth_svc_ex.UserPhoneNumberNotFound,
        auth_repo_ex.UserNotFoundException,
        ValueError,
        fb_ex.NotFoundError,
        fb_ex.FirebaseError,
        auth_mdl_ex.InvalidOtpException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "reset-password",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "reset-password",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="Password reset successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/reset-pin", methods=["POST"])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "otp": sch.OtpSchema,
        "phone_number": sch.PhoneNumberSchema,
        "new_pin": sch.PinSchema,
    }
)
def reset_pin():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        user = auth_qry.get_user_from_phone_number(
            phone_number=req["phone_number"],
            uow=uow,
        )
        auth_cmd.verify_otp(
            user_id=user.id,
            otp=req["otp"],
            uow=uow,
        )
        auth_cmd.change_pin(
            user_id=user.id,
            new_pin=req["new_pin"],
            uow=uow,
        )
        uow.commit_close_connection()

    except (
        auth_svc_ex.UserPhoneNumberNotFound,
        auth_repo_ex.UserNotFoundException,
        auth_mdl_ex.InvalidPinException,
        auth_mdl_ex.InvalidOtpException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "reset-pin",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "reset-pin",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="Pin reset successfully",
        status_code=200,
    ).__dict__


@cardpay_app.route("/execute-qr-transaction-v2", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "vendor_qr_id": sch.UuidSchema,
        "waiter_qr_id": sch.UuidSchema,
        "bill_amount": sch.AmountSchema,
        "tip_amount": sch.AmountSchema,
        "v": sch.VersionSchema,
    }
)
def execute_qr_transaction_v2(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        pmt_cmd.execute_qr_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=uid,
            recipient_qr_id=req["vendor_qr_id"],
            amount=req["bill_amount"],
            version=req["v"],
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
            pmt_svc=pmt_acl.PaymentService(),
        )
        uow.commit_close_connection()
    except pmt_svc_ex.TransactionFailedException as e:
        uow.commit_close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "execute-qr-transaction-v2",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except (
        pmt_svc_ex.InvalidQRCodeException,
        pmt_svc_ex.InvalidQRVersionException,
        pmt_svc_ex.InvalidUserTypeException,
        pmt_mdl_ex.TransactionNotAllowedException,
        mktg_mdl_ex.InvalidReferenceException,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "execute-qr-transaction-v2",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Unhandled exception raised",
                "endpoint": "/execute-qr-transaction-v2",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    uow = UnitOfWork()

    try:
        pmt_cmd.execute_qr_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=uid,
            recipient_qr_id=req["waiter_qr_id"],
            amount=req["tip_amount"],
            version=req["v"],
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
            pmt_svc=pmt_acl.PaymentService(),
        )
        uow.commit_close_connection()

    except pmt_svc_ex.TransactionFailedException as e:
        uow.commit_close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "execute-qr-transaction-v2",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        return utils.Response(
            message=f"Vendor QR transaction executed successfully, Waiter transaction failed ({str(e)})",
            status_code=201,
            event_code=EventCode.WAITER_QR_TRANSACTION_FAILED,
        ).__dict__

    except (
        pmt_svc_ex.InvalidQRCodeException,
        pmt_svc_ex.InvalidQRVersionException,
        pmt_svc_ex.InvalidUserTypeException,
        pmt_mdl_ex.TransactionNotAllowedException,
        mktg_mdl_ex.InvalidReferenceException,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "execute-qr-transaction-v2",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        return utils.Response(
            message=f"Vendor QR transaction executed successfully, Waiter transaction failed ({str(e)})",
            status_code=201,
            event_code=EventCode.WAITER_QR_KNOWN_FAILURE,
        ).__dict__

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Unhandled exception raised",
                "endpoint": "/execute-qr-transaction-v2",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        return utils.Response(
            message=f"Vendor QR transaction executed successfully, Waiter transaction failed ({str(e)})",
            status_code=201,
            event_code=EventCode.WAITER_QR_UNKNOWN_FAILURE,
        ).__dict__

    return utils.Response(
        message="Vendor and waiter QR transaction executed successfully",
        status_code=201,
        event_code=EventCode.WAITER_QR_TRANSACTION_SUCCESSFUL,
    ).__dict__


@cardpay_app.route("/set-fcm-token", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.CUSTOMER])
@utils.user_verified
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "fcm_token": sch.FcmTokenSchema,
    }
)
def set_fcm_token(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()
    fcm_token = req["fcm_token"]

    try:
        comms_cmd.set_fcm_token(
            user_id=uid,
            fcm_token=fcm_token,
            uow=uow,
        )
        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "set-fcm-token",
                "invoked_by": "cardpay_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="fcm token set successfully",
        status_code=201,
    ).__dict__
