# from dataclasses import asdict

import firebase_admin
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask, request

from core.api import utils
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_cmd_exc
from core.payment.domain import exceptions as pmt_ex
from core.payment.domain import model as pmt_mdl
from core.marketing.domain import exceptions as mktg_ex
from core.entrypoint.uow import UnitOfWork
from core.api.api_vendor_app import vendor_app
from core.api.api_cardpay_app import cardpay_app
from core.api.api_retool_app import retool
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.marketing.entrypoint import services as mktg_svc
from core.marketing.entrypoint import queries as mktg_qry
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import queries as pmt_qry

from dotenv import load_dotenv

load_dotenv()

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[
        FlaskIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

app.register_blueprint(cardpay_app)
app.register_blueprint(retool)
app.register_blueprint(vendor_app)

cred = firebase_admin.credentials.Certificate("core/api/credentials-prod.json")
firebase_admin.initialize_app(cred)

# 200 OK
# The request succeeded. The result meaning of "success" depends on the HTTP method:

# 201 Created
# The request succeeded, and a new resource was created as a result.
# This is typically the response sent after POST requests, or some PUT requests.

# 400 Bad Request
# The server cannot or will not process the request due to something
# that is perceived to be a client error (e.g., malformed request syntax,
# invalid request message framing, or deceptive request routing).

# 401 Unauthorized
# Although the HTTP standard specifies "unauthorized", semantically this response means
# "unauthenticated". That is, the client must authenticate itself to get the requested response.

# 404 Not Found
# The server cannot find the requested resource. In the browser, this means the URL is
# not recognized. In an API, this can also mean that the endpoint is valid but the resource
# itself does not exist. Servers may also send this response instead of 403 Forbidden to hide
# the existence of a resource from an unauthorized client. This response code is probably the most
# well known due to its frequent occurrence on the web.

# 500 Internal Server Error
# The server has encountered a situation it does not know how to handle.

PREFIX = "/api/v1"


@app.route(PREFIX)
def base():
    """base endpoint"""

    return utils.Response(message="Welcome to the backend", status_code=200).__dict__


@app.errorhandler(utils.CustomException)
def handle_exceptions(e: utils.CustomException):
    payload = {
        "message": e.message,
        "event_code": e.event_code.name,
    }
    return payload, e.status_code


# TODO: move this to a new file, 'api_pg.py' probably
@app.route(PREFIX + "/pay-pro-callback", methods=["POST"])
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


# for testing purposes only ({{BASE_URL}}/api/v1/create-test-wallet)
# @app.route(PREFIX + "/create-test-wallet", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types = [auth_mdl.UserType.ADMIN])
# # def create_test_wallet(uid, uow):
#     req = request.get_json(force=True)

#     with uow as uow:
#         pmt_cmd.create_wallet(user_id=uid, uow=uow)

#     return {
#         "success": True,
#         "message": "test wallet created successfully (only call me from create_user though)",
#     }, 200


# TODO: Check where this is used and then remove if not required
# @app.route(PREFIX + "/execute-transaction", methods=["POST"])
# # @utils.handle_missing_payload
# def execute_transaction():
#     req = request.get_json(force=True)

#     pmt_cmd.execute_transaction(
#         sender_wallet_id=req["sender_wallet_id"],
#         recipient_wallet_id=req["recipient_wallet_id"],
#         amount=req["amount"],
#         transaction_mode=TransactionMode.__members__[req["transaction_mode"]],
#         transaction_type=TransactionType.__members__[req["transaction_type"]],
#         uow=uow,
#     )
#     return (
#         jsonify({"success": True, "message": "transaction executed successfully"}),
#         200,
#     )
