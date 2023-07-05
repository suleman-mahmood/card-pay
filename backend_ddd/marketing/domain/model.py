# referral_roll_number: Optional[str] = None

"""marketing microservices domain model"""
from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from .exceptions import InvalidReferenceException, InvalidWeightageException, InvalidTransactionTypeException, InvalidCashbackTypeException, NegativeAmountException, InvalidAddingLoyaltyPointsException, InvalidSlabException, NotVerifiedException, negative_amount_exception, not_verified_exception, referee_not_verified_exception, user_already_referred_exception, cannot_refer_self, not_deposit_exception
from ...payment.domain.model import TransactionType
from typing import List, Dict
from itertools import filterfalse
from .utils import DEFAULT_UUID


def behaviour():
    """
    1. Weightage value for loyalty points can be any value which will be multipled directly to the transaction amount in case of P2P_PUSH, P2P_PULL, PAYMENT_GATEWAY or it can be an absolute amount in case of REFERRAL
    2. Cashback value is a percentage less than 1 (0.1 or 0.2)
    """
    pass


class CashbackType(str, Enum):
    """Cashback type enum"""
    PERCENTAGE = 1
    ABSOLUTE = 2


@dataclass
class CashbackSlab:
    """Data value object"""
    start_amount: float
    end_amount: float
    cashback_type: CashbackType
    cashback_value: float

    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class AllCashbacks:
    "Data Value Object - Aggregate Root"

    cashback_slabs: List[CashbackSlab]

    def _helper_handle_invalid_slabs(self, idx):
        if self.cashback_slabs[idx].end_amount <= self.cashback_slabs[idx].start_amount:
            raise InvalidSlabException(
                "ending amount is smaller than starting amount")
        if self.cashback_slabs[idx].cashback_value < 0:
            raise InvalidSlabException("Cashback value is negative")
        if self.cashback_slabs[idx].cashback_type != CashbackType.PERCENTAGE and self.cashback_slabs[idx].cashback_type != CashbackType.ABSOLUTE:
            raise InvalidSlabException(
                "Cashback type is neither PERCENTAGE nor ABSOLUTE")
        if self.cashback_slabs[idx].cashback_type == CashbackType.PERCENTAGE:
            if self.cashback_slabs[idx].cashback_value > 1:
                raise InvalidSlabException(
                    "Cashback percentage value is greater than 1")
        else:
            if self.cashback_slabs[idx].cashback_value > self.cashback_slabs[idx].end_amount:
                raise InvalidSlabException(
                    "Cashback absolute value is greater than the slab ending amount")
        if idx != -1 and self.cashback_slabs[idx+1].start_amount != self.cashback_slabs[idx].end_amount:
            raise InvalidSlabException(
                "Slabs are not continuous")

    def _handle_invalid_slabs(self):
        if len(self.cashback_slabs) == 0:
            raise InvalidSlabException("Cashback slabs cannot be empty")

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
            self._helper_handle_invalid_slabs(i)

    def __post_init__(self):
        self._handle_invalid_slabs()


@dataclass
class Weightage:
    """Data value object"""

    '''
    Weightage value will be a percentage for P2P_PUSH, P2P_PULL, PAYMENT_GATEWAY
    Weightage value will be an absolute amount for REFERRAL
    '''

    weightage_type: TransactionType
    weightage_value: float

    def set_weightage(self, weightage_value: float):
        if (weightage_value < 0):
            raise InvalidWeightageException(
                "Negative weightage value passed, weightage value cannot be negative"
            )
        self.weightage_value = weightage_value


@dataclass
class User():
    """Entity - Marketing user aggregate root"""

    id: str
    loyalty_points: int = 0
    referral_id: str = DEFAULT_UUID
    marketing_user_verified: bool = False

    # exceptions
    def _invalid_weightage_passed_exception(self, weightage: Weightage):
        if weightage.weightage_type != TransactionType.REFERRAL:
            raise InvalidWeightageException(
                "Invalid weightage type passed. Weightage type should be REFERRAL"
            )

    def _invalid_transaction_type_exception(self, transaction_type: TransactionType, weightage_type: TransactionType):
        if transaction_type != weightage_type:
            raise InvalidTransactionTypeException(
                "Passed transaction type and weightage type do not match"
            )
        
    def add_referral_loyalty_points(self, weightage: Weightage, referee_verified: bool):
        """Add loyalty points to user account for P transaction type"""

        # self._not_verified_exception()
        # self._referee_not_verified_exception(referee_verified)

        not_verified_exception(self.marketing_user_verified)
        referee_not_verified_exception(referee_verified)
        self._invalid_weightage_passed_exception(weightage)

    
        self.loyalty_points += weightage.weightage_value


    # use cases
    def use_reference(self, referral_id: str):

        not_verified_exception(self.marketing_user_verified)
        user_already_referred_exception(self.referral_id)
        cannot_refer_self(self.id, referral_id)

        self.referral_id = referral_id

    def add_loyalty_points(self, transaction_type: TransactionType, transaction_amount: int, weightage: Weightage):
        """Add loyalty points to user account for P2P_PUSH, P2P_PULL, and PAYMENT_GATEWAY transaction type"""

        not_verified_exception(self.marketing_user_verified)
        negative_amount_exception(transaction_amount)
        self._invalid_transaction_type_exception(
            transaction_type, weightage.weightage_type)

        self.loyalty_points += transaction_amount * weightage.weightage_value

    def calculate_cashback(self, deposit_amount: int, transaction_type: TransactionType, all_cashbacks: AllCashbacks) -> float:
        """Calculate cashback for the passed deposit amount"""

        not_verified_exception(self.marketing_user_verified)
        negative_amount_exception(deposit_amount)
        not_deposit_exception(transaction_type)

        # If deposit amount is greater than the last slab, then the last slab will be used
        if (deposit_amount >= all_cashbacks.cashback_slabs[-1].end_amount):
            slab = all_cashbacks.cashback_slabs[-1]

        else:
            eligible_slab = [slab for slab in all_cashbacks.cashback_slabs if deposit_amount >= slab.start_amount and deposit_amount < slab.end_amount]
            slab = eligible_slab[0]

        if slab.cashback_type == CashbackType.PERCENTAGE:
            return deposit_amount * slab.cashback_value
        else:
            return slab.cashback_value

    def verify_user(self):
        """for testing purposes"""
        self.marketing_user_verified = True
