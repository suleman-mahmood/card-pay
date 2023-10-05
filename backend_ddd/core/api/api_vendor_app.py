from core.api import schemas as sch
from core.api import utils
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import queries as auth_qry
from core.entrypoint.uow import UnitOfWork
from core.payment.entrypoint import queries as pmt_qry
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

vendor_app = Blueprint("vendor_app", __name__, url_prefix="/api/v1/vendor-app")

cors = CORS(
    vendor_app,
    resources={"/*": {"origins": "*"}},
)


@vendor_app.route("/get-vendor-transactions-to-be-reconciled", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.VENDOR])
@utils.user_verified
def get_vendor_transactions_to_be_reconciled(uid):
    uow = UnitOfWork()
    transactions = pmt_qry.payment_retools_get_transactions_to_be_reconciled(
        vendor_id=uid,
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All transactions returned successfully",
        status_code=200,
        data=transactions,
    ).__dict__


@vendor_app.route("/get-vendor-balance", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.VENDOR])
@utils.user_verified
def get_vendor_balance(uid):
    uow = UnitOfWork()
    balance = auth_qry.get_user_balance(
        user_id=uid,
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Vendor balance returned successfully",
        status_code=200,
        data={
            "balance": balance,
        },
    ).__dict__


@vendor_app.route("/get-vendor", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.VENDOR])
@utils.user_verified
def get_vendor(uid):
    uow = UnitOfWork()
    user = auth_qry.get_user_from_user_id(user_id=uid, uow=uow)
    uow.close_connection()

    return utils.Response(
        message="User returned successfully",
        status_code=200,
        data=user.__dict__,
    ).__dict__


""" 
    --- --- --- --- --- --- --- --- --- --- --- ---
    Events
    --- --- --- --- --- --- --- --- --- --- --- ---
"""


@vendor_app.route("/get-live-events", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.CUSTOMER])
@utils.user_verified
def get_live_events(uid):
    raise utils.CustomException("Not implemented")
    uow = UnitOfWork()

    try:
        uow.close_connection()

    except () as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(message="", status_code=200, data={}).__dict__


@vendor_app.route("/mark-entry-event-attendance", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.VENDOR])
@utils.user_verified
@utils.validate_and_sanitize_json_payload(
    required_parameters={"event_id": sch.UuidSchema, "qr_id": sch.UuidSchema}
)
def mark_entry_event_attendance(uid):
    raise utils.CustomException("Not implemented")
    uow = UnitOfWork()

    try:
        uow.close_connection()

    except () as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(message="", status_code=200, data={}).__dict__


@vendor_app.route("/mark-exit-event-attendance", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.VENDOR])
@utils.user_verified
@utils.validate_and_sanitize_json_payload(
    required_parameters={"event_id": sch.UuidSchema, "qr_id": sch.UuidSchema}
)
def mark_exit_event_attendance(uid):
    raise utils.CustomException("Not implemented")
    uow = UnitOfWork()

    try:
        uow.close_connection()

    except () as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(message="", status_code=200, data={}).__dict__
