import pytest
from ...domain.model import (User, Weightage,)
from uuid import uuid4

@pytest.fixture
def seed_user():
    def _seed_user() -> User:
        return User(
            id = str(uuid4())
        )
    
    return _seed_user

@pytest.fixture
def seed_weightage():
    def _seed_weightage() -> Weightage:
        return Weightage()
    
    return _seed_weightage