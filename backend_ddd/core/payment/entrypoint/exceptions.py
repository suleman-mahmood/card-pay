class DepositAmountTooSmallException(Exception):
    """Deposit amount is less than the minimum allowed deposit"""


class InvalidQRCodeException(Exception):
    """exception raised for when a QR code is invalid"""

class InvalidUserTypeException(Exception):
    """exception raised for when a user type is invalid"""