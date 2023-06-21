"""Fixtures for seeding data for tests."""
import pytest
from ..domain.model import (
    User,
    UserType,
    PersonalEmail,
    PhoneNumber,
    ClosedLoop,
    ClosedLoopVerificationType,
)
from uuid import uuid4
from backend_ddd.entrypoint.uow import AbstractUnitOfWork
from backend_ddd.authentication.entrypoint import commands as auth_commands


@pytest.fixture
def seed_user():
    def _seed_user() -> User:
        return User(
            id=str(uuid4()),
            personal_email=PersonalEmail(value="sulemanmahmood99@gmail.com"),
            user_type=UserType.CUSTOMER,
            phone_number=PhoneNumber(value="+923000000000"),
            pin="1234",
            full_name="Suleman Mahmood",
            location=(0, 0),
            wallet_id=str(uuid4()),
        )

    return _seed_user


@pytest.fixture
def seed_closed_loop():
    def _seed_closed_loop() -> ClosedLoop:
        return ClosedLoop(
            id=str(uuid4()),
            name="Test Loop",
            logo_url="https://www.google.com",
            description="This is a test loop.",
            regex=None,
            verification_type=ClosedLoopVerificationType.ROLLNUMBER,
        )

    return _seed_closed_loop


@pytest.fixture
def seed_auth_user():
    def _seed_auth_user(uow: AbstractUnitOfWork) -> User:
        return auth_commands.create_user(
            user_id=str(uuid4()),
            personal_email="mlkmoaz@gmail.com",
            phone_number="03034952255",
            user_type="CUSTOMER",
            pin="1234",
            full_name="Malik Muhammad Moaz",
            location=(0, 0),
            uow=uow,
        )

    return _seed_auth_user


@pytest.fixture
def seed_auth_closed_loop():
    def _seed_auth_closed_loop(uow: AbstractUnitOfWork) -> ClosedLoop:
        return auth_commands.create_closed_loop(
            name="Test Closed Loop",
            logo_url="https://test.com/logo.png",
            description="Test description",
            regex=None,
            verification_type="NONE",
            uow=uow,
        )

    return _seed_auth_closed_loop
