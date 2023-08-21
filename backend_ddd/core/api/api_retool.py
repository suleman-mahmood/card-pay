from flask import Blueprint, request

from core.api import utils
from core.entrypoint.uow import UnitOfWork
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.domain.model import UserType
from core.marketing.entrypoint import commands as mktg_cmd
from core.authentication.entrypoint import commands as auth_cmd
from core.marketing.domain import exceptions as mktg_ex

retool = Blueprint("retool", __name__, url_prefix="/api/v1")


@retool.route("/get-all-closed-loops", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.ADMIN])
def get_all_closed_loops():
    """get all closed loops of a user"""

    uow = UnitOfWork()
    closed_loops = auth_qry.get_all_closed_loops(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All closed loops returned successfully",
        status_code=201,
        data=closed_loops,
    )


@retool.route("/create-closed-loop", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_json_payload(
    required_parameters=[
        "name",
        "logo_url",
        "description",
        "verification_type",
        "regex",
    ]
)
def create_closed_loop():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    auth_cmd.create_closed_loop(
        name=req["name"],
        logo_url=req["logo_url"],
        description=req["description"],
        verification_type=req["verification_type"],
        regex=req["regex"],
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="Closed loop created successfully",
        status_code=201,
    )


@retool.route("/add-weightage", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["weightage_type", "weightage_value"])
def add_weightage():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    mktg_cmd.add_weightage(
        weightage_type=req["weightage_type"],
        weightage_value=req["weightage_value"],
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="weightage added successfully",
        status_code=200,
    )


@retool.route("/set-weightage", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["weightage_type", "weightage_value"])
def set_weightage():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    try:
        mktg_cmd.set_weightage(
            weightage_type=req["weightage_type"],
            weightage_value=req["weightage_value"],
            uow=uow,
        )
        uow.commit_close_connection()
    except mktg_ex.InvalidWeightageException as e:
        uow.close_connection()
        raise utils.Tabist(
            message=str(e),
            status_code=400,
        )

    return utils.Response(
        message="weightage set successfully",
        status_code=200,
    )


@retool.route("/set-cashback-slabs", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["cashback_slabs"])
def set_cashback_slabs():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    cashback_slabs = req["cashback_slabs"]
    try:
        mktg_cmd.set_cashback_slabs(
            cashback_slabs=cashback_slabs,
            uow=uow,
        )
        uow.commit_close_connection()
    except mktg_ex.InvalidSlabException as e:
        uow.close_connection()
        raise utils.Tabist(
            message=str(e),
            status_code=400,
        )

    return utils.Response(
        message="cashback slabs set successfully",
        status_code=200,
    )


# retool auth admin routes


@retool.route("/get-all-closed-loops-with-user-counts", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.ADMIN])
def get_all_closed_loops_with_user_counts():
    uow = UnitOfWork()
    closed_loops = auth_qry.get_all_closed_loops_with_user_counts(uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All closed loops returned successfully",
        status_code=201,
        data=closed_loops,
    )


@retool.route("/update-closed-loop", methods=["PUT"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_json_payload(
    required_parameters=[
        "id",
        "name",
        "logo_url",
        "description",
        "verification_type",
        "regex",
    ]
)
def update_closed_loop():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    auth_qry.update_closed_loop(
        closed_loop_id=req["id"],
        name=req["name"],
        logo_url=req["logo_url"],
        description=req["description"],
        verification_type=req["verification_type"],
        regex=req["regex"],
        uow=uow,
    )
    uow.commit_close_connection()

    return utils.Response(
        message="Closed loop updated successfully",
        status_code=200,
    )


@retool.route("/get-active-inactive-counts-of-a-closed_loop", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["closed_loop_id"])
def get_active_inactive_counts_of_a_closed_loop():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    counts = auth_qry.get_active_inactive_counts_of_a_closed_loop(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
    )
    uow.close_connection()

    response = utils.Response(
        message="Counts returned successfully",
        status_code=201,
        data=counts,
    )

    return response


@retool.route("/get-all-users-of-a-closed-loop", methods=["GET"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[UserType.ADMIN])
@utils.handle_missing_payload
@utils.validate_json_payload(required_parameters=["closed_loop_id"])
def get_information_of_all_users_of_a_closed_loop():
    req = request.get_json(force=True)

    uow = UnitOfWork()
    users = auth_qry.get_information_of_all_users_of_a_closed_loop(
        closed_loop_id=req["closed_loop_id"],
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All users returned successfully",
        status_code=201,
        data=users,
    )
