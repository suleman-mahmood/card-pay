import logging
from datetime import datetime, timedelta
from uuid import uuid4

from core.api import schemas as sch
from core.api import utils
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import anti_corruption as auth_acl
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.comms.entrypoint import anti_corruption as comms_acl
from core.comms.entrypoint import commands as comms_cmd
from core.entrypoint.uow import UnitOfWork
from core.event.domain import exceptions as event_mdl_exc
from core.event.domain import model as event_mdl
from core.event.entrypoint import anti_corruption as event_acl
from core.event.entrypoint import commands as event_cmd
from core.event.entrypoint import exceptions as event_svc_exc
from core.event.entrypoint import queries as event_qry
from core.event.entrypoint import services as event_svc
from core.marketing.domain import exceptions as mktg_mdl_ex
from core.marketing.entrypoint import commands as mktg_cmd
from core.payment.domain import exceptions as pmt_mdl_ex
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import paypro_service as pp_svc
from core.payment.entrypoint import queries as pmt_qry
from flask import Blueprint, request

retool = Blueprint("retool", __name__, url_prefix="/api/v1")


@retool.route("/create-closed-loop", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "name": sch.ClosedLoopOrVendorNameSchema,
        "logo_url": sch.URLSchema,
        "description": sch.DescriptionSchema,
        "verification_type": sch.VerificationTypeSchema,
        "regex": sch.RegexSchema,
    }
)
def create_closed_loop():
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        auth_cmd.create_closed_loop(
            id=str(uuid4()),
            name=req["name"],
            logo_url=req["logo_url"],
            description=req["description"],
            verification_type=req["verification_type"],
            regex=req["regex"],
            uow=uow,
        )
        uow.commit_close_connection()

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="Closed loop created successfully",
        status_code=201,
    ).__dict__


@retool.route("/add-weightage", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "weightage_type": sch.WeightageTypeSchema,
        "weightage_value": sch.WeightageValueSchema,
    }
)
def add_weightage(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        mktg_cmd.add_weightage(
            weightage_type=req["weightage_type"],
            weightage_value=req["weightage_value"],
            uow=uow,
        )
        uow.commit_close_connection()

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="weightage added successfully",
        status_code=201,
    ).__dict__


@retool.route("/set-weightage", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "weightage_type": sch.WeightageTypeSchema,
        "weightage_value": sch.WeightageValueSchema,
    }
)
def set_weightage(uow, uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        mktg_cmd.set_weightage(
            weightage_type=req["weightage_type"],
            weightage_value=req["weightage_value"],
            uow=uow,
        )
        uow.commit_close_connection()
    except mktg_mdl_ex.InvalidWeightageException as e:
        uow.close_connection()
        raise e

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="weightage set successfully",
        status_code=200,
    ).__dict__


