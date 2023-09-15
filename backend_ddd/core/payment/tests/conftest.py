import pytest
from ..domain.model import Wallet
from uuid import uuid4

@pytest.fixture
def seed_wallet():
    def _seed_wallet() -> Wallet:
        return Wallet(id=str(uuid4()), qr_id=str(uuid4()), balance=0 )

    return _seed_wallet

    
