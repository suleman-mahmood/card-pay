import pytest

from .conftest import (seed_user)
from ....payment.domain.model import TransactionType
from ...domain.exceptions import InvalidReferenceException, NotVerifiedException, InvalidAddingLoyaltyPointsException, NegativeAmountException, InvalidSlabException
from ...domain.model import User, CashbackType, Weightage, CashbackSlab, AllCashbacks


def test_add_loyalty_points_for_deposit(seed_user):
    transaction_amount = 1000
    weightage = Weightage(
        weightage_type= TransactionType.PAYMENT_GATEWAY,
        weightage_value=0.1
    )
    user = seed_user()
    user.verify_user()
    user.add_loyalty_points(TransactionType.PAYMENT_GATEWAY, transaction_amount, weightage)

    assert user.loyalty_points == transaction_amount * weightage.weightage_value


def test_add_loyalty_points_for_push_transaction(seed_user):
    transaction_amount = 1000
    weightage = Weightage(
        weightage_type= TransactionType.P2P_PUSH,
        weightage_value=0.1
    )
    user = seed_user()
    user.verify_user()
    user.add_loyalty_points(TransactionType.P2P_PUSH, transaction_amount, weightage)

    assert user.loyalty_points == transaction_amount * weightage.weightage_value
    
def test_add_loyalty_points_for_pull_transaction(seed_user):
    transaction_amount = 1000
    weightage = Weightage(
        weightage_type= TransactionType.P2P_PULL,
        weightage_value=0.1
    )
    user = seed_user()
    user.verify_user()
    user.add_loyalty_points(TransactionType.P2P_PULL, transaction_amount, weightage)

    assert user.loyalty_points == transaction_amount * weightage.weightage_value

def test_use_reference_and_add_referral_loyalty_points(seed_user):
    referral = seed_user()
    referee_1 = seed_user()
    referral_2 = seed_user()

    with pytest.raises(NotVerifiedException, match = "User is not verified"):
        referee_1.use_reference(referral.id)

    referee_1.verify_user()

    with pytest.raises(InvalidReferenceException, match = "User cannot refer themselves"):
        referee_1.use_reference(referee_1.id)

    referral.verify_user()
    # Marketing command 'use reference' will check if both the referee and referral are verified

    referee_1.use_reference(referral.id)
    assert referee_1.referral_id == referral.id

    with pytest.raises(InvalidReferenceException, match = "User has already been referred"):
        referee_1.use_reference(referral.id)

    with pytest.raises(InvalidReferenceException, match = "User has already been referred"):
        referee_1.use_reference(referral_2.id)

    weightage = Weightage(
        weightage_type= TransactionType.REFERRAL,
        weightage_value= 50
    )

    referral.add_referral_loyalty_points(
        weightage = weightage,
        referee_verified= referee_1.marketing_user_verified
    ) # This function will be called by the marketing commands
    
    assert referral.loyalty_points == weightage.weightage_value

    referee_2 = seed_user()
    referee_2.verify_user()

    referee_2.use_reference(referral.id)
    assert referee_2.referral_id == referral.id

    referral.add_referral_loyalty_points(
        weightage = weightage,
        referee_verified= referee_2.marketing_user_verified
    ) # This function will be called by the marketing commands
    
    assert referral.loyalty_points == 2 * weightage.weightage_value

def test_cashback_on_deposit(seed_user):
    '''
      if self.cashback_slabs[idx].end_amount <= self.cashback_slabs[idx].start_amount:
            raise ValueError(
                "ending amount is smaller than starting amount")
        if self.cashback_slabs[idx].cashback_value < 0:
            raise ValueError("Cashback value is negative")
        if self.cashback_slabs[idx].cashback_type != CashbackType.PERCENTAGE and self.cashback_slabs[idx].cashback_type != CashbackType.ABSOLUTE:
            raise ValueError(
                "Cashback type is neither PERCENTAGE nor ABSOLUTE")
        if self.cashback_slabs[idx].cashback_type == CashbackType.PERCENTAGE:
            if self.cashback_slabs[idx].cashback_value > 1:
                raise ValueError(
                    "Cashback percentage value is greater than 1")
            else:
                if self.cashback_slabs[idx].cashback_value > self.cashback_slabs[idx].end_amount:
                    raise ValueError(
                        "Cashback absolute value is greater than the slab ending amount")
        if idx != -1 and self.cashback_slabs[idx+1].start_amount != self.cashback_slabs[idx].end_amount:
            raise ValueError(
                "Slabs are not continuous")

    def _handle_invalid_slabs(self):
        if len(self.cashback_slabs) == 0:
            raise ValueError("Cashback slabs cannot be empty")

        first_slab_start_amount = self.cashback_slabs[0].start_amount
        if first_slab_start_amount != 0:
            self.cashback_slabs.insert(
                0, CashbackSlab(
                    start_amount=0,
                    end_amount=first_slab_start_amount,
                    cashback_type=self.cashback_slabs[0].cashback_type,
                    cashback_value=self.cashback_slabs[0].cashback_value
                )
            )
        self._helper_handle_invalid_slabs(-1)

        for i in range(len(self.cashback_slabs) - 1):
            print("ASJDHASKDGHAKSDHAKSJDHASKJDHASKJDH: ", i)
            self._helper_handle_invalid_slabs(i)

    '''
    user = seed_user()
    
    deposit_amount = 7000

    cashback_slab_1 = CashbackSlab(
        start_amount= 0,
        end_amount= 5000,
        cashback_type= CashbackType.PERCENTAGE,
        cashback_value= 0.1
    )

    cashback_slab_2 = CashbackSlab(
        start_amount= 5000,
        end_amount= 10000,
        cashback_type= CashbackType.ABSOLUTE,
        cashback_value= 100
    )
    
    all_cashbacks = AllCashbacks(cashback_slabs = [cashback_slab_1, cashback_slab_2])

    with pytest.raises(NotVerifiedException, match = "User is not verified"):
        user.calculate_cashback(deposit_amount, all_cashbacks.cashback_slabs)

    user.verify_user()

    with pytest.raises(NegativeAmountException, match = "amount cannot be negative"):
        user.calculate_cashback(-1 * deposit_amount, all_cashbacks.cashback_slabs)

    with pytest.raises(ValueError, match = "Slabs are not continuous"):
        AllCashbacks( cashback_slabs=[cashback_slab_1, cashback_slab_2, cashback_slab_2])

    assert user.calculate_cashback(deposit_amount, all_cashbacks) == cashback_slab_2.cashback_value
