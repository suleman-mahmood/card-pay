class TransactionNotAllowedException(Exception):
    """exception raised for when a transaction is not allowed"""


class TransactionNotFoundException(Exception):
    """exception raised for when a transaction is not found"""


class DepositAmountTooSmallException(Exception):
    """Deposit amount is less than the minimum allowed deposit"""


class ReversingUnsuccessfulTransaction(Exception):
    """exception raised for when reversing (marking) a transaction is not successful"""


class NotDepositReversal(Exception):
    """exception raised for when reversing a non-deposit transaction"""


class UnmarkedDepositReversal(Exception):
    """exception raised for when reversing an unmarked deposit transaction"""


class InsufficientBalanceForReversal(Exception):
    """exception raised for when reversing a transaction with insufficient balance"""


class AlreadyMarkedToReverse(Exception):
    """exception raised for when tryin to mark a transaction already marked to reverse"""

class OfflineQrExpired(Exception):
    """Offline QR Code has expired"""
