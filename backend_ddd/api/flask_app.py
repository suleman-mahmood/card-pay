# from dataclasses import asdict

import firebase_admin

from flask import Flask, request, jsonify

from backend_ddd.api.utils import (
    handle_exceptions,
    handle_missing_payload,
    authenticate_token,
)
from backend_ddd.entrypoint.uow import UnitOfWork
from backend_ddd.payment.entrypoint import commands as payment_commands
from backend_ddd.payment.domain.model import (
    TransactionMode,
    TransactionType,
)
from backend_ddd.authentication.entrypoint import queries as authentication_queries
from backend_ddd.marketing.entrypoint import commands as marketing_commands
from backend_ddd.authentication.entrypoint import commands as authentication_commands
from backend_ddd.payment.entrypoint import queries as payment_queries

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
PREFIX = "/api/v1"


cred = firebase_admin.credentials.Certificate("credentials-dev.json")
firebase_admin.initialize_app(cred)

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
def base():
    """base endpoint"""

    return jsonify({"success": True, "message": "Welcome to the backend"}), 200


@app.route(PREFIX + "/create-user", methods=["POST"])
# @authenticate_token
@handle_exceptions
@handle_missing_payload
def create_user():
    """Create a new user account"""
    authentication_commands.create_user(
        personal_email=request.json["personal_email"],
        password=request.json["password"],
        phone_number=request.json["phone_number"],
        user_type=request.json["user_type"],
        full_name=request.json["full_name"],
        location=request.json["location"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "User created successfully",
            }
        ),
        201,
    )


@app.route(PREFIX + "/create-customer", methods=["POST"])
# @authenticate_token
@handle_exceptions
@handle_missing_payload
def create_customer():
    """
    Create a new user account of type customer

    phone_number = '03333462677'
    """

    event_code, user_id = authentication_commands.create_user(
        personal_email=request.json["personal_email"],
        password=request.json["password"],
        phone_number=request.json["phone_number"],
        user_type="CUSTOMER",
        full_name=request.json["full_name"],
        location=request.json["location"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "User created successfully",
                "event_code": event_code.name,
                "user_id": user_id,
            }
        ),
        201,
    )


@app.route(PREFIX + "/create-closed-loop", methods=["POST"])
@handle_missing_payload
@handle_exceptions
def create_closed_loop():
    authentication_commands.create_closed_loop(
        name=request.json["name"],
        logo_url=request.json["logo_url"],
        description=request.json["description"],
        verification_type=request.json["verification_type"],
        regex=request.json["regex"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "Closed loop created successfully",
            }
        ),
        201,
    )


@app.route(PREFIX + "/change-name", methods=["POST"])
@handle_exceptions
@handle_missing_payload
def change_name():
    authentication_commands.change_name(
        user_id=request.json["user_id"],
        new_name=request.json["new_name"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "Name changed successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/change-pin", methods=["POST"])
@handle_exceptions
@handle_missing_payload
def change_pin():
    authentication_commands.change_pin(
        user_id=request.json["user_id"],
        new_pin=request.json["new_pin"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "Pin changed successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/user-toggle-active", methods=["POST"])
@handle_exceptions
@handle_missing_payload
def user_toggle_active():
    authentication_commands.user_toggle_active(
        user_id=request.json["user_id"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "User toggled active successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/verify-otp", methods=["POST"])
@handle_exceptions
@handle_missing_payload
def verify_otp():
    authentication_commands.verify_otp(
        user_id=request.json["user_id"],
        otp=request.json["otp"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "OTP verified successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/verify-phone-number", methods=["POST"])
@handle_exceptions
@handle_missing_payload
def verify_phone_number():
    authentication_commands.verify_phone_number(
        user_id=request.json["user_id"],
        otp=request.json["otp"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "Phone number verified successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/register-closed-loop", methods=["POST"])
@handle_exceptions
@handle_missing_payload
def register_closed_loop():
    authentication_commands.register_closed_loop(
        user_id=request.json["user_id"],
        closed_loop_id=request.json["closed_loop_id"],
        unique_identifier=request.json["unique_identifier"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "User registered into loop successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/verify-closed-loop", methods=["POST"])
@handle_exceptions
@handle_missing_payload
def verify_closed_loop():
    authentication_commands.verify_closed_loop(
        user_id=request.json["user_id"],
        closed_loop_id=request.json["closed_loop_id"],
        unique_identifier_otp=request.json["unique_identifier_otp"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "Closed loop verified successfully",
            }
        ),
        200,
    )


# Get requests


@app.route(PREFIX + "/get-all-closed-loops", methods=["GET"])
@handle_exceptions
def get_all_closed_loops():
    """ """

    closed_loops = authentication_queries.get_all_closed_loops(uow=UnitOfWork())

    return (
        jsonify(
            {
                "success": True,
                "message": "All closed loops returned successfully",
                "closed_loops": closed_loops,
            }
        ),
        201,
    )


@app.route(PREFIX + "/decode-access-token", methods=["GET"])
@authenticate_token
def decode_access_token(uid):
    """Decode an access token"""

    return_obj = {"uid": uid}
    return jsonify(return_obj), 200


@app.route(PREFIX + "/get-user", methods=["GET"])
@handle_exceptions
@authenticate_token
def get_user(uid):
    user = authentication_queries.get_user_from_user_id(
        user_id=uid,
        uow=UnitOfWork(),
    )

    user.closed_loops = [c for c in user.closed_loops.values()]

    return (
        jsonify(
            {
                "success": True,
                "message": "User returned successfully",
                "user": user,
            }
        ),
        200,
    )


@app.route(PREFIX + "/get-user-balance", methods=["GET"])
@handle_exceptions
@authenticate_token
def get_user_balance(uid):
    balance = authentication_queries.get_user_balance(
        user_id=uid,
        uow=UnitOfWork(),
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "User balance returned successfully",
                "balance": balance,
            }
        ),
        200,
    )


@app.route(PREFIX + "/get-user-recent-transactions", methods=["GET"])
@handle_exceptions
@authenticate_token
def get_user_recent_transactions(uid):
    txs = payment_queries.get_all_transactions_of_a_user(
        user_id=uid,
        offset=0,
        page_size=50,
        uow=UnitOfWork(),
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "User recent transactions returned successfully",
                "recent_transactions": txs,
            }
        ),
        200,
    )


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


@app.route(PREFIX + "/create-deposit-request", methods=["POST"])
@handle_exceptions
@handle_missing_payload
@authenticate_token
def create_deposit_request(uid):
    checkout_url = payment_commands.create_deposit_request(
        user_id=uid,
        amount=request.json["amount"],
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "deposit request created successfully",
                "checkout_url": checkout_url,
            }
        ),
        201,
    )


