from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from core.api import utils
from core.entrypoint.uow import UnitOfWork
from core.payment.entrypoint import queries as pmt_qry
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import queries as auth_qry

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
    transactions = pmt_qry.vendor_app_get_transactions_to_be_reconciled(
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
