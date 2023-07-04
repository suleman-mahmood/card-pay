class InvalidReferenceException(Exception):
    """exception raised for invalid reference"""


class InvalidWeightageException(Exception):
    """exception raised for invalid weightage"""


class InvalidTrasnsactionTypeException(Exception):
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


def _negative_amount_exception(amount: int):
    if amount < 0:
        raise NegativeAmountException(
            "Negative amount passed, amount cannot be negative"
        )