@retool.route("/set-cashback-slabs", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_and_sanitize_json_payload(
    required_parameters={"cashback_slabs": sch.AllCashbackSlabsSchema}
)
def set_cashback_slabs(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()
    cashback_slabs = req["cashback_slabs"]

    try:
        mktg_cmd.set_cashback_slabs(
            cashback_slabs=cashback_slabs,
            uow=uow,
        )
        uow.commit_close_connection()

    except mktg_mdl_ex.InvalidSlabException as e:
        uow.close_connection()
        raise e

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="cashback slabs set successfully",
        status_code=200,
    ).__dict__


# retool auth admin routes


@retool.route("/auth-retools-get-all-closed-loops-with-user-counts", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
def auth_retools_get_all_closed_loops_with_user_counts():
    uow = UnitOfWork()
    closed_loops = auth_qry.get_all_closed_loops_with_user_counts(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All closed loops returned successfully",
        status_code=201,
        data=closed_loops,
    ).__dict__


@retool.route("/auth-retools-update-closed-loop", methods=["PUT"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "id": sch.UuidSchema,
        "name": sch.ClosedLoopOrVendorNameSchema,
        "logo_url": sch.URLSchema,
        "description": sch.DescriptionSchema,
    }
)
def auth_retools_update_closed_loop():
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        auth_cmd.auth_retools_update_closed_loop(
            closed_loop_id=req["id"],
            name=req["name"],
            logo_url=req["logo_url"],
            description=req["description"],
            uow=uow,
        )
        uow.commit_close_connection()
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="Closed loop updated successfully",
        status_code=200,
    ).__dict__


@retool.route("/auth-retools-get-active-inactive-counts-of-a-closed_loop", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
def auth_retools_get_active_inactive_counts_of_a_closed_loop():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    counts = auth_qry.get_active_inactive_counts_of_a_closed_loop(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Counts returned successfully", status_code=200, data={"counts": counts}
    ).__dict__


@retool.route("/auth-retools-get-all-users-of-a-closed-loop", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
def auth_retools_get_information_of_all_users_of_a_closed_loop():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    users = auth_qry.get_information_of_all_users_of_a_closed_loop(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All users returned successfully",
        status_code=200,
        data={"users": users},
    ).__dict__


@retool.route("/auth-retools-create-vendor", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "personal_email": sch.EmailSchema,
        "password": sch.PasswordSchema,
        "phone_number": sch.PhoneNumberSchema,
        "full_name": sch.ClosedLoopOrVendorNameSchema,
        "longitude": sch.FloatSchema,
        "latitude": sch.FloatSchema,
        "closed_loop_id": sch.UuidSchema,
    }
)
def auth_retools_create_vendor():
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        user_id, should_create_wallet = auth_cmd.create_vendor_through_retool(
            personal_email=req["personal_email"],
            password=req["password"],
            phone_number=req["phone_number"],
            full_name=req["full_name"],
            location=(float(req["longitude"]), float(req["latitude"])),
            closed_loop_id=req["closed_loop_id"],
            unique_identifier=None,
            uow=uow,
            auth_svc=auth_acl.AuthenticationService(),
            fb_svc=auth_acl.FirebaseService(),
        )
        # if should_create_wallet:
        #     pmt_cmd.create_wallet(user_id=user_id, uow=uow)

        uow.commit_close_connection()
    except (
        pmt_mdl_ex.TransactionNotAllowedException,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="Vendor created successfully",
        status_code=201,
    ).__dict__


# PAYMENT RETOOLS


@retool.route("/payment-retools-get-closed-loops", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
def payment_retools_get_closed_loops():
    uow = UnitOfWork()
    closed_loops = pmt_qry.get_all_closed_loops_id_and_names(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All closed loops returned successfully",
        status_code=200,
        data={"closed_loops": closed_loops},
    ).__dict__


@retool.route(
    "/payment-retools-get-customers-and-ventors-of-selected-closed-loop",
    methods=["POST"],
)
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
def payment_retools_get_customers_and_vendors_of_selected_closed_loop():
    req = request.get_json(force=True)
    uow = UnitOfWork()
    customer_vendor_counts_dto = (
        pmt_qry.payment_retools_get_customers_and_vendors_of_selected_closed_loop(
            closed_loop_id=req["closed_loop_id"],
            uow=uow,
        )
    )
    uow.close_connection()

    return utils.Response(
        message="User, Vendor and total count returned successfully",
        status_code=200,
        data=customer_vendor_counts_dto,
    ).__dict__


@retool.route("/payment-retools-get-all-transaction-of-selected-user", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"user_wallet_id": sch.UuidSchema})
def payment_retools_get_all_transaction_of_selected_user():
    req = request.get_json(force=True)
    uow = UnitOfWork()
    transactions = pmt_qry.payment_retools_get_all_transactions_of_selected_user(
        user_id=req["user_wallet_id"],
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All transactions returned successfully",
        status_code=200,
        data={
            "transactions": transactions,
        },
    ).__dict__


@retool.route("/payment-retools-get-vendors-and-balance", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
def payment_retools_get_vendors_and_balance():
    """fetching only those vendors who have balance greater than 0"""

    req = request.get_json(force=True)
    uow = UnitOfWork()
    vendors = pmt_qry.payment_retools_get_vendors_and_balance(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All vendors returned successfully",
        status_code=200,
        data={"vendors": vendors},
    ).__dict__


@retool.route("/payment-retools-get-transactions-to-be-reconciled", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"vendor_id": sch.UuidSchema})
def payment_retools_get_transactions_to_be_reconciled():
    req = request.get_json(force=True)
    uow = UnitOfWork()
    transactions = pmt_qry.payment_retools_get_transactions_to_be_reconciled(
        vendor_id=req["vendor_id"],
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All transactions returned successfully",
        status_code=200,
        data={"transactions": transactions},
    ).__dict__


@retool.route("/payment-retools-reconcile-vendor", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"vendor_wallet_id": sch.UuidSchema})
def payment_retools_reconcile_vendor():
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        pmt_cmd.payment_retools_reconcile_vendor(
            tx_id=str(uuid4()),
            uow=uow,
            vendor_wallet_id=req["vendor_wallet_id"],
            auth_svc=pmt_acl.AuthenticationService(),
            pmt_svc=pmt_acl.PaymentService(),
        )
        uow.commit_close_connection()

    except pmt_svc_ex.TransactionFailedException as e:
        uow.commit_close_connection()
        raise utils.CustomException(str(e))

    except (
        pmt_mdl_ex.TransactionNotAllowedException,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="Vendor reconciled successfully",
        status_code=201,
    ).__dict__


@retool.route("/payment-retools-get-vendors", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
def payment_retools_get_vendors():
    req = request.get_json(force=True)
    uow = UnitOfWork()
    vendors = pmt_qry.payment_retools_get_vendors(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All vendors returned successfully",
        status_code=200,
        data={"vendors": vendors},
    ).__dict__


@retool.route("/payment-retools-get-reconciliation-history", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"vendor_id": sch.UuidSchema})
def payment_retools_get_reconciliation_history():
    req = request.get_json(force=True)
    uow = UnitOfWork()
    transactions = pmt_qry.payment_retools_get_reconciliation_history(
        vendor_id=req["vendor_id"],
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All transactions returned successfully",
        status_code=200,
        data={"transactions": transactions},
    ).__dict__


@retool.route("/payment-retools-get-reconciled-transactions", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "vendor_id": sch.UuidSchema,
        "reconciliation_txn_id": sch.UuidSchema,
    }
)
def payment_retools_get_reconciled_transactions():
    req = request.get_json(force=True)
    uow = UnitOfWork()
    transactions = pmt_qry.payment_retools_get_reconciled_transactions(
        vendor_id=req["vendor_id"],
        reconciliation_txn_id=req["reconciliation_txn_id"],
        uow=uow,
    )

    uow.close_connection()

    return utils.Response(
        message="All transactions returned successfully",
        status_code=200,
        data={"transactions": transactions},
    ).__dict__


