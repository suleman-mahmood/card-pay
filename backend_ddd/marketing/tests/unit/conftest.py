import pytest
from ...domain.model import (User,Vendor,)

@pytest.fixture
def seed_user():
    def _seed_user() -> User:
        return User()
    
    return _seed_user

@pytest.fixture
def seed_vendor():
    def _seed_vendor() -> Vendor:
        return Vendor()
    
    return _seed_vendor

