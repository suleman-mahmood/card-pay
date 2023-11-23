class TransactionNotAllowedException(Exception):
    """exception raised for when a transaction is not allowed"""


class TransactionNotFoundException(Exception):
    """exception raised for when a transaction is not found"""


class DepositAmountTooSmallException(Exception):
    """Deposit amount is less than the minimum allowed deposit"""
