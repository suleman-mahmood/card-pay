import pytest
from core.authentication.tests.conftest import (
    seed_auth_user,
    seed_verified_auth_user,
    seed_auth_closed_loop,
)
from core.entrypoint.uow import UnitOfWork
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import exceptions as auth_exc
from core.api import view_models as vm


def test_get_user_checkpoint(seed_verified_auth_user, seed_auth_closed_loop):
    uow = UnitOfWork()
    user = seed_verified_auth_user(uow=uow)
    closed_loop = seed_auth_closed_loop(uow=uow)

    assert auth_qry.user_checkpoints(user_id=user.id, uow=uow) == vm.CheckpointsDTO(
        verified_phone_otp=True, verified_closed_loop=False, pin_setup=False
    )

    auth_cmd.change_pin(user_id=user.id, new_pin="1234", uow=uow)

    assert auth_qry.user_checkpoints(user_id=user.id, uow=uow) == vm.CheckpointsDTO(
        verified_phone_otp=True, verified_closed_loop=False, pin_setup=True
    )

    auth_cmd.register_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop.id,
        unique_identifier="1234",
        uow=uow,
    )

    user = uow.users.get(user_id=user.id)
    otp = user.closed_loops[closed_loop.id].unique_identifier_otp
    auth_cmd.verify_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop.id,
        unique_identifier_otp=otp,
        ignore_migration=False,
        uow=uow,
    )
    checkpoint = auth_qry.user_checkpoints(user_id=user.id, uow=uow)
    uow.close_connection()

    assert checkpoint == vm.CheckpointsDTO(
        verified_phone_otp=True, verified_closed_loop=True, pin_setup=True
    )


def test_get_full_name_from_unique_identifier_and_closed_loop(
    seed_verified_auth_user, seed_auth_closed_loop
):
    uow = UnitOfWork()
    user = seed_verified_auth_user(uow=uow)
    closed_loop = seed_auth_closed_loop(uow=uow)

    auth_cmd.register_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop.id,
        unique_identifier="1234",
        uow=uow,
    )

    assert (
        auth_qry.get_full_name_from_unique_identifier_and_closed_loop(
            unique_identifier="1234", closed_loop_id=closed_loop.id, uow=uow
        )
        == "Malik Muhammad Moaz"
    )

    with pytest.raises(auth_exc.UserNotFoundException, match="user not found"):
        auth_qry.get_full_name_from_unique_identifier_and_closed_loop(
            unique_identifier="1235", closed_loop_id=closed_loop.id, uow=uow
        )
