import pytest

from .conftest import (seed_user, seed_weightage)
from ...domain.exceptions import InvalidReferenceException



def test_add_loyalty_points_for_deposit(seed_user, seed_weightage):
    transaction_type = "PAYMENT_GATEWAY"
    amount = 1000
    weightage = seed_weightage()

    user = seed_user()
    user.add_loyalty_points(transaction_type, amount, weightage)

    assert user.loyalty_points == amount * weightage.weightage_payment_gateway

def test_add_loyalty_points_on_push_transaction(seed_user, seed_weightage):
    transaction_type = "P2P_PUSH"
    amount = 1000
    weightage = seed_weightage()

    user = seed_user()
    user.add_loyalty_points(transaction_type, amount, weightage)

    assert user.loyalty_points == amount * weightage.weightage_p2p_push


def test_add_loyalty_points_on_pull_transaction(seed_user, seed_weightage):
    transaction_type = "P2P_PULL"
    amount = 1000
    weightage = seed_weightage()

    user = seed_user()
    user.add_loyalty_points(transaction_type, amount, weightage)

    assert user.loyalty_points == amount * weightage.weightage_p2p_pull

def test_cashback_on_deposit(seed_user, seed_weightage):
    """Also Caters to cashback on number of transactions"""
    
    amount = 1200
    weightage = seed_weightage()

    user = seed_user()
    assert user.calculate_cashback(amount, weightage) == weightage.weightage_cashback[1000] * amount

    amount = 550
    assert user.calculate_cashback(amount, weightage) == weightage.weightage_cashback[500]

    amount = 400
    assert user.calculate_cashback(amount, weightage) == weightage.weightage_cashback[0]


def test_referral(seed_user, seed_weightage):

    referral_1 = seed_user()
    referral_2 = seed_user()
    referee_1 = seed_user()
    referee_2 = seed_user()
    weightage = seed_weightage()

    with pytest.raises(InvalidReferenceException, match = "User cannot refer themselves"):
        referral_1.use_reference(referral_1.id)

    referee_1.use_reference(referral_1.id)
    referral_1.add_referral_loyalty_points(weightage)
    assert referral_1.loyalty_points == weightage.weightage_referral

    referee_2.use_reference(referral_1.id)
    referral_1.add_referral_loyalty_points(weightage)
    assert referral_1.loyalty_points == 2 * weightage.weightage_referral

    assert referee_1.referral_id == referral_1.id
    assert referee_2.referral_id == referral_1.id

    with pytest.raises(InvalidReferenceException, match = "User has already been referred"):
        referee_1.use_reference(referral_2.id)

    with pytest.raises(InvalidReferenceException, match = "User has already been referred"):
        referee_2.use_reference(referral_2.id)

