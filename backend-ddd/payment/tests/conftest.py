from uuid import uuid4
from typing import Tuple
import pytest
from ..domain.model import User, Wallet, UserType


@pytest.fixture
def seed_user():
    def _seed_user() -> User:
        return User(
            id=str(uuid4()),
            wallet=Wallet(id=uuid4(), qr_code='https://cardpay.com.pk', pin='1234'),
            phone_number="03034952255",
            email="mlkmoaz@gmail.com",
            full_name="Malik M. Moaz",
            user_type=UserType.CUSTOMER,
        )

    return _seed_user


@pytest.fixture
def seed_user_wallet(seed_user):
    def _seed_user_wallet() -> Tuple[User, Wallet]:
        user = seed_user()
        return user, user.wallet

    return _seed_user_wallet


@pytest.fixture
def seed_payment_gateway():
    return "PAYPRO", str(uuid4())
