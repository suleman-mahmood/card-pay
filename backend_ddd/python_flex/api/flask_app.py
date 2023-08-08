# from dataclasses import asdict

import firebase_admin

from flask import Flask, request, jsonify

from python_flex.api.utils import (
    handle_exceptions,
    handle_missing_payload,
    authenticate_token,
)
from python_flex.entrypoint.uow import UnitOfWork
from python_flex.payment.entrypoint import commands as payment_commands
from python_flex.payment.domain.model import (
    TransactionMode,
    TransactionType,
)
from python_flex.authentication.entrypoint import queries as authentication_queries
from python_flex.marketing.entrypoint import commands as marketing_commands
from python_flex.authentication.entrypoint import commands as authentication_commands
from python_flex.payment.entrypoint import queries as payment_queries

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
    req = request.get_json(force=True)

    authentication_commands.create_user(
        personal_email=req["personal_email"],
        password=req["password"],
        phone_number=req["phone_number"],
        user_type=req["user_type"],
        full_name=req["full_name"],
        location=req["location"],
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
    req = request.get_json(force=True)

    event_code, user_id = authentication_commands.create_user(
        personal_email=req["personal_email"],
        password=req["password"],
        phone_number=req["phone_number"],
        user_type="CUSTOMER",
        full_name=req["full_name"],
        location=req["location"],
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
    req = request.get_json(force=True)

    authentication_commands.create_closed_loop(
        name=req["name"],
        logo_url=req["logo_url"],
        description=req["description"],
        verification_type=req["verification_type"],
        regex=req["regex"],
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
    req = request.get_json(force=True)

    authentication_commands.change_name(
        user_id=req["user_id"],
        new_name=req["new_name"],
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
    req = request.get_json(force=True)

    authentication_commands.change_pin(
        user_id=req["user_id"],
        new_pin=req["new_pin"],
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
    req = request.get_json(force=True)

    authentication_commands.user_toggle_active(
        user_id=req["user_id"],
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
    req = request.get_json(force=True)

    authentication_commands.verify_otp(
        user_id=req["user_id"],
        otp=req["otp"],
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
    req = request.get_json(force=True)

    authentication_commands.verify_phone_number(
        user_id=req["user_id"],
        otp=req["otp"],
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
    req = request.get_json(force=True)

    authentication_commands.register_closed_loop(
        user_id=req["user_id"],
        closed_loop_id=req["closed_loop_id"],
        unique_identifier=req["unique_identifier"],
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
    req = request.get_json(force=True)

    authentication_commands.verify_closed_loop(
        user_id=req["user_id"],
        closed_loop_id=req["closed_loop_id"],
        unique_identifier_otp=req["unique_identifier_otp"],
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
# @app.route(PREFIX + "/create-test-wallet", methods=["POST"])
# @handle_exceptions
# def create_test_wallet():
#     req = request.get_json(force=True)

#     with UnitOfWork() as uow:
#         payment_commands.create_wallet(uow=uow)

#     return {
#         "success": True,
#         "message": "test wallet created successfully (only call me from create_user though)",
#     }, 200


@app.route(PREFIX + "/create-deposit-request", methods=["POST"])
@handle_exceptions
@handle_missing_payload
@authenticate_token
def create_deposit_request(uid):
    req = request.get_json(force=True)

    checkout_url = payment_commands.create_deposit_request(
        user_id=uid,
        amount=req["amount"],
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
    req = request.get_json(force=True)

    payment_commands.pay_pro_callback(
        uow=UnitOfWork(),
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


@app.route(PREFIX + "/execute-p2p-push-transaction", methods=["POST"])
@handle_exceptions
@handle_missing_payload
@authenticate_token
def execute_p2p_push_transaction(uid):
    req = request.get_json(force=True)

    unique_identifier = authentication_queries.get_unique_identifier_from_user_id(
        user_id=uid, uow=UnitOfWork()
    )
    payment_commands.execute_transaction_unique_identifier(
        sender_unique_identifier=unique_identifier,
        recipient_unique_identifier=req["recipient_unique_identifier"],
        amount=req["amount"],
        closed_loop_id=req["closed_loop_id"],
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
    req = request.get_json(force=True)

    unique_identifier = authentication_queries.get_unique_identifier_from_user_id(
        user_id=uid, uow=UnitOfWork()
    )
    payment_commands.execute_transaction_unique_identifier(
        sender_unique_identifier=req["sender_unique_identifier"],
        recipient_unique_identifier=unique_identifier,
        amount=req["amount"],
        closed_loop_id=req["closed_loop_id"],
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
    req = request.get_json(force=True)

    payment_commands.execute_transaction(
        sender_wallet_id=req["sender_wallet_id"],
        recipient_wallet_id=req["recipient_wallet_id"],
        amount=req["amount"],
        transaction_mode=TransactionMode.__members__[req["transaction_mode"]],
        transaction_type=TransactionType.__members__[req["transaction_type"]],
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
    req = request.get_json(force=True)

    payment_commands.accept_p2p_pull_transaction(
        transaction_id=req["transaction_id"],
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
    req = request.get_json(force=True)

    payment_commands.decline_p2p_pull_transaction(
        transaction_id=req["transaction_id"],
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
    req = request.get_json(force=True)

    payment_commands.generate_voucher(
        sender_wallet_id=req["sender_wallet_id"],
        amount=req["amount"],
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
    req = request.get_json(force=True)

    payment_commands.redeem_voucher(
        recipient_wallet_id=req["recipient_wallet_id"],
        transaction_id=req["transaction_id"],
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
    req = request.get_json(force=True)

    marketing_commands.use_reference(
        referee_id=req["referee_id"],
        referral_id=req["referral_id"],
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
    req = request.get_json(force=True)

    marketing_commands.add_weightage(
        weightage_type=req["weightage_type"],
        weightage_value=req["weightage_value"],
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
    req = request.get_json(force=True)
    
    marketing_commands.set_weightage(
        weightage_type=req["weightage_type"],
        weightage_value=req["weightage_value"],
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
    req = request.get_json(force=True)

    cashback_slabs = req["cashback_slabs"]

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
    req = request.get_json(force=True)

    authentication_queries.update_closed_loop(
        closed_loop_id=req["id"],
        name=req["name"],
        logo_url=req["logo_url"],
        description=req["description"],
        verification_type=req["verification_type"],
        regex=req["regex"],
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
    req = request.get_json(force=True)

    counts = authentication_queries.get_active_inactive_counts_of_a_closed_loop(
        closed_loop_id=req["closed_loop_id"],
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
    req = request.get_json(force=True)
    
    users = authentication_queries.get_information_of_all_users_of_a_closed_loop(
        closed_loop_id=req["closed_loop_id"],
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