@retool.route("/add-and-set-missing-marketing-weightages-to-zero", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
def add_and_set_missing_marketing_weightages_to_zero():
    uow = UnitOfWork()

    mktg_cmd.add_and_set_missing_weightages_to_zero(
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="Weightages added and set successfully",
        status_code=201,
    ).__dict__


@retool.route("/qr-retool-get-all-vendor-names-and-qr-ids-of-a-closed-loop", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
def qr_retool_get_all_vendor_names_and_qr_ids_of_a_closed_loop():
    req = request.get_json(force=True)
    uow = UnitOfWork()

    vendors = pmt_qry.get_all_vendor_id_name_and_qr_id_of_a_closed_loop(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Vendors returned successfully",
        status_code=200,
        data=vendors,
    ).__dict__


@retool.route("/get-daily-successful-deposits", methods=["POST"])
@utils.authenticate_retool_secret
def get_daily_successful_deposits():
    uow = UnitOfWork()

    deposits_dtos = pmt_qry.get_daily_successful_deposits(
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Daily successful deposits returned successfully",
        status_code=200,
        data={"deposits": deposits_dtos},
    ).__dict__


@retool.route("/get-daily-pending-deposits", methods=["POST"])
@utils.authenticate_retool_secret
def get_daily_pending_deposits():
    uow = UnitOfWork()

    deposits_dtos = pmt_qry.get_daily_pending_deposits(
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Daily pending deposits returned successfully",
        status_code=200,
        data={"deposits": deposits_dtos},
    ).__dict__


@retool.route("/get-daily-transactions", methods=["POST"])
@utils.authenticate_retool_secret
def get_daily_transactions():
    uow = UnitOfWork()

    transactions_dtos = pmt_qry.get_daily_transactions(
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Daily transactions returned successfully",
        status_code=200,
        data={"transactions": transactions_dtos},
    ).__dict__


@retool.route("/get-monthly-transactions", methods=["POST"])
@utils.authenticate_retool_secret
def get_monthly_transactions():
    uow = UnitOfWork()

    transactions_dtos = pmt_qry.get_monthly_transactions(
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Monthly transactions returned successfully",
        status_code=200,
        data={"transactions": transactions_dtos},
    ).__dict__


@retool.route("/get-total-users", methods=["POST"])
@utils.authenticate_retool_secret
def get_total_users():
    uow = UnitOfWork()

    total_users = auth_qry.get_total_users(
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Total users returned successfully",
        status_code=200,
        data={"total_users": total_users},
    ).__dict__


@retool.route("/get-signed-up-daily-users", methods=["POST"])
@utils.authenticate_retool_secret
def get_signed_up_daily_users():
    uow = UnitOfWork()

    daily_users = auth_qry.get_signed_up_daily_users(
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Daily users returned successfully",
        status_code=200,
        data={"daily_users": daily_users},
    ).__dict__


@retool.route("/get-total-phone-number-verified-users", methods=["POST"])
@utils.authenticate_retool_secret
def get_total_phone_number_verified_users():
    uow = UnitOfWork()

    total_users = auth_qry.get_total_phone_number_verified_users(
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Total users returned successfully",
        status_code=200,
        data={"total_users": total_users},
    ).__dict__


@retool.route("get-total-verified-closed-loops-users", methods=["POST"])
@utils.authenticate_retool_secret
def get_total_verified_closed_loops_users():
    uow = UnitOfWork()

    total_users = auth_qry.get_total_verified_closed_loops_users(
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Total users returned successfully",
        status_code=200,
        data={"total_users": total_users},
    ).__dict__


@retool.route("/get-total-dashboard-reached-users", methods=["POST"])
@utils.authenticate_retool_secret
def get_total_dashboard_reached_users():
    uow = UnitOfWork()

    total_users = auth_qry.get_total_dashboard_reached_users(
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Total users returned successfully",
        status_code=200,
        data={"total_users": total_users},
    ).__dict__


""" 
    --- --- --- --- --- --- --- --- --- --- --- ---
    Events
    --- --- --- --- --- --- --- --- --- --- --- ---
"""


@retool.route("/create-event", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "event_name": sch.EventNameSchema,
        "organizer_id": sch.UuidSchema,
        "venue": sch.EventNameSchema,
        "capacity": sch.EventCapacitySchema,
        "description": sch.DescriptionSchema,
        "image_url": sch.URLSchema,
        "closed_loop_id": sch.UuidSchema,
        "event_start_timestamp": sch.EventTimestampSchema,
        "event_end_timestamp": sch.EventTimestampSchema,
        "registration_start_timestamp": sch.EventTimestampSchema,
        "registration_end_timestamp": sch.EventTimestampSchema,
        "registration_fee": sch.AmountSchema,
        "event_type": sch.EventTypeSchema,
    }
)
def create_event():
    req = request.get_json(force=True)

    uow = UnitOfWork()

    try:
        event_cmd.create(
            id=str(uuid4()),
            status=event_mdl.EventStatus.DRAFT,
            registrations={},
            cancellation_reason="",
            name=req["event_name"],
            organizer_id=req["organizer_id"],
            venue=req["venue"],
            capacity=req["capacity"],
            description=req["description"],
            image_url=req["image_url"],
            closed_loop_id=req["closed_loop_id"],
            event_start_timestamp=req["event_start_timestamp"],
            event_end_timestamp=req["event_end_timestamp"],
            registration_start_timestamp=req["registration_start_timestamp"],
            registration_end_timestamp=req["registration_end_timestamp"],
            registration_fee=req["registration_fee"],
            event_type=req["event_type"],
            uow=uow,
            auth_acl=event_acl.AuthenticationService(),
        )
        uow.commit_close_connection()

    except (
        event_svc_exc.ClosedLoopDoesNotExist,
        event_svc_exc.EventNotCreatedByOrganizer,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(message="Event created", status_code=200).__dict__


@retool.route("/publish-event", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "event_id": sch.UuidSchema,
    }
)
def publish_event():
    req = request.get_json(force=True)

    uow = UnitOfWork()

    try:
        event_cmd.publish(event_id=req["event_id"], uow=uow)
        uow.commit_close_connection()

    except (
        event_mdl_exc.EventNotDrafted,
        event_mdl_exc.EventRegistrationEndsAfterStart,
        event_mdl_exc.EventEndsBeforeStartTime,
        event_mdl_exc.EventStartsBeforeRegistrationTime,
        event_mdl_exc.EventEndsBeforeRegistrationStartTime,
        event_mdl_exc.EventTicketPriceNegative,
        event_mdl_exc.EventCapacityExceeded,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(message="Event published", status_code=200).__dict__


@retool.route("/get-all-organizers", methods=["POST"])
@utils.authenticate_retool_secret
def get_all_organizers():
    uow = UnitOfWork()
    organizers = event_qry.get_all_organizers(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All organizers returned successfully",
        status_code=200,
        data=organizers,
    ).__dict__


@retool.route("/get-live-events", methods=["POST"])
@utils.authenticate_retool_secret
def get_live_events():
    closed_loop_id = request.args.get("closed_loop_id")
    uow = UnitOfWork()

    try:
        events = event_qry.get_live_events(closed_loop_id=closed_loop_id, uow=uow)
        uow.close_connection()

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="All live events returned successfully", status_code=200, data=events
    ).__dict__


@retool.route("/get-draft-events", methods=["POST"])
@utils.authenticate_retool_secret
def get_draft_events():
    uow = UnitOfWork()
    draft_events = event_qry.get_draft_events(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All draft events returned successfully",
        status_code=200,
        data=draft_events,
    ).__dict__


@retool.route("/form-schema", methods=["POST"])
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "event_id": sch.UuidSchema,
        "event_form_schema": sch.EventFormSchema,
    }
)
def form_schema():
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        event_id = req["event_id"]
        event_form_schema = event_mdl.Event.from_json_to_event_schema(
            event_schema_json=req["event_form_schema"]
        )
        event_cmd.add_form_schema(
            event_id=event_id,
            event_form_schema=event_form_schema,
            current_time=datetime.now() + timedelta(hours=5),
            uow=uow,
        )
        uow.commit_close_connection()

    except (event_mdl_exc.DuplicateFormSchema, event_mdl_exc.RegistrationStarted) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(message="Schema attached successfully", status_code=200, data={}).__dict__


