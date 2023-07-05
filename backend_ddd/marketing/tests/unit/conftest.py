import pytest
from ...domain import model
from uuid import uuid4

@pytest.fixture
def seed_user():
    def _seed_user() -> model.User:
        return model.User(
            id = str(uuid4())
        )
    
    return _seed_user

# @pytest.fixture
# def seed_weightage():
#     def _seed_weightage() -> model.Weightage:
#         return model.Weightage()
    
#     return _seed_weightage