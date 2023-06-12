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
            verification_type=ClosedLoopVerificationType.ROLLNUMBER,
        )

    return _seed_closed_loop
