
from ..domain.utils import DEFAULT_UUID
from ...payment.domain.model import TransactionType

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
    if transaction_type != TransactionType.PAYMENT_GATEWAY:
        raise InvalidTransactionTypeException(
            "Transaction Type is not deposit"
        )

# def invalid_weightage_passed_exception(weightage: Weightage):
#     if weightage.weightage_type != TransactionType.REFERRAL:
#         raise InvalidWeightageException(
#             "Invalid weightage type passed. Weightage type should be REFERRAL"
#         )


# def invalid_transaction_type_exception(transaction_type: TransactionType, weightage_type: TransactionType):
#     if transaction_type != weightage_type:
#         raise InvalidTrasnsactionTypeException(
#             "Passed transaction type and weightage type do not match"
#         )