@retool.route("/deposit-requests", methods=["POST"])
@utils.authenticate_retool_secret
def deposit_requests():
    uow = UnitOfWork()
    dr = pmt_qry.get_deposit_requests(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="Deposit requests returned successfully", status_code=200, data=dr
    ).__dict__


@retool.route("/daily-user-checkpoints", methods=["POST"])
@utils.authenticate_retool_secret
def daily_user_checkpoints():
    uow = UnitOfWork()
    duc = pmt_qry.get_daily_user_checkpoints(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="Daily user checkpoints returned successfully",
        status_code=200,
        data=duc,
    ).__dict__


@retool.route("paypro-ghost-invoices-report", methods=["POST"])
@utils.authenticate_retool_secret
def paypro_ghost_invoices_report():
    logging.info({"message": "PayPro ghost invoices report | starting"})

    pk_time = datetime.now() + timedelta(hours=5)
    pp_orders = pp_svc.invoice_range(
        start_date=pk_time - timedelta(weeks=8),
        end_date=pk_time,
    )
    logging.info(
        {
            "message": "PayPro ghost invoices report | Invoices fetched from PayPro",
            "pp_orders": [order.__dict__ for order in pp_orders],
        }
    )

    tx_ids = [res.tx_id for res in pp_orders]

    uow = UnitOfWork()
    try:
        txs = pmt_qry.get_many_transactions(tx_ids=tx_ids, uow=uow)
        uow.close_connection()
    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": "PayPro ghost invoices report | Unhandled exception in pmt_qry.get_many_transactions",
                "pp_orders": [order.__dict__ for order in pp_orders],
                "exception_type": 500,
                "exception_message": str(e),
            }
        )
        raise utils.CustomException(str(e))

    logging.info(
        {
            "message": "PayPro ghost invoices report | Pulled transactions from our db",
            "txs": [tx.__dict__ for tx in txs],
        }
    )

    set_tx_pp_id = set([tx.paypro_id for tx in txs])
    set_pp_id = set([order.paypro_id for order in pp_orders])

    ghost_pp_ids = set_pp_id.difference(set_tx_pp_id)

    ghost_paid_orders = [
        order
        for order in pp_orders
        if order.paypro_id in ghost_pp_ids and order.tx_status == "PAID"
    ]

    logging.info(
        {
            "message": "PayPro ghost invoices report | finished successfully!",
            "ghost_paid_orders": [order.__dict__ for order in ghost_paid_orders],
        }
    )

    return utils.Response(
        message="PayPro ghost invoices report finished successfully!",
        status_code=200,
        data=ghost_paid_orders,
    ).__dict__


