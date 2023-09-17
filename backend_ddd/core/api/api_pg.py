from flask import Blueprint, request

from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_cmd_exc
from core.payment.domain import model as pmt_mdl
from core.entrypoint.uow import UnitOfWork
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.marketing.entrypoint import services as mktg_svc
from core.marketing.entrypoint import queries as mktg_qry
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import queries as pmt_qry

pg = Blueprint("pg", __name__, url_prefix="/api/v1")


@pg.route("/pay-pro-callback", methods=["POST"])
def pay_pro_callback():
    """This api will only be called by PayPro"""

    req = request.get_json(force=True)

    if request.get_json() is None:
        return [
            {
                "StatusCode": "01",
                "InvoiceID": None,
                "Description": "Invalid Data. Username or password is invalid",
            }
        ], 200

    try:
        user_name = req["username"]
        password = req["password"]
        csv_invoice_ids = req["csvinvoiceids"]
    except KeyError as e:
        return [
            {
                "StatusCode": "01",
                "InvoiceID": None,
                "Description": "Invalid Data. Username or password is invalid",
            }
        ], 200

    uow = UnitOfWork()
    try:
        success_invoice_ids, not_found_invoice_ids = pmt_cmd.pay_pro_callback(
            user_name=user_name,
            password=password,
            csv_invoice_ids=csv_invoice_ids,
            uow=uow,
        )

    except pmt_cmd_exc.InvalidPayProCredentialsException:
        uow.close_connection()
        return [
            {
                "StatusCode": "02",
                "InvoiceID": None,
                "Description": "Service Failure",
            }
        ], 200

    except Exception:
        uow.close_connection()
        return [
            {
                "StatusCode": "02",
                "InvoiceID": None,
                "Description": "Service Failure",
            }
        ], 200

    # Give cashbacks for all the accepted transactions
    all_cashbacks = mktg_qry.get_all_cashbacks(uow=uow)
    for tx_id in success_invoice_ids:
        tx_amount = pmt_qry.get_tx_balance(tx_id=tx_id, uow=uow)
        recipient_wallet_id = pmt_qry.get_tx_recipient(tx_id=tx_id, uow=uow)
        cashback_amount = mktg_svc.calculate_cashback(
            amount=tx_amount,
            invoker_transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
            all_cashbacks=all_cashbacks,
        )
        try:
            pmt_cmd.execute_cashback_transaction(
                recipient_wallet_id=recipient_wallet_id,
                cashback_amount=cashback_amount,
                pmt_svc=pmt_acl.PaymentService(),
                auth_svc=pmt_acl.AuthenticationService(),
                uow=uow,
            )
        except pmt_mdl.TransactionNotAllowedException:
            pass

    res = []
    for invoice_id in success_invoice_ids:
        res.append(
            {
                "StatusCode": "00",
                "InvoiceID": invoice_id,
                "Description": "Invoice successfully marked as paid",
            }
        )
    for invoice_id in not_found_invoice_ids:
        res.append(
            {
                "StatusCode": "03",
                "InvoiceID": invoice_id,
                "Description": "No records found.",
            }
        )

    uow.commit_close_connection()
    return res, 200
