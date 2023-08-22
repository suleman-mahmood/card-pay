# from dataclasses import asdict

import firebase_admin
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask, request, jsonify

from core.api import utils
from core.payment.entrypoint import commands as pmt_cmd
from core.authentication.domain import model as auth_mdl
from core.entrypoint.uow import UnitOfWork
from .api_cardpay_app import cardpay_app
from .api_retool import retool

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

cred = firebase_admin.credentials.Certificate("core/api/credentials-dev.json")
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


@app.route(PREFIX + "/pay-pro-callback", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.PAYMENT_GATEWAY])
@utils.handle_missing_payload
def pay_pro_callback():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    pmt_cmd.pay_pro_callback(
        uow=uow,
        data=req[""],  # TODO: fill these later
    )
    uow.close_connection()

    return utils.Response(
        message="callback processed successfully",
        status_code=201,
    )


# for testing purposes only ({{BASE_URL}}/api/v1/create-test-wallet)
# @app.route(PREFIX + "/create-test-wallet", methods=["POST"])
# @utils.authenticate_token
# @utils.authenticate_user_type(allowed_user_types = [auth_mdl.UserType.ADMIN])
# @utils.handle_exceptions_uow
# def create_test_wallet(uid, uow):
#     req = request.get_json(force=True)

#     with uow as uow:
#         pmt_cmd.create_wallet(user_id=uid, uow=uow)

#     return {
#         "success": True,
#         "message": "test wallet created successfully (only call me from create_user though)",
#     }, 200


# TODO: Check where this is used and then remove if not required
# @app.route(PREFIX + "/execute-transaction", methods=["POST"])
# @utils.handle_exceptions_uow
# @utils.handle_missing_payload
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