@retool.route("/send-email-to-all", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "email_body_template": sch.StringSchema,
        "email_subject": sch.StringSchema,
    }
)
def send_email_to_all():
    req = request.get_json(force=True)

    uow = UnitOfWork()

    try:
        comms_cmd.send_personalized_emails(
            email_body_template=req["email_body_template"],
            email_subject=req["email_subject"],
            uow=uow,
            auth_acl=comms_acl.AuthenticationService(),
            task=comms_cmd.send_email,
        )
        uow.close_connection()

    except TimeoutError as e:
        uow.close_connection()
        raise utils.CustomException(str(e))
    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(message="Event published", status_code=200).__dict__


@retool.route("/send-event-registration-email", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"paypro_id": sch.StringSchema})
def send_event_registration_email():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    event_svc.send_registration_email(paypro_id=req["paypro_id"], uow=uow)
    uow.close_connection()

    return utils.Response(message="Event email sent!", status_code=200).__dict__


@retool.route("/force-transaction", methods=["POST"])
@utils.authenticate_retool_secret
def force_transaction():
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        pmt_cmd._execute_transaction(
            tx_id=str(uuid4()),
            amount=req["amount"],
            sender_wallet_id=req["sender_wallet_id"],
            recipient_wallet_id=req["recipient_wallet_id"],
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.CARD_PAY,
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
        )
        uow.commit_close_connection()

    except (
        pmt_mdl_ex.TransactionNotAllowedException,
        pmt_svc_ex.TransactionFailedException,
    ) as e:
        uow.commit_close_connection()
        logging.info(
            {
                "message": "Transaction failed exception raised",
                "endpoint": "/force-transaction",
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
                "message": "Custom exception raised",
                "endpoint": "/force-transaction",
                "invoked_by": "cardpay_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(message="Transaction forced successfully", status_code=200).__dict__


@retool.route("/reverse-deposit", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"tx_id": sch.UuidSchema})
def reverse_deposit():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        pmt_cmd.reverse_deposit(
            txn_id=req["tx_id"], uow=uow, auth_svc=pmt_acl.AuthenticationService()
        )
        uow.commit_close_connection()
    except pmt_svc_ex.TransactionFailedException as e:
        # If a reversal fails due to balance/txn issues save it else dont
        uow.commit_close_connection()
        logging.info(
            {
                "message": "Reversal failed due to transaction failure",
                "error": str(e),
                "exception": e.__class__.__name__,
            }
        )
    except (
        pmt_svc_ex.NotVerifiedException,
        pmt_mdl_ex.UnmarkedDepositReversal,
        pmt_mdl_ex.NotDepositReversal,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Reversal failed",
                "error": str(e),
                "exception": e.__class__.__name__,
            }
        )
        raise utils.CustomException(str(e))

    return utils.Response(message="Deposit reversed", status_code=200).__dict__


