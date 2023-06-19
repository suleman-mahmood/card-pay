import pytest

from ...domain.model import (User, Vendor, Deal, Deal_status)
from .utils import _calculate_loyalty_points    
from .conftest import seed_user

# def test_add_loyalty_points_for_transactions_and_deals():
#     user = User()

#     user.make_transaction(1000)
#     user.make_transaction(2000)
#     vendor = Vendor()
#     deal = vendor.create_deal(name = "Ek ke sath ek free")
#     user.redeem_deal(deal)

#     loyalty_points = _calculate_loyalty_points(user.number_of_transactions, user.total_amount, user.number_of_deals_redeemed)

#     assert user.loyalty_points == loyalty_points


# def test_give_referral():
#     """One user give referral to another user
#             Check the referral and referee id of the user"""
#     referral = User()
#     referee_1 = User()
#     referee_2 = User()

#     referee_1.use_reference(referral.id)
#     referee_2.use_reference(referral.id)

#     assert referee_1.referral_id == referral.id
#     assert referee_2.referral_id == referral.id

# def test_cashback_on_amount():
#     amount = 100000
#     user = User()
#     user.make_transaction(amount)
#     user.cashback = _calculate_cashback_amount(amount)


# def test_cashback_on_number_of_transactions():
#     pass


def test_add_loyalty_points_for_deposit(seed_user):
    transaction_type = "PAYMENT_GATEWAY"
    amount = 1000

    user = seed_user()
    user.add_loyalty_points(transaction_type, amount)

    assert user.loyalty_points == 1000

def test_add_loyalty_points_on_push_transaction(seed_user):
    transaction_type = "P2P_PUSH"
    amount = 1000

    user = seed_user()
    user.add_loyalty_points(transaction_type, amount)

    assert user.loyalty_points == 100


def test_add_loyalty_points_on_pull_transaction(seed_user):
    transaction_type = "P2P_PULL"
    amount = 1000

    user = seed_user()
    user.add_loyalty_points(transaction_type, amount)

    assert user.loyalty_points == 50

def test_cashback_on_deposit(seed_user):
    action = "PAYMENT_GATEWAY"
    amount = 1000

    user = seed_user()
    user.calculate_cashback(action, amount)

    assert user.cashback == 100

def test_cashback_on_x_transactions():
    #We have to record the number of transactions for this. No?
    pass

def test_referral(seed_user):
    referral = seed_user()
    referee_1 = seed_user()
    referee_2 = seed_user()

    referee_1.use_reference(referral.id)
    referral.calculate_cashback("REFERRAL", 0)
    assert referral.cashback == 100

    referee_2.use_reference(referral.id)
    referral.calculate_cashback("REFERRAL", 0)
    assert referral.cashback == 200

    assert referee_1.referral_id == referral.id
    assert referee_2.referral_id == referral.id

def test_vendor_create_deal(seed_vendor):
    vendor = seed_vendor()
    deal_name = "Bazinga"
    deal = vendor.create_deal(deal_name)

    assert deal.vendor_id == vendor.id
    assert vendor.deals[0] == deal.id
