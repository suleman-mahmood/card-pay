from backend_ddd.core.entrypoint.uow import UnitOfWork
from core.api import schemas as sch
from core.api import utils
from flask import Blueprint, request
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.domain import exceptions as pmt_exc
from core.authentication.domain import exceptions as auth_exc
import json

rp_app = Blueprint("rp_app", __name__, url_prefix="/api/v1/rp")


@rp_app.route("/execute-offline-qr-transaction", methods=["POST"])
@utils.handle_missing_payload
@utils.authenticate_rp_secret
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "qr_data": sch.StringSchema,
        "amount": sch.AmountSchema,
        "document_id": sch.StringSchema,
    }
)
def exceute_offline_transaction():
    req = request.get_json(force=True)
    offline_payload = json.loads(req)
    qr_data = json.loads(offline_payload["qr_data"])
    uow = UnitOfWork()

    try:
        pmt_cmd.offline_qr_transaction(
            digest=qr_data["digest"],
            uow=uow,
            user_id=qr_data["user_id"],
            recipient_wallet_id=pmt_acl.PaymentService().get_lums_id(),
            amount=offline_payload["amount"],
            auth_svc=pmt_acl.AuthenticationService(),
            pmt_svc=pmt_acl.PaymentService(),
        )
    except (
        pmt_exc.OfflineQrExpired,
        auth_exc.DecryptionFailed,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except (
        Exception,
    ) as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="Offline Qr Transaction Executed Successfully",
        status_code=200,
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
