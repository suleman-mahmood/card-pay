# from dataclasses import asdict

import firebase_admin

from flask import Flask, request, jsonify

from core.api.utils import (
    authenticate_token,
    authenticate_user_type,
    handle_exceptions_uow,
    handle_missing_payload,
)
from core.payment.entrypoint import commands as payment_commands
from core.authentication.domain.model import UserType

from .api_cardpay_app import cardpay_app
from .api_retool import retool

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
PREFIX = "/api/v1"

cred = firebase_admin.credentials.Certificate("credentials-dev.json")
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

app.register_blueprint(cardpay_app)
app.register_blueprint(retool)


@app.route(PREFIX)
def base():
    """base endpoint"""

    return jsonify({"success": True, "message": "Welcome to the backend"}), 200


@app.route(PREFIX + "/pay-pro-callback", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.PAYMENT_GATEWAY])
@handle_exceptions_uow
@handle_missing_payload
def pay_pro_callback(uow):
    req = request.get_json(force=True)

    payment_commands.pay_pro_callback(
        uow=uow,
        data=req[""],  # TODO: fill these later
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "callback processed successfully",
            }
        ),
        201,
    )


# for testing purposes only ({{BASE_URL}}/api/v1/create-test-wallet)
# @app.route(PREFIX + "/create-test-wallet", methods=["POST"])
# @authenticate_token
# @authenticate_user_type(allowed_user_types = [UserType.ADMIN])
# @handle_exceptions_uow
# def create_test_wallet(uid, uow):
#     req = request.get_json(force=True)

#     with uow as uow:
#         payment_commands.create_wallet(user_id=uid, uow=uow)

#     return {
#         "success": True,
#         "message": "test wallet created successfully (only call me from create_user though)",
#     }, 200


# TODO: Check where this is used and then remove if not required
# @app.route(PREFIX + "/execute-transaction", methods=["POST"])
# @handle_exceptions_uow
# @handle_missing_payload
# def execute_transaction():
#     req = request.get_json(force=True)

#     payment_commands.execute_transaction(
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
