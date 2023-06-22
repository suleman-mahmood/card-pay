# referral_roll_number: Optional[str] = None

"""marketing microservices domain model"""
from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from .exceptions import InvalidReferenceException, InvalidWeightageException, InvalidTrasnsactionTypeException, InvalidCashbackTypeException, NegativeAmountException, InvalidAddingLoyaltyPointsException, InvalidSlabException, NotVerifiedException
from ...payment.domain.model import TransactionType
from typing import List, Dict
from itertools import filterfalse


class CashbackType(str, Enum):
    """Cashback type enum"""
    PERCENTAGE = 1
    ABSOLUTE = 2


# class WeightageType(str, Enum):
#     """Weightage type enum"""
#     P2P_PUSH = 1
#     P2P_PULL = 2
#     PAYMENT_GATEWAY = 3
#     CASHBACK = 4
#     REFERRAL = 5


@dataclass
class CashbackSlab:
    """data value object"""
    start_amount: float
    end_amount: float
    cashback_type: CashbackType
    cashback_value: float

    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class Weightage:
    """data value object"""
    weightage_type: TransactionType

    '''
    Weightage value will be in percentage for P2P_PUSH, P2P_PULL, PAYMENT_GATEWAY
    Weightage value will be an absolute amount for REFERRAL
    '''

    weightage_value: float 

    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class User():
    """Entity"""
    id: str
    loyalty_points: int = 0
    referral_id: str = ""
    user_verified: bool = False

    def _negative_amount_exception(self, amount: int):
        if amount < 0:
            raise NegativeAmountException(
                "Negative amount passed, amount cannot be negative"
            )

    def _not_verified_exception(self):
        if not self.user_verified:
            raise NotVerifiedException(
                "User is not verified"
            )


    def add_referral_loyalty_points(self, weightage: Weightage, referee_verified: bool):
        """Add loyalty points to user account for P transaction type"""
        if self.user_verified == False:
            raise InvalidAddingLoyaltyPointsException(
                "Referral is not verified"
            )
        if referee_verified == False:
            raise InvalidAddingLoyaltyPointsException(
                "Referee is not verified"
            )
        if weightage.weightage_type != TransactionType.REFERRAL:
            raise InvalidWeightageException(
                "Invalid weightage type passed. Weightage type should be REFERRAL"
            )

        self.loyalty_points += weightage.weightage_value

    def use_reference(self, referral_id: str):
        
        self._not_verified_exception()

        if self.referral_id != "":
            raise InvalidReferenceException(
                "User has already been referred"
            )
        if self.id == referral_id:
            raise InvalidReferenceException(
                "User cannot refer themselves"
            )

        # if referral_id == "":
        #     self.referral_id = "-1111"
        # else:
        self.referral_id = referral_id

    def add_loyalty_points(self, transaction_type: TransactionType, transaction_amount: int, weightage: Weightage):
        """Add loyalty points to user account for P2P_PUSH, P2P_PULL, and PAYMENT_GATEWAY transaction type"""
        self._not_verified_exception()
        self._negative_amount_exception(transaction_amount)

        if transaction_type != weightage.weightage_type:
            raise InvalidAddingLoyaltyPointsException(
                "Passed transaction type and weightage type do not match"
            )

        self.loyalty_points += transaction_amount * weightage.weightage_value

    def calculate_cashback(self, deposit_amount: int, cashback_slabs: List[CashbackSlab]) -> float:
        """Calculate cashback for the passed deposit amount"""
        self._not_verified_exception()
        self._negative_amount_exception(deposit_amount)

        eligible_slabs = list(
            filter(
                    lambda slab: deposit_amount >= slab.start_amount and deposit_amount < slab.end_amount,
                    cashback_slabs
                )
        )
        
        if len(eligible_slabs) > 1:
            raise InvalidSlabException(
                "Multiple slabs exist for the passed amount"
            )
        elif len(eligible_slabs) == 0:
            raise InvalidSlabException(
                "No slab exists for the passed amount"
            )

        slab = eligible_slabs[0]

        if slab.cashback_type != CashbackType.PERCENTAGE and slab.cashback_type != CashbackType.ABSOLUTE:
            raise InvalidCashbackTypeException(
                "Invalid cashback type passed"
            )

        if slab.cashback_type == CashbackType.PERCENTAGE:
            return deposit_amount * slab.cashback_value
        elif slab.cashback_type == CashbackType.ABSOLUTE:
            return slab.cashback_value

    def verify_user(self):
        """Verify user"""
        self.user_verified = True
        
        