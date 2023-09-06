from flask import Blueprint, request
from flask_cors import CORS, cross_origin

from core.api import utils
from core.entrypoint.uow import UnitOfWork
from core.payment.entrypoint import queries as payment_qry
from core.authentication.domain.model import UserType

vendor_app = Blueprint("vendor_app", __name__, url_prefix="/api/v1")
cors = CORS(
    vendor_app,
    resources={"/get-vendor-transactions-to-be-reconciled": {"origins": "*"}},
)


@vendor_app.route("/get-vendor-transactions-to-be-reconciled", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.VENDOR])
@utils.user_verified
def get_vendor_transactions_to_be_reconciled(uid):
    uow = UnitOfWork()
    transactions = payment_qry.payment_retools_get_transactions_to_be_reconciled(
        vendor_id=uid,
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All transactions returned successfully",
        status_code=200,
        data=transactions,
    ).__dict__
