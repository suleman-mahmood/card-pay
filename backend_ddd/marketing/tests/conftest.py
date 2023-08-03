import pytest
from ..domain import model
from uuid import uuid4
from backend_ddd.entrypoint.uow import AbstractUnitOfWork
from backend_ddd.payment.entrypoint import commands as payment_commands
@pytest.fixture
def seed_user():
    def _seed_user() -> model.User:
        return model.User(
            id = str(uuid4())
        )
    
    return _seed_user

@pytest.fixture
def seed_starred_wallet():
    def _seed_starred_wallet(uow: AbstractUnitOfWork):
        with uow:
            user_id = str(uuid4())
            payment_commands.create_wallet(user_id=user_id, uow=uow)

            uow.transactions.add_1000_wallet(wallet_id=user_id)

            delete_sql = """
                delete from starred_wallet_id
            """
            uow.cursor.execute(delete_sql)

            sql = """
                insert into starred_wallet_id
                values (%s)
            """
            uow.cursor.execute(sql, [user_id])  
    
    return _seed_starred_wallet

# @pytest.fixture
# def seed_weightage():
#     def _seed_weightage() -> model.Weightage:
#         return model.Weightage()
    
#     return _seed_weightage