from copy import deepcopy
from uuid import uuid4

import pytest
from core.authentication.domain import model as auth_mdl
from core.entrypoint.uow import AbstractUnitOfWork
from core.marketing.domain import model as mdl
from core.payment.entrypoint import commands as payment_commands


@pytest.fixture
def seed_user():
    def _seed_user() -> mdl.User:
        return mdl.User(id=str(uuid4()))

    return _seed_user


@pytest.fixture
def seed_starred_wallet():
    def _seed_starred_wallet(uow: AbstractUnitOfWork):
        user_id = str(uuid4())

        user = auth_mdl.User(
            id=user_id,
            personal_email=auth_mdl.PersonalEmail(value="mlkmoaz@gmail.com"),
            phone_number=auth_mdl.PhoneNumber(value="03269507423"),
            user_type=auth_mdl.UserType.CUSTOMER,
            pin="1234",
            full_name="CardPay",
            location=auth_mdl.Location(latitude=0, longitude=0),
            wallet_id=user_id,
            is_phone_number_verified=True,
            public_key=bytes(),
            private_key=bytes()
        )

        payment_commands.create_wallet(user_id=user_id, uow=uow)
        uow.users.add(user)

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
        return user_id

    return _seed_starred_wallet


# @pytest.fixture
# def seed_weightage():
#     def _seed_weightage() -> model.Weightage:
#         return model.Weightage()

#     return _seed_weightage


@pytest.fixture
def seed_marketing_user():
    def _seed_marketing_user(uow: AbstractUnitOfWork) -> mdl.User:
        user = mdl.User(id=str(uuid4()), marketing_user_verified=True)
        uow.marketing_users.save(user=user)
        return deepcopy(user)

    return _seed_marketing_user
