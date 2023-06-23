import pytest
from ....entrypoint.uow import UnitOfWork
from ....authentication.entrypoint.commands import create_user
from ...domain.model import (User, Weightage, CashbackSlab,)
from ....authentication.domain.model import Location
from ...adapters.repository import (MarketingUserRepository, WeightageRepository, CashbackSlabRepository,)
from uuid import uuid4

def test_marketing_user_repository_add_get():
    uow = UnitOfWork()
    #Use Authentication command to create a user first, then use marketing command to fill the 4 marketing related columns in the users table
    with uow:
        # function that creates a user given a uow and user id
        user_id = str(uuid4())
        create_user(
            user_id = user_id,
            personal_email = "shaheer@shaheer.com",
            phone_number = "1234567890",
            user_type = "CUSTOMER",
            pin = "1234",
            full_name = "Shaheer",
            location= Location(latitude=0, longitude=0),
            uow = uow
        )
        user = User(
            id = user_id,
            loyalty_points=0,
            referral_id = "",
            marketing_user_verified=False,
        )
        uow.marketing_users.save(user)
        
        fetched_user = uow.marketing_users.get(id=user_id)

        assert fetched_user == user

