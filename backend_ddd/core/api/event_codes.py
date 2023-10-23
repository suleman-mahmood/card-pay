from enum import Enum


class EventCode(str, Enum):
    """event codes enum"""

    DEFAULT_EVENT = 1
    OTP_SENT = 2
    USER_VERIFIED = 3
    WAITER_QR_TRANSACTION_FAILED = 4
    WAITER_QR_KNOWN_FAILURE = 5
    WAITER_QR_UNKNOWN_FAILURE = 6
    WAITER_QR_TRANSACTION_SUCCESSFUL = 7