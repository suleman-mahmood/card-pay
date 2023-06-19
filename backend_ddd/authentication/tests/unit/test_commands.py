"""Unit tests for commands."""
import pytest
from ...entrypoint.commands import (
    create_closed_loop,
    create_user,
    change_name,
    change_pin,
    user_toggle_active,
    verify_otp,
    verify_phone_number,
    register_closed_loop,
    verify_closed_loop,
)
from ....entrypoint.uow import FakeUnitOfWork
from ...domain.model import ClosedLoopVerificationType, ClosedLoopUserState, UserType
from uuid import uuid4
from copy import deepcopy
from ...domain.exceptions import InvalidOtpException, VerificationException


def test_create_closed_loop(seed_auth_closed_loop):
    with FakeUnitOfWork() as uow:
        closed_loop = seed_auth_closed_loop(uow)

        fetched_closed_loop = uow.closed_loops.get(closed_loop.id)

        assert fetched_closed_loop == closed_loop


def test_create_user(seed_auth_user):
    with FakeUnitOfWork() as uow:
        user = seed_auth_user(uow)

        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user == user


def test_change_name(seed_auth_user):
    with FakeUnitOfWork() as uow:
        user = seed_auth_user(uow)
        change_name(user_id=user.id, new_name="Malik Moaz", uow=uow)
        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user.id == user.id
        assert fetched_user.full_name == "Malik Moaz"


def test_change_pin(seed_auth_user):
    with FakeUnitOfWork() as uow:
        user = seed_auth_user(uow)
        change_pin(user_id=user.id, new_pin="5678", uow=uow)
        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user.id == user.id
        assert fetched_user.pin == "5678"


def test_user_toggle_active(seed_auth_user):
    with FakeUnitOfWork() as uow:
        user = deepcopy(seed_auth_user(uow))
        user_toggle_active(user_id=user.id, uow=uow)
        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user.id == user.id
        assert fetched_user.is_active == (not user.is_active)


def test_verify_otp(seed_auth_user):
    with FakeUnitOfWork() as uow:
        user = seed_auth_user(uow)
        otp = user.otp
        wrong_otp = "0000"

        with pytest.raises(InvalidOtpException, match="Otps don't match"):
            verify_otp(user_id=user.id, otp=wrong_otp, uow=uow)
        assert verify_otp(user_id=user.id, otp=otp, uow=uow)
        with pytest.raises(InvalidOtpException):
            verify_otp(user_id=user.id, otp=otp, uow=uow)


def test_verify_phone_number(seed_auth_user):
    with FakeUnitOfWork() as uow:
        user = seed_auth_user(uow)
        otp = user.otp

        assert verify_phone_number(user_id=user.id, otp=otp, uow=uow)
        with pytest.raises(VerificationException):
            verify_phone_number(user_id=user.id, otp=otp, uow=uow)


def test_register_closed_loop(seed_auth_user, seed_auth_closed_loop):
    with FakeUnitOfWork() as uow:
        user = seed_auth_user(uow)
        closed_loop = seed_auth_closed_loop(uow)

        fetched_user = uow.users.get(user_id=user.id)

        register_closed_loop(
            user_id=fetched_user.id,
            closed_loop_id=closed_loop.id,
            unique_identifier=None,
            uow=uow,
        )

        fetched_user = uow.users.get(user_id=user.id)

        assert (
            fetched_user.closed_loops[closed_loop.id].status
            == ClosedLoopUserState.VERIFIED
        )
        assert len(fetched_user.closed_loops) == 1


def test_verify_closed_loop(seed_auth_user, seed_auth_closed_loop):
    with FakeUnitOfWork() as uow:
        user = seed_auth_user(uow)
        closed_loop = seed_auth_closed_loop(uow)

        fetched_user = uow.users.get(user_id=user.id)

        registered_user = register_closed_loop(
            user_id=fetched_user.id,
            closed_loop_id=closed_loop.id,
            unique_identifier="24100163",
            uow=uow,
        )

        assert (
            registered_user.closed_loops[closed_loop.id].status
            == ClosedLoopUserState.UN_VERIFIED
        )

        otp = user.closed_loops[closed_loop.id].unique_identifier_otp

        with pytest.raises(InvalidOtpException):
            verify_closed_loop(
                user_id=user.id,
                closed_loop_id=closed_loop.id,
                unique_identifier_otp="0000",
                uow=uow,
            )

        fetched_user = uow.users.get(user_id=user.id)
        assert (
            fetched_user.closed_loops[closed_loop.id].status
            == ClosedLoopUserState.UN_VERIFIED
        )

        verified_user = verify_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop.id,
            unique_identifier_otp=otp,
            uow=uow,
        )

        assert (
            verified_user.closed_loops[closed_loop.id].status
            == ClosedLoopUserState.VERIFIED
        )