@app.route(PREFIX + "/pay-pro-callback", methods=["POST"])
def pay_pro_callback():
    payment_commands.pay_pro_callback(
        uow=UnitOfWork(),
        data=request.json[""],  # TODO: fill these later
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


@app.route(PREFIX + "/execute-p2p-push-transaction", methods=["POST"])
@handle_exceptions
@handle_missing_payload
@authenticate_token
def execute_p2p_push_transaction(uid):
    unique_identifier = authentication_queries.get_unique_identifier_from_user_id(
        user_id=uid, uow=UnitOfWork()
    )
    payment_commands.execute_transaction_unique_identifier(
        sender_unique_identifier=unique_identifier,
        recipient_unique_identifier=request.json["recipient_unique_identifier"],
        amount=request.json["amount"],
        closed_loop_id=request.json["closed_loop_id"],
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "p2p push transaction executed successfully",
            }
        ),
        201,
    )


@app.route(PREFIX + "/create-p2p-pull-transaction", methods=["POST"])
@handle_exceptions
@handle_missing_payload
@authenticate_token
def create_p2p_pull_transaction(uid):
    unique_identifier = authentication_queries.get_unique_identifier_from_user_id(
        user_id=uid, uow=UnitOfWork()
    )
    payment_commands.execute_transaction_unique_identifier(
        sender_unique_identifier=request.json["sender_unique_identifier"],
        recipient_unique_identifier=unique_identifier,
        amount=request.json["amount"],
        closed_loop_id=request.json["closed_loop_id"],
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "p2p pull transaction created successfully",
            }
        ),
        201,
    )


@app.route(PREFIX + "/execute-transaction", methods=["POST"])
@handle_exceptions
@handle_missing_payload
def execute_transaction():
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
@handle_missing_payload
def accept_p2p_pull_transaction():
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
@handle_missing_payload
def decline_p2p_pull_transaction():
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
@handle_missing_payload
def generate_voucher():
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
@handle_missing_payload
def redeem_voucher():
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
@handle_missing_payload
def use_reference():
    marketing_commands.use_reference(
        referee_id=request.json["referee_id"],
        referral_id=request.json["referral_id"],
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
@handle_missing_payload
def add_weightage():
    marketing_commands.add_weightage(
        weightage_type=request.json["weightage_type"],
        weightage_value=request.json["weightage_value"],
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
@handle_missing_payload
def set_weightage():
    marketing_commands.set_weightage(
        weightage_type=request.json["weightage_type"],
        weightage_value=request.json["weightage_value"],
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
@handle_missing_payload
def set_cashback_slabs():
    cashback_slabs = request.json["cashback_slabs"]

    marketing_commands.set_cashback_slabs(
        cashback_slabs=cashback_slabs,
        uow=UnitOfWork(),
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "cashback slabs set successfully",
            }
        ),
        200,
    )


# retool auth admin routes


@app.route(PREFIX + "/get-all-closed-loops-with-user-counts", methods=["GET"])
@handle_exceptions
def get_all_closed_loops_with_user_counts():
    closed_loops = authentication_queries.get_all_closed_loops_with_user_counts(
        uow=UnitOfWork()
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "All closed loops returned successfully",
                "closed_loops": closed_loops,
            }
        ),
        201,
    )


@app.route(PREFIX + "/update-closed-loop", methods=["PUT"])
@handle_exceptions
@handle_missing_payload
def update_closed_loop():
    authentication_queries.update_closed_loop(
        closed_loop_id=request.json["id"],
        name=request.json["name"],
        logo_url=request.json["logo_url"],
        description=request.json["description"],
        verification_type=request.json["verification_type"],
        regex=request.json["regex"],
        uow=UnitOfWork(),
    )
    # print("hello")
    return (
        jsonify(
            {
                "success": True,
                "message": "closed loop updated successfully",
            }
        ),
        200,
    )


@app.route(PREFIX + "/get-active-inactive-counts-of-a-closed_loop", methods=["GET"])
@handle_exceptions
@handle_missing_payload
def get_active_inactive_counts_of_a_closed_loop():
    counts = authentication_queries.get_active_inactive_counts_of_a_closed_loop(
        closed_loop_id=request.json["closed_loop_id"],
        uow=UnitOfWork(),
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "All counts returned successfully",
                "counts": counts,
            }
        ),
        201,
    )


@app.route(PREFIX + "/get-all-users-of-a-closed-loop", methods=["GET"])
@handle_exceptions
@handle_missing_payload
def get_information_of_all_users_of_a_closed_loop():
    users = authentication_queries.get_information_of_all_users_of_a_closed_loop(
        closed_loop_id=request.json["closed_loop_id"],
        uow=UnitOfWork(),
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "All users returned successfully",
                "users": users,
            }
        ),
        201,
    )
