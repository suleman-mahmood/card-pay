from dataclasses import asdict

# import firebase_admin
# from firebase_admin import credentials, auth
from flask import Flask, request, jsonify

from backend_ddd.api.utils import handle_exceptions  # authenticate_token
from backend_ddd.entrypoint.uow import UnitOfWork
from backend_ddd.payment.entrypoint import commands as payment_commands
from backend_ddd.payment.domain.model import (
    TransactionMode,
    TransactionType,
    TransactionStatus,
)
from backend_ddd.marketing.entrypoint import commands as marketing_commands

app = Flask(__name__)
PREFIX = "/api/v1"

# TODO: add firebase admin credentials here
# cred = credentials.Certificate("")
# firebase_admin.initialize_app(cred)

# Or this in app engine
# default_app = firebase_admin.initialize_app()

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


@app.route(PREFIX)
def hello():
    """Simple hello world endpoint"""

    return "Welcome to the MySpots api!", 200


@app.route(PREFIX + "/create-user", methods=["POST"])
# @authenticate_token
def create_user(uid):
    """Create a new user account"""
    raise NotImplementedError

    # if request.json is None:
    #     return_obj = {"message": "payload missing in request"}
    #     return jsonify(return_obj), 400

    # try:
    #     user = commands.create_user(
    #         id=uid,
    #         full_name=request.json["full_name"],
    #         user_name=request.json["user_name"],
    #         email=request.json["email"],
    #         phone_number=request.json["phone_number"],
    #         profile_text=request.json["profile_text"],
    #         location=tuple(request.json["location"]),
    #         avatar_url=request.json["avatar_url"],
    #         uow=unit_of_work.UnitOfWork(),
    #     )
    #     return_obj = {"message": "User created successfully!", "user_id": user.id}
    #     return jsonify(return_obj), 201

    # except Exception as exception:
    #     return_obj = {"message": str(exception)}
    #     return jsonify(return_obj), 400


# Get requests


@app.route(PREFIX + "/decode-access-token", methods=["GET"])
def decode_access_token():
    raise NotImplementedError

    # """Decode an access token"""

    # # Fetch the token from the request headers
    # auth_header = request.headers.get("Authorization")
    # if not auth_header:
    #     return "Unauthorized", 401

    # # Extract the token from the Authorization header
    # token = auth_header.split("Bearer ")[1]

    # decoded_token = auth.verify_id_token(token)
    # uid = decoded_token["uid"]

    # return_obj = {"decoded_token": decoded_token, "uid": uid}
    # return jsonify(return_obj), 200


@app.route(PREFIX + "/get-user", methods=["GET"])
# @authenticate_token
def get_user(uid):
    raise NotImplementedError

    # """Get a user"""

    # user = queries.get_user(
    #     user_id=uid,
    #     uow=unit_of_work.UnitOfWork(),
    # )

    # user_dict = asdict(user)
    # for attr, value in user_dict.items():
    #     if isinstance(value, set):
    #         user_dict[attr] = list(value)

    # user_dict["followers"] = len(user_dict["followers"])
    # user_dict["following"] = len(user_dict["following"])

    # return_obj = {"user": user_dict}
    # return jsonify(return_obj), 200


# post requests
# flask --app ./api/flask_app.py run --debug


# for testing purposes only ({{BASE_URL}}/api/v1/create-test-wallet)
@app.route(PREFIX + "/create-test-wallet", methods=["POST"])
@handle_exceptions
def create_test_wallet():
    with UnitOfWork() as uow:
        payment_commands.create_wallet(uow=uow)
    return {
        "success": True,
        "message": "test wallet created successfully (only call me from create_user though)",
    }, 200


@app.route(PREFIX + "/execute-transaction", methods=["POST"])
def execute_transaction():
    if request.json is None:
        return jsonify({"success": False, "message": "payload missing in request"}), 400

    payment_commands.execute_transaction(
        sender_wallet_id=request.json["sender_wallet_id"],
        recipient_wallet_id=request.json["recipient_wallet_id"],
        amount=request.json["amount"],
        transaction_mode=TransactionMode.__members__[request.json["transaction_mode"]],
        transaction_type=TransactionType.__members__[request.json["transaction_type"]],
        uow=UnitOfWork(),
    )
    return (
        jsonify({"success": True, "message": "transaction executed successfully"}),
        200,
    )


@app.route(PREFIX + "/accept-p2p-pull-transaction", methods=["POST"])
@handle_exceptions
def accept_p2p_pull_transaction():
    if request.json is None:
        return jsonify({"success": False, "message": "payload missing in request"}), 400

    payment_commands.accept_p2p_pull_transaction(
        transaction_id=request.json["transaction_id"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "p2p pull transaction accepted successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/decline-p2p-pull-transaction", methods=["POST"])
@handle_exceptions
def decline_p2p_pull_transaction():
    if request.json is None:
        return jsonify({"success": False, "message": "payload missing in request"}), 400

    payment_commands.decline_p2p_pull_transaction(
        transaction_id=request.json["transaction_id"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "p2p pull transaction declined successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/generate-voucher", methods=["POST"])
@handle_exceptions
def generate_voucher():
    if request.json is None:
        return jsonify({"success": False, "message": "payload missing in request"}), 400

    payment_commands.generate_voucher(
        sender_wallet_id=request.json["sender_wallet_id"],
        amount=request.json["amount"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "voucher generated successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/redeem-voucher", methods=["POST"])
@handle_exceptions
def redeem_voucher():
    if request.json is None:
        return jsonify({"success": False, "message": "payload missing in request"}), 400

    payment_commands.redeem_voucher(
        recipient_wallet_id=request.json["recipient_wallet_id"],
        transaction_id=request.json["transaction_id"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "voucher redeemed successfully",
            }
        ),
        200,
    )

@app.route(PREFIX + "/use-reference", methods=["POST"])
@handle_exceptions
def use_reference():
    if request.json is None:
        return jsonify({"success": False, "message": "payload missing in request"}), 400

    marketing_commands.use_reference(
        referee_id = request.json["referee_id"],
        referral_id = request.json["referral_id"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "reference used successfully",
            }
        ),
        200,
    )

# Admin Portal Routes

@app.route(PREFIX + "/add-weightage", methods=["POST"])
@handle_exceptions
def add_weightage():
    if request.json is None:
        return jsonify({"success": False, "message": "payload missing in request"}), 400

    marketing_commands.add_weightage(
        weightage_type = request.json["weightage_type"],
        weightage_value = request.json["weightage_value"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "weightage added successfully",
            }
        ),
        200,
    )

@app.route(PREFIX + "/set-weightage", methods=["POST"])
@handle_exceptions
def set_weightage():
    if request.json is None:
        return jsonify({"success": False, "message": "payload missing in request"}), 400

    marketing_commands.set_weightage(
        weightage_type = request.json["weightage_type"],
        weightage_value = request.json["weightage_value"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "weightage set successfully",
            }
        ),
        200,
    )

@app.route(PREFIX + "/set-cashback-slabs", methods=["POST"])
@handle_exceptions
def set_cashback_slabs():
    if request.json is None:
        return jsonify({"success": False, "message": "payload missing in request"}), 400

    cashback_slabs = request.json["cashback_slabs"]

    marketing_commands.set_cashback_slabs(
        cashback_slabs = cashback_slabs,
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "cashback slabs set successfully",
            }
        ),
    )
