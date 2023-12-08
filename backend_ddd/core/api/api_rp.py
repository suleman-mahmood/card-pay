from core.api import schemas as sch
from core.api import utils
from flask import Blueprint, request

rp_app = Blueprint("rp_app", __name__, url_prefix="/api/v1/rp")


@rp_app.route("/execute-offline-qr-transaction", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_rp_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "qr_data": sch.StringSchema,
        "amount": sch.AmountSchema,
        "tx_id": sch.StringSchema,
    }
)
def exceute_offline_transaction():
    req = request.get_json(force=True)

    if req["amount"] < 500:
        raise utils.CustomException("Amount less than 500")

    return utils.Response(
        message="Transaction made successfully",
        status_code=201,
    ).__dict__


@rp_app.route("/reverse-transaction", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_rp_secret
@utils.validate_and_sanitize_json_payload(required_parameters={"tx_id": sch.StringSchema})
def reverse_transaction():
    req = request.get_json(force=True)

    if req["tx_id"] != "12345":
        raise utils.CustomException("Transaction ID does not exist")

    return utils.Response(
        message="Transaction made successfully",
        status_code=201,
    ).__dict__
