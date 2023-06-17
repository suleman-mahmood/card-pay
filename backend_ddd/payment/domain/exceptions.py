class TransactionNotAllowedException(Exception):
    """exception raised for when a transaction is not allowed"""

class TransactionNotFoundException(Exception):
    """exception raised for when a transaction is not found"""