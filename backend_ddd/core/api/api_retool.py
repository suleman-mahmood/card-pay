from flask import Blueprint, request, jsonify

from core.api.utils import (
    authenticate_token,
    authenticate_user_type,
    handle_exceptions_uow,
    handle_missing_payload,
    validate_json_payload,
)

from core.authentication.entrypoint import queries as authentication_queries
from core.authentication.domain.model import UserType
from core.marketing.entrypoint import commands as marketing_commands
from core.authentication.entrypoint import commands as authentication_commands
from core.payment.entrypoint import queries as payment_queries

retool = Blueprint("retool", __name__, url_prefix="/api/v1")


@retool.route("/get-user-recent-transactions", methods=["GET"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
def get_user_recent_transactions(uid, uow):
    txs = payment_queries.get_all_transactions_of_a_user(
        user_id=uid,
        offset=0,
        page_size=50,
        uow=uow,
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


@retool.route("/get-all-closed-loops", methods=["GET"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
def get_all_closed_loops(uow):
    """ """

    closed_loops = authentication_queries.get_all_closed_loops(uow=uow)

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


@retool.route("/decode-access-token", methods=["GET"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
def decode_access_token(uid):
    """Decode an access token"""

    return_obj = {"uid": uid}
    return jsonify(return_obj), 200


@retool.route("/get-user", methods=["GET"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
def get_user(uid, uow):
    user = authentication_queries.get_user_from_user_id(
        user_id=uid,
        uow=uow,
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


@retool.route("/get-user-balance", methods=["GET"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
def get_user_balance(uid, uow):
    balance = authentication_queries.get_user_balance(
        user_id=uid,
        uow=uow,
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


@retool.route("/create-closed-loop", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_missing_payload
@handle_exceptions_uow
def create_closed_loop(uow):
    req = request.get_json(force=True)

    authentication_commands.create_closed_loop(
        name=req["name"],
        logo_url=req["logo_url"],
        description=req["description"],
        verification_type=req["verification_type"],
        regex=req["regex"],
        uow=uow,
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


@retool.route("/add-weightage", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["weightage_type", "weightage_value"])
def add_weightage(uow):
    req = request.get_json(force=True)

    marketing_commands.add_weightage(
        weightage_type=req["weightage_type"],
        weightage_value=req["weightage_value"],
        uow=uow,
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


@retool.route("/set-weightage", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["weightage_type", "weightage_value"])
def set_weightage(uow):
    req = request.get_json(force=True)

    marketing_commands.set_weightage(
        weightage_type=req["weightage_type"],
        weightage_value=req["weightage_value"],
        uow=uow,
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


@retool.route("/set-cashback-slabs", methods=["POST"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["cashback_slabs"])
def set_cashback_slabs(uow):
    req = request.get_json(force=True)

    cashback_slabs = req["cashback_slabs"]

    marketing_commands.set_cashback_slabs(
        cashback_slabs=cashback_slabs,
        uow=uow,
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


@retool.route("/get-all-closed-loops-with-user-counts", methods=["GET"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
def get_all_closed_loops_with_user_counts(uow):
    closed_loops = authentication_queries.get_all_closed_loops_with_user_counts(uow=uow)

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


@retool.route("/update-closed-loop", methods=["PUT"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["id", "name", "logo_url", "description", "verification_type", "regex"])
def update_closed_loop(uow):
    req = request.get_json(force=True)

    authentication_queries.update_closed_loop(
        closed_loop_id=req["id"],
        name=req["name"],
        logo_url=req["logo_url"],
        description=req["description"],
        verification_type=req["verification_type"],
        regex=req["regex"],
        uow=uow,
    )
    return (
        jsonify(
            {
                "success": True,
                "message": "closed loop updated successfully",
            }
        ),
        200,
    )


@retool.route("/get-active-inactive-counts-of-a-closed_loop", methods=["GET"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["closed_loop_id"])
def get_active_inactive_counts_of_a_closed_loop(uow):
    req = request.get_json(force=True)

    counts = authentication_queries.get_active_inactive_counts_of_a_closed_loop(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
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


@retool.route("/get-all-users-of-a-closed-loop", methods=["GET"])
@authenticate_token
@authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@handle_exceptions_uow
@handle_missing_payload
@validate_json_payload(required_parameters = ["closed_loop_id"])
def get_information_of_all_users_of_a_closed_loop(uow):
    req = request.get_json(force=True)

    users = authentication_queries.get_information_of_all_users_of_a_closed_loop(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
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
