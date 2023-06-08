from uuid import uuid4
from typing import Tuple
import pytest
from ..domain.model import User, Wallet, UserType


@pytest.fixture
def seed_user_wallet():
    def _seed_user_wallet() -> Tuple[User, Wallet]:
        wallet = Wallet()
        user = User(
            id=str(uuid4()),
            wallet_id=wallet.id,
            qr_code="https://cardpay.com.pk",
            pin="1234",
            phone_number="03034952255",
            email="mlkmoaz@gmail.com",
            full_name="Malik M. Moaz",
            user_type=UserType.CUSTOMER,
        )

        return user, wallet

    return _seed_user_wallet


@pytest.fixture
def seed_wallet():
    def _seed_wallet() -> Wallet:
        return Wallet()

    return _seed_wallet
