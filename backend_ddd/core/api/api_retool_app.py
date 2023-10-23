from uuid import uuid4

from core.api import schemas as sch
from core.api import utils
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import anti_corruption as auth_acl
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.entrypoint.uow import UnitOfWork
from core.event.domain import exceptions as event_mdl_exc
from core.event.domain import model as event_mdl
from core.event.entrypoint import anti_corruption as event_acl
from core.event.entrypoint import commands as event_cmd
from core.event.entrypoint import exceptions as event_svc_exc
from core.event.entrypoint import queries as event_qry
from core.marketing.domain import exceptions as mktg_mdl_ex
from core.marketing.entrypoint import commands as mktg_cmd
from core.payment.domain import exceptions as pmt_mdl_ex
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import queries as pmt_qry
from flask import Blueprint, request
from datetime import datetime

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

@retool.route('/form-schema', methods=['POST'])
@utils.authenticate_retool_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"event_id": sch.UuidSchema, "event_form_schema": sch.EventFormSchema})
def form_schema():
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        form_schema = req["event_form_schema"]
        event_id = req["event_id"]
        event_form_schema = event_mdl.Event.from_json_to_event_schema(event_schema_json=form_schema)
        event_cmd.add_form_schema(
            event_id=event_id,
            event_form_schema=event_form_schema,
            current_time=datetime.now(),
            uow=uow
        )
        uow.commit_close_connection()

    except (event_mdl_exc.DuplicateFormSchema,
            event_mdl_exc.RegistrationStarted) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    return utils.Response(
        message='Schema attached successfully',
        status_code=200,
        data={}
    ).__dict__

