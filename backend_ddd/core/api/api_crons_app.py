import logging
import os
from datetime import datetime, timedelta

from core.comms.entrypoint import anti_corruption as comms_acl
from core.comms.entrypoint import commands as comms_cmd
from core.comms.entrypoint import exceptions as comms_svc_ex
from core.entrypoint.uow import UnitOfWork
from core.event.entrypoint import exceptions as event_ex
from core.event.entrypoint import services as event_svc
from core.marketing.entrypoint import queries as mktg_qry
from core.marketing.entrypoint import services as mktg_svc
from core.payment.domain import exceptions as pmt_mdl_ex
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import paypro_service as pp_svc
from core.payment.entrypoint import queries as pmt_qry
from flask import Blueprint

crons_app = Blueprint("crons_app", __name__, url_prefix="/api/v1/crons-app")


@crons_app.route("paypro-inquiry-cron", methods=["GET"])
def paypro_manual_inquiry():
    logging.info({"message": "PayPro inquiry cron | starting"})

    uow = UnitOfWork()

    # Get last pending deposit requests
    pk_time = datetime.now() + timedelta(hours=5)
    pp_orders = pp_svc.invoice_range(
        start_date=pk_time - timedelta(hours=1),
        end_date=pk_time,
    )

    pp_paid_tx_ids = [pp_order.tx_id for pp_order in pp_orders if pp_order.tx_status == "PAID"]

    logging.info(
        {
            "message": "PayPro inquiry cron | Filtered paid txns",
            "txs": pp_paid_tx_ids,
        }
    )

    # These are the txns that are paid in PayPro but pending in our db
    paid_txs = pmt_qry.get_pending_pg_txs_from_ids(pp_paid_tx_ids, uow)
    logging.info(
        {
            "message": "PayPro inquiry cron | Fetched pending txns",
            "txs": paid_txs,
        }
    )

    # For all of them that are now paid, run the callback function
    user_name = os.environ.get("PAYPRO_USERNAME")
    user_name = user_name if user_name is not None else ""

    password = os.environ.get("PAYPRO_PASSWORD")
    password = password if password is not None else ""

    success_invoice_ids = []
    for tx_id in paid_txs:
        success_ids, _ = pp_svc.pay_pro_callback(
            user_name=user_name,
            password=password,
            csv_invoice_ids=tx_id,
            uow=uow,
        )
        success_invoice_ids += success_ids

    logging.info(
        {
            "message": "PayPro inquiry cron | Marked pending txns as paid in our database",
            "txs": success_invoice_ids,
        }
    )

    ### ### ###
    # Do the rest of important stuff
    ### ### ###

    # Give cashbacks for all the accepted transactions
    all_cashbacks = mktg_qry.get_all_cashbacks(uow=uow)
    cb = []
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
            cb.append(
                {
                    "cashback_amount": cashback_amount,
                    "recipient_wallet_id": recipient_wallet_id,
                }
            )
        except pmt_svc_ex.TransactionFailedException:
            pass

    logging.info({"message": "PayPro inquiry cron | Cashbacks given", "cashbacks": cb})

    # Send notifications
    notifs = []
    for tx_id in success_invoice_ids:
        tx = uow.transactions.get(transaction_id=tx_id)
        try:
            comms_cmd.send_notification(
                user_id=tx.recipient_wallet.id,
                title="Deposit Success! 🎉",
                body=f"Yay! {tx.amount} is deposited in your CardPay wallet 🥳",
                uow=uow,
                comms_svc=comms_acl.CommunicationService(),
            )
            notifs.append(
                {
                    "user_id": tx.recipient_wallet.id,
                    "amount": tx.amount,
                    "status": "sent",
                }
            )
        except comms_svc_ex.FcmTokenNotFound as e:
            logging.info(
                {
                    "message": "Pay Pro | Can't send notification | Custom exception raised",
                    "exception_type": e.__class__.__name__,
                    "exception_message": str(e),
                    "silent": True,
                },
            )
            notifs.append(
                {
                    "user_id": tx.recipient_wallet.id,
                    "amount": tx.amount,
                    "status": "token_not_found",
                }
            )
        except Exception as e:
            logging.info(
                {
                    "message": "Pay Pro | Can't send notification | Unhandled exception raised",
                    "exception_type": 500,
                    "exception_message": str(e),
                    "silent": True,
                },
            )
            notifs.append(
                {
                    "user_id": tx.recipient_wallet.id,
                    "amount": tx.amount,
                    "status": "error_500",
                }
            )

    logging.info({"message": "PayPro inquiry cron | Notifications sent", "notifs": notifs})

    # Send registration emails to successful people
    reg_emails = []
    for tx_id in success_invoice_ids:
        tx = uow.transactions.get(transaction_id=tx_id)
        try:
            event_svc.send_registration_email(tx_id=tx.id, uow=uow)
            reg_emails.append({"tx_id": tx.id, "status": "sent"})
        except event_ex.TxIdDoesNotExist as e:
            logging.info(
                {
                    "message": "Pay Pro | Can't send email | Paypro ID does not exist",
                    "exception_type": e.__class__.__name__,
                    "tx_id": tx.id,
                    "exception_message": str(e),
                    "silent": True,
                },
            )
            reg_emails.append({"tx_id": tx.id, "status": "no_regis_for_pp_id"})
        except Exception as e:
            logging.info(
                {
                    "message": "Pay Pro | Can't send email | Unhandled exception raised",
                    "tx_id": tx.id,
                    "exception_type": 500,
                    "exception_message": str(e),
                    "silent": True,
                },
            )
            reg_emails.append({"tx_id": tx.id, "status": "error_500"})

    logging.info(
        {
            "message": "PayPro inquiry cron | Event registration confirmation emails sent",
            "reg_emails": reg_emails,
        }
    )

    uow.commit_close_connection()
    logging.info({"message": "PayPro inquiry cron | finished successfully!"})

    return "PayPro Inquiry Cron finished successfully!", 200


