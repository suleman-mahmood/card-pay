from enum import Enum


class EventCode(str, Enum):
    """event codes enum"""

    DEFAULT_EVENT = 1
    OTP_SENT = 2
    USER_VERIFIED = 3