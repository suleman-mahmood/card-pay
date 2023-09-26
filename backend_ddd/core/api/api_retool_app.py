from flask import Blueprint, request

from uuid import uuid4
from core.api import utils
from core.entrypoint.uow import UnitOfWork
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.domain import model as auth_mdl
from core.marketing.entrypoint import commands as mktg_cmd
from core.authentication.entrypoint import commands as auth_cmd
from core.marketing.domain import exceptions as mktg_mdl_ex
from core.payment.entrypoint import queries as pmt_qry
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.domain import exceptions as pmt_mdl_ex
from core.api import schemas as sch
from core.authentication.entrypoint import anti_corruption as auth_acl
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import anti_corruption as pmt_acl

retool = Blueprint("retool", __name__, url_prefix="/api/v1")


@retool.route("/create-closed-loop", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_json_payload(
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
@utils.validate_json_payload(
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
@utils.validate_json_payload(
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
@utils.validate_json_payload(
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
@utils.validate_json_payload(
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


@retool.route(
    "/auth-retools-get-active-inactive-counts-of-a-closed_loop", methods=["POST"]
)
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.ADMIN])
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
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
@utils.validate_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
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
@utils.validate_json_payload(
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
@utils.validate_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
def payment_retools_get_customers_and_vendors_of_selected_closed_loop():
    req = request.get_json(force=True)
    uow = UnitOfWork()
    customer_vendor_counts_dto = pmt_qry.payment_retools_get_customers_and_vendors_of_selected_closed_loop(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
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
@utils.validate_json_payload(required_parameters={"user_wallet_id": sch.UuidSchema})
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
@utils.validate_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
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
@utils.validate_json_payload(required_parameters={"vendor_id": sch.UuidSchema})
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
@utils.validate_json_payload(required_parameters={"vendor_wallet_id": sch.UuidSchema})
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
@utils.validate_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
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
@utils.validate_json_payload(required_parameters={"vendor_id": sch.UuidSchema})
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
@utils.validate_json_payload(
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


@retool.route(
    "/qr-retool-get-all-vendor-names-and-qr-ids-of-a-closed-loop", methods=["POST"]
)
@utils.handle_missing_payload
@utils.authenticate_retool_secret
@utils.validate_json_payload(required_parameters={"closed_loop_id": sch.UuidSchema})
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
