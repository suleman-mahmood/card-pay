import pytest
from ....entrypoint.uow import UnitOfWork, AbstractUnitOfWork
from ....authentication.entrypoint import commands as authentication_commands
from ...domain.model import (User, Weightage, CashbackSlab, CashbackType,)
from ....authentication.domain.model import Location, PersonalEmail, PhoneNumber, UserType
from ....authentication.domain.model import User as AuthenticationUser
from ....payment.entrypoint import commands as payment_commands
from ....payment.domain.model import TransactionType
from ...adapters.repository import (MarketingUserRepository, WeightageRepository, CashbackSlabRepository,)
from uuid import uuid4

def _create_authentication_user(uow: AbstractUnitOfWork):
    user_id = str(uuid4())
    wallet = payment_commands.create_wallet(uow)
    authentication_user = AuthenticationUser(
        id = user_id,
        personal_email = PersonalEmail(value = "asdasd@asdasd.com"),
        phone_number = PhoneNumber(value = "1234567890"),
        user_type = UserType.CUSTOMER,
        pin = "1234",
        full_name = "asdasd",
        wallet_id = wallet.id,
        location = Location(latitude = 1.0, longitude = 1.0),
    )
    uow.users.add(authentication_user)
    
    return authentication_user


def test_marketing_user_repository_add_get_save():
    uow = UnitOfWork()
    #Use Authentication command to create a user first, then use marketing command to fill the 4 marketing related columns in the users table
    with uow:
        
        #create a user (authentication)
        authentication_user = _create_authentication_user(uow)            

        marketing_user = User(
            id = authentication_user.id,
            loyalty_points=0,
            referral_id = str(uuid4()),
            marketing_user_verified=False,
        )
        uow.marketing_users.save(marketing_user)
        
        fetched_user = uow.marketing_users.get(id = marketing_user.id)

        assert fetched_user == marketing_user

        marketing_user.loyalty_points = 100
        uow.marketing_users.save(marketing_user)

        fetched_user = uow.marketing_users.get(id = marketing_user.id)

        assert fetched_user == marketing_user


def test_weightage_repository_add_get_save():
   
    uow = UnitOfWork()
    with uow:
        weightage = Weightage(
            weightage_type= TransactionType.REFERRAL,
            weightage_value= 10,
        )

        uow.weightages.save(weightage)
        fetched_weightage = uow.weightages.get(id = weightage.id)
        assert fetched_weightage == weightage

        weightage.weightage_value = 20
        uow.weightages.save(weightage)
        fetched_weightage = uow.weightages.get(id = weightage.id)
        assert fetched_weightage == weightage

def test_cashback_slab_repository_add_get_save():
    uow = UnitOfWork()
    with uow:
        cashback_slab = CashbackSlab(
            start_amount= 0,
            end_amount= 100,
            cashback_type= CashbackType.PERCENTAGE,
            cashback_value= 10,
        )

        uow.cashback_slabs.save(cashback_slab)
        fetched_cashback_slab = uow.cashback_slabs.get(id = cashback_slab.id)
        assert fetched_cashback_slab == cashback_slab

        cashback_slab.cashback_value = 20
        uow.cashback_slabs.save(cashback_slab)
        fetched_cashback_slab = uow.cashback_slabs.get(id = cashback_slab.id)
        assert fetched_cashback_slab == cashback_slab