@crons_app.route("reverse-transaction-cron", methods=["GET"])
def reverse_transaction_cron():
    """
    Runs every day and marks all the transactions of the entire week that
     are to be reversed
    """

    logging.info({"message": "Reverse Transaction cron | starting"})

    uow = UnitOfWork()

    pk_time = datetime.now() + timedelta(hours=5)
    pp_orders = pp_svc.invoice_range(
        start_date=pk_time - timedelta(days=7),
        end_date=pk_time,
        uow=uow,
    )

    unpaid_pp_txns = [pp_order.tx_id for pp_order in pp_orders if pp_order.tx_status == "UNPAID"]

    logging.info(
        {
            "message": "Reverse Transaction cron | Filtered unpaid txns",
            "txs": unpaid_pp_txns,
        }
    )

    txns_to_reverse = pmt_qry.get_successful_pg_txs_from_ids(tx_ids=unpaid_pp_txns, uow=uow)

    logging.info(
        {
            "message": "Reverse Transaction cron | Fetched txns to reverse",
            "txs": txns_to_reverse,
        }
    )
    for txn_id in txns_to_reverse:
        try:
            pmt_cmd.mark_as_to_reverse(txn_id=txn_id, uow=uow)
        except (
            pmt_mdl_ex.ReversingUnsuccessfulTransaction,
            pmt_mdl_ex.NotDepositReversal,
            pmt_mdl_ex.AlreadyMarkedToReverse,
        ) as e:
            logging.info(
                {
                    "message": "Reverse Transaction cron | Can't mark as to reverse | Custom exception raised",
                    "exception_type": e.__class__.__name__,
                    "exception_message": str(e),
                    "silent": True,
                },
            )

    uow.commit_close_connection()

    logging.info(
        {
            "message": "Reverse transaction cron | Marked transactions as to reverse",
            "txns": txns_to_reverse,
        }
    )
