# referral_roll_number: Optional[str] = None

"""marketing microservices domain model"""
from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from .exceptions import InvalidReferenceException, InvalidWeightageException, InvalidTrasnsactionTypeException, InvalidCashbackTypeException, NegativeAmountException, InvalidAddingLoyalityPointsException, InvalidSlabException
from ...payment.domain.model import TransactionType
from typing import List, Dict
from itertools import filterfalse


class CashbackType(str, Enum):
    """Cashback type enum"""
    PERCENTAGE = 1
    ABSOLUTE = 2


class WeightageType(str, Enum):
    """Weightage type enum"""
    P2P_PUSH = 1
    P2P_PULL = 2
    PAYMENT_GATEWAY = 3
    CASHBACK = 4
    REFERRAL = 5


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
    weightage_type: WeightageType
    weightage_value: float

    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class User():
    """Entity"""
    id: str
    loyalty_points: int = 0
    referral_id: str = ""
    user_referred: bool = False

    def _negative_amount_exception(self, amount: int):
        if amount < 0:
            raise NegativeAmountException(
                "Negative amount passed, amount cannot be negative"
            )

    def use_reference(self, referral_id: str):
        if self.user_referred and self.referral_id != "":
            raise InvalidReferenceException(
                "User has already been referred"
            )
        elif self.user_referred:
            raise InvalidReferenceException(
                "Cannot refer a user now"
            )
        elif self.id == referral_id:
            raise InvalidReferenceException(
                "User cannot refer themselves"
            )

        self.referral_id = referral_id

    def add_referral_loyalty_points(self, weightage: Weightage):
        """Add loyalty points to user account for P transaction type"""
        if self.user_referred:
            raise InvalidAddingLoyalityPointsException(
                "User has already been referred"
            )
        if weightage.weightage_type != WeightageType.REFERRAL:
            raise InvalidWeightageException(
                "Invalid weightage type passed. Weightage type should be REFERRAL"
            )

        self.user_referred = True
        self.loyalty_points += weightage.value

    def add_loyalty_points(self, transaction_type: TransactionType, amount: int, weightage: Weightage):
        """Add loyalty points to user account for P2P_PUSH, P2P_PULL, and PAYMENT_GATEWAY transaction type"""
        self._negative_amount_exception(amount)
        if transaction_type != weightage.weightage_type:
            raise InvalidAddingLoyalityPointsException(
                "Passed transaction type and weightage type do not match"
            )

        self.loyalty_points += amount * weightage.weightage_value

    def calculate_cashback(self, deposit_amount: int, cashback_slabs: List[CashbackSlab]) -> float:

        self._negative_amount_exception(deposit_amount)

        eligible_slabs = filterfalse(
            lambda slab: deposit_amount >= slab.start_amount and deposit_amount < slab.end_amount, cashback_slabs)
        
        if len(eligible_slabs) > 1:
            raise InvalidSlabException(
                "Multiple slabs exist for the passed amount"
            )
        elif len(eligible_slabs) <= 0:
            raise InvalidSlabException(
                "No slab exist for the passed amount"
            )

        slab = eligible_slabs[0]
        if slab.cashback_type != CashbackType.PERCENTAGE or slab.cashback_type != CashbackType.ABSOLUTE:
            raise InvalidCashbackTypeException(
                "Invalid cashback type passed"
            )

        if slab.cashback_type == CashbackType.PERCENTAGE:
            return deposit_amount * slab.cashback_value
        elif slab.cashback_type == CashbackType.ABSOLUTE:
            return slab.cashback_value

        # for slab in cashback_slabs:
        #     if deposit_amount >= slab.start_amount and deposit_amount < slab.end_amount:
        #         if slab.cashback_type == CashbackType.PERCENTAGE:
        #             return deposit_amount * slab.cashback_value
        #         elif slab.cashback_type == CashbackType.ABSOLUTE:
        #             return slab.cashback_value
        #         else:
        #             raise InvalidCashbackTypeException(
        #                 "Invalid cashback type passed"
        #             )

        # # slabs = list(weightage_cashback.keys())
        # # slab = slabs[-1]
        # # for i in range(len(slabs)):
        # #     if deposit_amount >= slabs[i]:
        # #         continue
        # #     else:
        # #         slab = slabs[i-1]
        # #         break

        # # if weightage_cashback[slab] <= 1:
        # #     return deposit_amount * weightage_cashback[slab]
        # # else:
        # #     return weightage_cashback[slab]


# @dataclass
# class Weightage:
#     """Entity"""
#     id: int = 1
#     weightage_payment_gateway: int = 0.1
#     weightage_p2p_push: int = 2
#     weightage_p2p_pull: int = 3
#     weightage_referral: int = 0.1
#     weightage_cashback: List[WeightageCashback] = field(default_factory=list)

#     def change_weightage(self, weightage_type: TransactionType, amount: int):
#         if weightage_type == TransactionType.PAYMENT_GATEWAY:
#             self.weightage_payment_gateway = amount
#         elif weightage_type == TransactionType.P2P_PUSH:
#             self.weightage_p2p_push = amount
#         elif weightage_type == TransactionType.P2P_PULL:
#             self.weightage_p2p_pull = amount
#         else:
#             raise InvalidWeightageException(
#                 "Invalid weightage type passed"
#             )

#     def change_referral_weightage(self, amount: int):
#         self.weightage_referral = amount

#     def change_cashback_weightage(self, weightage_cashback: List[WeightageCashback]):
#         self.weightage_cashback = weightage_cashback


# @dataclass
# class User():
#     """Entity"""
#     id: str
#     loyalty_points: int = 0
#     referral_id: str = ""

#     def use_reference(self, referral_id: str):
#         if self.referral_id != "":
#             raise InvalidReferenceException(
#                 "User has already been referred"
#             )
#         if self.id == referral_id:
#             raise InvalidReferenceException(
#                 "User cannot refer themselves"
#             )

#         self.referral_id = referral_id

#     def add_loyalty_points(self, transaction_type: TransactionType, amount: int, weightage: Weightage):

#         if transaction_type == TransactionType.PAYMENT_GATEWAY:
#             self.loyalty_points += amount * weightage.weightage_payment_gateway

#         elif transaction_type == TransactionType.P2P_PUSH:
#             self.loyalty_points += amount * weightage.weightage_p2p_push

#         elif transaction_type == TransactionType.P2P_PULL:
#             self.loyalty_points += amount * weightage.weightage_p2p_pull

#     def add_referral_loyalty_points(self, weightage: Weightage):
#         self.loyalty_points += weightage.weightage_referral

#     def calculate_cashback(self, deposit_amount: int, weightage: Weightage) -> float:

#         weightage_cashback = weightage.weightage_cashback
#         for slab in weightage_cashback:
#             if deposit_amount >= slab.start_amount and deposit_amount < slab.end_amount:
#                 if slab.cashback_type == CashbackType.PERCENTAGE:
#                     return deposit_amount * slab.cashback_value
#                 else:
#                     return slab.cashback_value
#         # slabs = list(weightage_cashback.keys())
#         # slab = slabs[-1]
#         # for i in range(len(slabs)):
#         #     if deposit_amount >= slabs[i]:
#         #         continue
#         #     else:
#         #         slab = slabs[i-1]
#         #         break

#         # if weightage_cashback[slab] <= 1:
#         #     return deposit_amount * weightage_cashback[slab]
#         # else:
#         #     return weightage_cashback[slab]
