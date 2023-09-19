class DepositAmountTooSmallException(Exception):
    """Deposit amount is less than the minimum allowed deposit"""


class InvalidQRCodeException(Exception):
    """exception raised for when a QR code is invalid"""


class InvalidUserTypeException(Exception):
    """exception raised for when a user type is invalid"""


class InvalidPayProCredentialsException(Exception):
    """PayPro credentials are invalid"""

class PaymentUrlNotFoundException(Exception):
    """exception raised for when payment url is not found"""

class NotVerifiedException(Exception):
    """User is not verified"""

class TransactionFailedException(Exception):
    """exception raised for when transaction fails"""

class InvalidQRVersionException(Exception):
    """QR version is invalid"""

class UserDoesNotExistException(Exception):
    """exception raised for when the user does not exist"""

class TransactionNotFound(Exception):
    """exception raised for when a transaction is not found"""
