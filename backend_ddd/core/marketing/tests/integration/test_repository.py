import pytest
from core.entrypoint.uow import UnitOfWork
from core.marketing.domain import model as mdl
from core.payment.domain import model as pmt_mdl


def test_marketing_user_repository_add_get_save(seed_auth_user):
    uow = UnitOfWork()
    authentication_user, _ = seed_auth_user(uow)
                
    marketing_user = mdl.User(
        id = authentication_user.id,
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
    weightage = mdl.Weightage(
        weightage_type= pmt_mdl.TransactionType.REFERRAL,
        weightage_value= 10,
    )

    uow.weightages.save(weightage)
    fetched_weightage = uow.weightages.get(weightage_type= pmt_mdl.TransactionType.REFERRAL)
    assert fetched_weightage == weightage

    weightage.weightage_value = 20
    uow.weightages.save(weightage)
    fetched_weightage = uow.weightages.get(weightage_type= pmt_mdl.TransactionType.REFERRAL)
    assert fetched_weightage == weightage

def test_cashback_slab_repository_add_get_save():
    uow = UnitOfWork()
    cashback_slab_1 = mdl.CashbackSlab(
        start_amount= 0,
        end_amount= 100,
        cashback_type= mdl.CashbackType.PERCENTAGE,
        cashback_value= 0.5,
    )

    cashback_slab_2 = mdl.CashbackSlab(
        start_amount= 100,
        end_amount= 200,
        cashback_type= mdl.CashbackType.PERCENTAGE,
        cashback_value= 0.7,
    )
    
    cashback_slabs = [cashback_slab_1, cashback_slab_2]
    all_cashbacks = mdl.AllCashbacks(cashback_slabs=cashback_slabs)
    uow.cashback_slabs.save_all(all_cashbacks)
    fetched_all_cashbacks = uow.cashback_slabs.get_all()
    assert fetched_all_cashbacks.cashback_slabs == cashback_slabs

    cashback_slabs[0].cashback_value = 0.6
    all_cashbacks = mdl.AllCashbacks(cashback_slabs=cashback_slabs)
    uow.cashback_slabs.save_all(all_cashbacks)
    fetched_all_cashbacks = uow.cashback_slabs.get_all()
    assert fetched_all_cashbacks.cashback_slabs == cashback_slabs
