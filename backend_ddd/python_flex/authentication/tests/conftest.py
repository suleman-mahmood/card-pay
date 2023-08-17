"""Fixtures for seeding data for tests."""
import pytest
from ..domain.model import (
    User,
    UserType,
    PersonalEmail,
    PhoneNumber,
    ClosedLoop,
    ClosedLoopVerificationType,
    Location,
)
from uuid import uuid4
from python_flex.payment.domain import model as payment_model
from python_flex.entrypoint.uow import AbstractUnitOfWork
from python_flex.authentication.entrypoint import commands as auth_commands


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
            location=Location(latitude=0, longitude=0),
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
            regex="No regex yet",
            verification_type=ClosedLoopVerificationType.ROLLNUMBER,
        )

    return _seed_closed_loop


@pytest.fixture
def seed_auth_user():
    def _seed_auth_user(uow: AbstractUnitOfWork) -> User:
        user_id = str(uuid4())
        user = User(
            id=user_id,
            personal_email=PersonalEmail(value="mlkmoaz@gmail.com"),
            phone_number=PhoneNumber(value="03034952255"),
            user_type=UserType.CUSTOMER,
            pin="1234",
            full_name="Malik Muhammad Moaz",
            location=Location(latitude=0, longitude=0),
            wallet_id=user_id,
        )

        with uow:
            uow.transactions.add_wallet(wallet=payment_model.Wallet(id=user_id))
            uow.users.add(user)

        return user

    return _seed_auth_user


@pytest.fixture
def seed_verified_auth_user(seed_auth_user):
    def _seed_auth_user(uow: AbstractUnitOfWork) -> User:
        user = seed_auth_user(uow)
        auth_commands.verify_phone_number(
            user_id=user.id,
            otp=user.otp,
            uow=uow,
        )
        return user

    return _seed_auth_user


@pytest.fixture
def seed_auth_closed_loop():
    def _seed_auth_closed_loop(uow: AbstractUnitOfWork) -> ClosedLoop:
        return auth_commands.create_closed_loop(
            name="Test Closed Loop",
            logo_url="https://test.com/logo.png",
            description="Test description",
            regex="No regex yet",
            verification_type="NONE",
            uow=uow,
        )

    return _seed_auth_closed_loop