@retool.route("/get-all-deposits-to-reverse", methods=["POST"])
@utils.authenticate_retool_secret
def get_all_deposits_to_reverse():
    uow = UnitOfWork()
    deposits = pmt_qry.get_all_deposits_to_reverse(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All deposits returned successfully",
        status_code=200,
        data={"deposits": deposits},
    ).__dict__


@retool.route("/get-all-failed-reversals", methods=["POST"])
@utils.authenticate_retool_secret
def get_all_failed_reversals():
    uow = UnitOfWork()
    failed_reversals = pmt_qry.get_all_failed_reversals(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All failed reversals returned successfully",
        status_code=200,
        data={"failed_reversals": failed_reversals},
    ).__dict__


@retool.route("/get-all-users", methods=["POST"])
@utils.authenticate_retool_secret
def get_all_users():
    uow = UnitOfWork()
    users = auth_qry.get_all_users(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All users with ids and full names returned successfully",
        status_code=200,
        data={"users": users},
    ).__dict__


@retool.route("/bulk-reconcile-vendors", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={"vendor_wallet_ids": sch.ListOfUuidSchema}
)
def bulk_reconcile_vendors():
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        pmt_cmd.bulk_reconcile_vendors(
            vendor_wallet_ids=req["vendor_wallet_ids"],
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
            pmt_svc=pmt_acl.PaymentService(),
        )
        uow.commit_close_connection()

    except (
        pmt_svc_ex.TransactionFailedException,
        pmt_mdl_ex.TransactionNotAllowedException,
        mktg_mdl_ex.NegativeAmountException,
        mktg_mdl_ex.InvalidTransactionTypeException,
        mktg_mdl_ex.NotVerifiedException,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    balance_with_id_dtos = pmt_qry.get_latest_reconciliation_amounts(
        vendor_ids=req["vendor_wallet_ids"],
        uow=uow,
    )

    phone_number_with_id_dtos = auth_qry.get_phone_numbers_from_ids(
        user_ids=req["vendor_wallet_ids"],
        uow=uow,
    )

    balance_dict = {balance.id: balance for balance in balance_with_id_dtos}
    phone_number_dict = {
        phone_number.id: phone_number for phone_number in phone_number_with_id_dtos
    }

    # Merge the two DTOs based on ID
    merged_dtos = [
        {
            "balance": balance_dict.get(vendor_id).amount,
            "phone_number": phone_number_dict.get(vendor_id).phone_number,
        }
        for vendor_id in req["vendor_wallet_ids"]
    ]

    return utils.Response(
        message="Vendors Bulk reconciled successfully",
        status_code=201,
        data=merged_dtos,
    ).__dict__
