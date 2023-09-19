
from core.marketing.domain.utils import DEFAULT_UUID
from core.payment.domain import model as pmt_mdl


class InvalidReferenceException(Exception):
    """exception raised for invalid reference"""


class InvalidWeightageException(Exception):
    """exception raised for invalid weightage"""


class InvalidTransactionTypeException(Exception):
    """exception raised for invalid transaction type"""


class InvalidCashbackTypeException(Exception):
    """exception raised for invalid cashback type"""


class NegativeAmountException(Exception):
    """exception raised for negative amount"""


class InvalidAddingLoyaltyPointsException(Exception):
    """exception raised for invalid adding loyality points"""


class InvalidSlabException(Exception):
    """exception raised for invalid slab"""


class NotVerifiedException(Exception):
    """exception raised for user not verified"""

class WeightageNotFoundException(Exception):
    """exception raised for missing weightage"""

def negative_amount_exception(amount: int):
    if amount < 0:
        raise NegativeAmountException(
            "Negative amount passed, amount cannot be negative"
        )


def not_verified_exception(marketing_user_verified: bool):
    if not marketing_user_verified:
        raise NotVerifiedException(
            "User is not verified"
        )


def referee_not_verified_exception(referee_verified: bool):
    if not referee_verified:
        raise InvalidReferenceException(
            "Referee is not verified"
        )


def user_already_referred_exception(referral_id: str):
    if referral_id != DEFAULT_UUID:
        raise InvalidReferenceException(
            "User has already been referred"
        )


def cannot_refer_self(self_id: str, referral_id: str):
    if self_id == referral_id:
        raise InvalidReferenceException(
            "User cannot refer themselves"
        )


def not_deposit_exception(transaction_type: str):
    if transaction_type != pmt_mdl.TransactionType.PAYMENT_GATEWAY:
        raise InvalidTransactionTypeException(
            "Transaction Type is not deposit"
        )


def invalid_weightage_passed_exception(weightage_type: pmt_mdl.TransactionType):
    if weightage_type != pmt_mdl.TransactionType.REFERRAL:
        raise InvalidWeightageException(
            "Invalid weightage type passed. Weightage type should be REFERRAL"
        )


def invalid_transaction_type_exception(transaction_type: pmt_mdl.TransactionType, weightage_type: pmt_mdl.TransactionType):
    if transaction_type != weightage_type:
        raise InvalidTransactionTypeException(
            "Passed transaction type and weightage type do not match"
        )

# AllCashbacks exceptions
def slab_ending_amount_lesser_than_or_equal_to_slab_starting_amount_exception(slab_ending_amount: float, slab_starting_amount: float):
    if slab_ending_amount <= slab_starting_amount:
        raise InvalidSlabException(
            "ending amount is smaller than starting amount"
        )


def slab_cashback_value_is_negative_exception(slab_cashback_value: float):
    if slab_cashback_value < 0:
        raise InvalidSlabException(
            "Cashback value is negative"
        )


def slab_not_continuos_exception(next_slab_starting_amount: float, current_slab_ending_amount: float):
    if next_slab_starting_amount != current_slab_ending_amount:
        raise InvalidSlabException(
            "Slabs are not continuous"
        )


# _handle_invalid_slabs exceptions
def empty_slabs_exception(slabs_len: int):
    if slabs_len == 0:
        raise InvalidSlabException(
            "Cashback slabs cannot be empty"
        )

# Weightage exceptions
def negative_weightage_exception(weightage_value: float):
    if (weightage_value < 0):
        raise InvalidWeightageException(
            "Negative weightage value passed, weightage value cannot be negative"
        )
