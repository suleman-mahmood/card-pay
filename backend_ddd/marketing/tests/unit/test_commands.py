from ...entrypoint.commands import (
    verify_user,
    use_reference,
    add_loyalty_points,
    give_cashback,
    add_weightage,
    set_weightage,
    set_cashback_slabs,
)
from ....entrypoint.uow import FakeUnitOfWork
from ....payment.domain.model import TransactionType
from ....authentication.tests.conftest import seed_auth_user

# User related commands are not tested because there is not a fake Marketing user repo 

# def test_use_reference(seed_auth_user):

#     uow = FakeUnitOfWork()
#     referee = seed_auth_user(uow=uow)
#     referral = seed_auth_user(uow=uow)
#     with uow:
#         use_reference(
#             referee_id=referee.id,
#             referral_id=referral.id,
#             uow=uow,
#         )
        
#         fetched_referee = uow.marketing_users.get(referee.id)

#         assert fetched_referee.referral_id == referral.id

def test_add_and_set_weightage():

    uow = FakeUnitOfWork()
    add_weightage(
        weightage_type= "PAYMENT_GATEWAY",
        weightage_value=10,
        uow=uow
    )
    with uow:
        set_weightage(
            weightage_type= "PAYMENT_GATEWAY",
            weightage_value=20,
            uow=uow,
        )

        fetched_weightage = uow.weightages.get(TransactionType.PAYMENT_GATEWAY)

        assert fetched_weightage.weightage_value == 20

def test_add_and_set_cashback_slabs():
     
    uow = FakeUnitOfWork()
    set_cashback_slabs(
        cashback_slabs= [[0,100,"PERCENTAGE",10],[100,200,"PERCENTAGE",20]],
        uow=uow,
    ) #Adding cashback slabs
    
    with uow:
        set_cashback_slabs(
            cashback_slabs= [[0,100,"PERCENTAGE",20],[100,200,"PERCENTAGE",30]],
            uow=uow,
        )

        fetched_cashback_slabs = uow.cashback_slabs.get_all()

        assert fetched_cashback_slabs[0].cashback_value == 20
