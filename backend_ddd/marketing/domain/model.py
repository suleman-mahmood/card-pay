# referral_roll_number: Optional[str] = None

"""marketing microservices domain model"""
from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from .exceptions import InvalidReferenceException, InvalidWeightageException, InvalidTrasnsactionTypeException, InvalidCashbackTypeException, NegativeAmountException, InvalidAddingLoyaltyPointsException, InvalidSlabException, NotVerifiedException
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
    """data value object"""
    start_amount: float
    end_amount: float
    cashback_type: CashbackType
    cashback_value: float

    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class AllCashbacks:

    cashback_slabs: List[CashbackSlab]

    def _helper_handle_invalid_slabs(self, idx):
        if self.cashback_slabs[idx].end_amount <= self.cashback_slabs[idx].start_amount:
            raise ValueError(
                "ending amount should be greater than starting amount")
        if self.cashback_slabs[idx].cashback_value < 0:
            raise ValueError("Cashback value cannot be negative")
        if self.cashback_slabs[idx].cashback_type != "PERCENTAGE" and self.cashback_slabs[idx].cashback_type != "ABSOLUTE":
            raise ValueError(
                "Cashback type should be either PERCENTAGE or ABSOLUTE")
        if self.cashback_slabs[idx].cashback_type == "PERCENTAGE":
            if self.cashback_slabs[idx].cashback_value > 1:
                raise ValueError(
                    "Cashback percentage value cannot be greater than 1")
            else:
                if self.cashback_slabs[idx].cashback_value > self.cashback_slabs[idx].end_amount:
                    raise ValueError(
                        "Cashback absolute value cannot be greater than the slab ending amount")

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
            self._helper_handle_invalid_slabs(i)

    def __post_init__(self):
        self._handle_invalid_slabs()


@dataclass
class Weightage:
    """data value object - Loyality points weightage"""

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
    """Entity"""
    id: str
    loyalty_points: int = 0
    referral_id: str = DEFAULT_UUID
    marketing_user_verified: bool = False

    # exceptions
    def _negative_amount_exception(self, amount: int):
        if amount < 0:
            raise NegativeAmountException(
                "Negative amount passed, amount cannot be negative"
            )

    def _not_verified_exception(self):
        if not self.marketing_user_verified:
            raise NotVerifiedException(
                "User is not verified"
            )

    def _already_referred_exception(self):
        if self.referral_id != DEFAULT_UUID:
            raise InvalidReferenceException(
                "User has already been referred"
            )

    def _cannot_refer_self(self, referral_id: str):
        if self.id == referral_id:
            raise InvalidReferenceException(
                "User cannot refer themselves"
            )

    def _referee_not_verified_exception(self, referee_verified: bool):
        if not referee_verified:
            raise InvalidReferenceException(
                "Referee is not verified"
            )

    def _invalid_weightage_passed_exception(self, weightage: Weightage):
        if weightage.weightage_type != TransactionType.REFERRAL:
            raise InvalidWeightageException(
                "Invalid weightage type passed. Weightage type should be REFERRAL"
            )

    def add_referral_loyalty_points(self, weightage: Weightage, referee_verified: bool):
        """Add loyalty points to user account for P transaction type"""

        self._not_verified_exception()
        self._referee_not_verified_exception(referee_verified)
        self._invalid_weightage_passed_exception(weightage)

        self.loyalty_points += weightage.weightage_value

    def _invalid_transaction_type_exception(self, transaction_type: TransactionType, weightage_type: TransactionType):
        if transaction_type != weightage_type:
            raise InvalidTrasnsactionTypeException(
                "Passed transaction type and weightage type do not match"
            )

    def _empty_cashback_slabs_exception(self, cashback_slabs: List[CashbackSlab]):
        if len(cashback_slabs) == 0:
            raise InvalidSlabException(
                "No slabs exist"
            )

    def _multiple_eligible_slabs_exception(self, eligible_slabs: List[CashbackSlab]):
        if len(eligible_slabs) > 1:
            raise InvalidSlabException(
                "Multiple slabs exist for the passed amount"
            )

    def _no_eligible_slabs_exception(self, eligible_slabs: List[CashbackSlab]):
        if len(eligible_slabs) == 0:
            raise InvalidSlabException(
                "No slab exists for the passed amount"
            )

    def _invalid_cashback_type_exception(self, cashback_type: CashbackType):
        if cashback_type != CashbackType.PERCENTAGE and cashback_type != CashbackType.ABSOLUTE:
            raise InvalidCashbackTypeException(
                "Invalid cashback type passed"
            )

    # use cases
    def use_reference(self, referral_id: str):

        self._not_verified_exception()

        self._already_referred_exception()

        self._cannot_refer_self(referral_id)

        self.referral_id = referral_id

    def add_loyalty_points(self, transaction_type: TransactionType, transaction_amount: int, weightage: Weightage):
        """Add loyalty points to user account for P2P_PUSH, P2P_PULL, and PAYMENT_GATEWAY transaction type"""

        self._not_verified_exception()
        self._negative_amount_exception(transaction_amount)
        self._invalid_transaction_type_exception(
            transaction_type, weightage.weightage_type)

        self.loyalty_points += transaction_amount * weightage.weightage_value

    def calculate_cashback(self, deposit_amount: int, cashback_slabs: List[CashbackSlab]) -> float:
        """Calculate cashback for the passed deposit amount"""

        self._not_verified_exception()
        self._negative_amount_exception(deposit_amount)
        self._empty_cashback_slabs_exception(cashback_slabs)

        # If deposit amount is greater than the last slab, then the last slab will be used
        if (deposit_amount >= cashback_slabs[-1].end_amount):

            slab = cashback_slabs[-1]

        else:
            eligible_slabs = list(
                filter(
                    lambda slab: deposit_amount >= slab.start_amount and deposit_amount < slab.end_amount,
                    cashback_slabs
                )
            )

            self._multiple_eligible_slabs_exception(eligible_slabs)
            self._no_eligible_slabs_exception(eligible_slabs)

            slab = eligible_slabs[0]

            self._invalid_cashback_type_exception(slab.cashback_type)

        if slab.cashback_type == CashbackType.PERCENTAGE:
            return deposit_amount * slab.cashback_value
        elif slab.cashback_type == CashbackType.ABSOLUTE:
            return slab.cashback_value

    def verify_user(self):
        """Verify user"""
        self.marketing_user_verified = True
