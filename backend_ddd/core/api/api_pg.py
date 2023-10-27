import logging
import os

from core.comms.entrypoint import anti_corruption as comms_acl
from core.comms.entrypoint import commands as comms_cmd
from core.comms.entrypoint import exceptions as comms_svc_ex
from core.entrypoint.uow import UnitOfWork
from core.marketing.entrypoint import queries as mktg_qry
from core.marketing.entrypoint import services as mktg_svc
from core.payment.domain import exceptions as pmt_mdl_ex
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import paypro_service as pp_svc
from core.payment.entrypoint import queries as pmt_qry
from flask import Blueprint, request

pg = Blueprint("pg", __name__, url_prefix="/api/v1")


@pg.route("/pay-pro-callback", methods=["POST"])
def pay_pro_callback():
    """This api will only be called by PayPro"""

    logging.info(
        {
            "message": "Pay Pro | Callback triggered",
            "json_body": request.get_json(),
        },
    )

    req = request.get_json()

    if request.get_json() is None:
        logging.info({"message": "Pay Pro | No json body"})
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
        logging.info({"message": "Pay Pro | Wrong json body"})
        return [
            {
                "StatusCode": "01",
                "InvoiceID": None,
                "Description": "Invalid Data. Username or password is invalid",
            }
        ], 200

    uow = UnitOfWork()
    try:
        success_invoice_ids, not_found_invoice_ids = pp_svc.pay_pro_callback(
            user_name=user_name,
            password=password,
            csv_invoice_ids=csv_invoice_ids,
            uow=uow,
        )

    except pmt_svc_ex.InvalidPayProCredentialsException:
        logging.info(
            {
                "message": "Pay Pro | Invalid credentials",
                "passed_credentials": {
                    "user_name": user_name,
                    "password": password,
                },
                "my_credentials": {
                    "user_name": os.environ.get("PAYPRO_USERNAME"),
                    "password": os.environ.get("PAYPRO_PASSWORD"),
                },
            },
        )
        uow.close_connection()
        return [
            {
                "StatusCode": "02",
                "InvoiceID": None,
                "Description": "Service Failure",
            }
        ], 200

    except Exception:
        logging.info({"message": "Pay Pro | An exception triggered"})
        uow.close_connection()
        return [
            {
                "StatusCode": "02",
                "InvoiceID": None,
                "Description": "Service Failure",
            }
        ], 200

    logging.info(
        {
            "message": "Pay Pro | Going to give cashbacks",
            "success_invoice_ids": success_invoice_ids,
            "failed_invoice_ids": not_found_invoice_ids,
        },
    )

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
        except pmt_svc_ex.TransactionFailedException:
            pass

    # Send notifications
    for tx_id in success_invoice_ids:
        tx = uow.transactions.get(transaction_id=tx_id)
        try:
            comms_cmd.send_notification(
                user_id=tx.recipient_wallet.id,
                title="Deposit success!",
                body=f"${tx.amount} was deposited in your CardPay account",
                uow=uow,
                comms_svc=comms_acl.CommunicationService(),
            )
        except comms_svc_ex.FcmTokenNotFound:
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

    logging.info(
        {
            "message": "Pay Pro | Callback finished successfully",
            "response": res,
        },
    )

    uow.commit_close_connection()
    return res, 200
