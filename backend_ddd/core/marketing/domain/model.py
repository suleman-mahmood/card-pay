"""
    1. Weightage value for loyalty points can be any value which will be multiplied 
        directly to the transaction amount in case of P2P_PUSH, P2P_PULL, PAYMENT_GATEWAY
        or it can be an absolute amount in case of REFERRAL
    2. Cashback value is a percentage less than 1 (0.1 or 0.2)
"""

import math
from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from typing import List
from core.marketing.domain import exceptions as ex
from core.payment.domain import model as  pmt_mdl
from core.marketing.domain.utils import DEFAULT_UUID


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
        ex.slab_ending_amount_lesser_than_or_equal_to_slab_starting_amount_exception(
            slab_ending_amount=self.cashback_slabs[idx].end_amount,
            slab_starting_amount=self.cashback_slabs[idx].start_amount,
        )
        ex.slab_cashback_value_is_negative_exception(
            slab_cashback_value=self.cashback_slabs[idx].cashback_value
        )

        if (
            self.cashback_slabs[idx].cashback_type != CashbackType.PERCENTAGE
            and self.cashback_slabs[idx].cashback_type != CashbackType.ABSOLUTE
        ):
            raise ex.InvalidSlabException(
                "Cashback type is neither PERCENTAGE nor ABSOLUTE"
            )
        if (
            self.cashback_slabs[idx].cashback_type == CashbackType.PERCENTAGE
            and self.cashback_slabs[idx].cashback_value > 1
        ):
            raise ex.InvalidSlabException("Cashback percentage value is greater than 1")
        elif (
            self.cashback_slabs[idx].cashback_type == CashbackType.ABSOLUTE
            and self.cashback_slabs[idx].cashback_value
            > self.cashback_slabs[idx].end_amount
        ):
            raise ex.InvalidSlabException(
                "Cashback absolute value is greater than the slab ending amount"
            )

        if idx != -1:
            ex.slab_not_continuos_exception(
                next_slab_starting_amount=self.cashback_slabs[idx + 1].start_amount,
                current_slab_ending_amount=self.cashback_slabs[idx].end_amount,
            )

    def handle_invalid_slabs(self):
        if len(self.cashback_slabs) == 0:
            self.cashback_slabs.insert(
                0,
                CashbackSlab(
                    start_amount=0,
                    end_amount=10,
                    cashback_type=CashbackType.ABSOLUTE,
                    cashback_value=0,
                ),
            )

        first_slab_start_amount = self.cashback_slabs[0].start_amount
        if first_slab_start_amount != 0:
            self.cashback_slabs.insert(
                0,
                CashbackSlab(
                    start_amount=0,
                    end_amount=first_slab_start_amount,
                    cashback_type=self.cashback_slabs[0].cashback_type,
                    cashback_value=0,
                ),
            )
        self._helper_handle_invalid_slabs(-1)

        for i in range(len(self.cashback_slabs) - 1):
            self._helper_handle_invalid_slabs(i)


@dataclass
class Weightage:
    """Data value object"""

    """
    Weightage value will be a percentage (less than 1) for P2P_PUSH, P2P_PULL, PAYMENT_GATEWAY
    Weightage value will be an absolute amount for REFERRAL
    """

    weightage_type: pmt_mdl.TransactionType
    weightage_value: float

    def set_weightage(self, weightage_value: float):
        ex.negative_weightage_exception(weightage_value)
        self.weightage_value = weightage_value


@dataclass
class User:
    """Entity - Marketing user aggregate root"""

    id: str
    loyalty_points: int = 0
    referral_id: str = DEFAULT_UUID
    marketing_user_verified: bool = False  # TODO: remove this pls

    def add_referral_loyalty_points(self, weightage: Weightage, referee_verified: bool):
        """Add loyalty points to user account for referral"""

        ex.not_verified_exception(self.marketing_user_verified)
        ex.referee_not_verified_exception(referee_verified)
        ex.invalid_weightage_passed_exception(weightage.weightage_type)

        self.loyalty_points += math.floor(weightage.weightage_value)

    def use_reference(self, referral_id: str):
        ex.not_verified_exception(self.marketing_user_verified)
        ex.user_already_referred_exception(self.referral_id)
        ex.cannot_refer_self(self.id, referral_id)

        self.referral_id = referral_id

    def add_loyalty_points(
        self,
        transaction_type: pmt_mdl.TransactionType,
        transaction_amount: int,
        weightage: Weightage,
    ):
        """Add loyalty points to user account for P2P_PUSH, P2P_PULL, and PAYMENT_GATEWAY transaction type"""

        if transaction_type == pmt_mdl.TransactionType.CASH_BACK:
            return

        ex.not_verified_exception(self.marketing_user_verified)
        ex.negative_amount_exception(transaction_amount)
        ex.invalid_transaction_type_exception(transaction_type, weightage.weightage_type)

        self.loyalty_points += math.floor(
            transaction_amount * weightage.weightage_value
        )

    def verify_user(self):
        """for testing purposes"""
        self.marketing_user_verified = True


@dataclass
class CashbackCalculator:
    all_cashbacks: AllCashbacks

    def calculate_cashback(
        self,
        deposit_amount: int,
        invoker_transaction_type: pmt_mdl.TransactionType,
    ) -> int:
        """Calculate cashback for the passed deposit amount"""

        # ex.not_verified_exception(self.marketing_user_verified)
        ex.negative_amount_exception(deposit_amount)
        ex.not_deposit_exception(invoker_transaction_type)

        # If deposit amount is greater than the last slab, then returned calculated cashback value should be 0
        if deposit_amount >= self.all_cashbacks.cashback_slabs[-1].end_amount:
            return 0

        else:
            eligible_slab = [
                slab
                for slab in self.all_cashbacks.cashback_slabs
                if deposit_amount >= slab.start_amount
                and deposit_amount < slab.end_amount
            ]
            slab = eligible_slab[0]

        if slab.cashback_type == CashbackType.PERCENTAGE:
            return math.floor(deposit_amount * slab.cashback_value)
        else:
            return math.floor(slab.cashback_value)
