import pytest
from ..domain.model import Wallet


@pytest.fixture
def seed_wallet():
    def _seed_wallet() -> Wallet:
        return Wallet()

    return _seed_wallet

    
