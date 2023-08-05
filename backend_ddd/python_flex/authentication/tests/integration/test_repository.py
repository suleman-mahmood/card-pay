import pytest
from ...adapters.repository import ClosedLoopRepository, UserRepository
from ...domain.model import (
    ClosedLoop,
    ClosedLoopVerificationType,
    UserType,
    User,
    PersonalEmail,
    PhoneNumber,
    Location,
)
from python_flex.entrypoint.uow import UnitOfWork
from ..conftest import seed_closed_loop, seed_auth_user
from uuid import uuid4
from datetime import datetime


def test_closed_loop_repository_add_get(seed_closed_loop):
    uow = UnitOfWork()

    with uow:
        closed_loop = seed_closed_loop()
        uow.closed_loops.add(closed_loop=closed_loop)
        fetched_closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop.id)
        assert fetched_closed_loop == closed_loop


def test_user_repository_add_get(seed_user):
    uow = UnitOfWork()

    with uow:
        uow.cursor.execute(
            "ALTER TABLE users DROP CONSTRAINT IF EXISTS users_wallet_id_fkey CASCADE;"
        )

        user = seed_user()
        uow.users.add(user=user)

        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user == user


def test_closed_loop_repository_save(seed_closed_loop):
    uow = UnitOfWork()

    with uow:
        closed_loop = seed_closed_loop()
        uow.closed_loops.add(closed_loop=closed_loop)
        fetched_closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop.id)

        assert fetched_closed_loop == closed_loop

        fetched_closed_loop.name = "Test Loop 2"
        uow.closed_loops.save(closed_loop=fetched_closed_loop)

        fetched_closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop.id)

        assert fetched_closed_loop.name == "Test Loop 2"


def test_user_repository_save(seed_user, seed_closed_loop):
    uow = UnitOfWork()

    with uow:
        uow.cursor.execute(
            "ALTER TABLE users DROP CONSTRAINT IF EXISTS users_wallet_id_fkey CASCADE;"
        )
        user = seed_user()

        uow.users.add(user=user)
        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user == user

        fetched_user.pin = "4321"

        uow.users.save(user=fetched_user)

        fetched_user = uow.users.get(user_id=user.id)

        assert fetched_user.pin == "4321"
