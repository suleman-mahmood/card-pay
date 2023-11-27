class InvalidQRCodeException(Exception):
    """exception raised for when a QR code is invalid"""


class InvalidUserTypeException(Exception):
    """exception raised for when a user type is invalid"""


class InvalidPayProCredentialsException(Exception):
    """PayPro credentials are invalid"""


class PaymentUrlNotFoundException(Exception):
    """exception raised for when payment url is not found"""


class PayProsCreateOrderTimedOut(Exception):
    """PayPro's request timed out, retry again please!"""


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


class WalletNotExists(Exception):
    """The wallet does not exist"""


class CardPayWalletNotExists(Exception):
    """The CardPay wallet does not exist in starred wallets table"""


class NoUserDepositRequest(Exception):
    """User has no deposit requests"""


class NoNextReconciliationFound(Exception):
    """No next reconciliation found"""


class NoPreviousReconciliationFound(Exception):
    """No previous reconciliation found"""


class NoLatestReconciliationFound(Exception):
    """No Latest reconciliation found"""
<<<<<<< HEAD


class ConsumerAlreadyExists(Exception):
    """Consumer already exists"""


class ReversalFailedException(Exception):
    """exception raised for when reversal fails"""
=======
>>>>>>> 4b741a6e (incorporated comments and changed exceptions)
