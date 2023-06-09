"""authentication domain model"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime
from uuid import uuid4


def behaviour():
    """
    - Use Cases
        - create account
            - non-loop specific email for marketing etc
        - verify phone
        - login
        - verify email (aws)
        - forgot password (aws)
        - block card




        - guest sign up
    """


# @dataclass
class ClosedLoop:
    """Closed loop entity - Aggregate root"""

    id: str
    name: str
    logo_url: str
    description: str


class ClosedLoopUserState(str, Enum):
    """Closed loop enum"""

    UN_VERIFIED = 1
    PENDING = 2
    VERIFIED = 3


@dataclass
class ClosedLoopUser:
    """Closed loop entity - Aggregate root"""

    id: str
    closed_loop: ClosedLoop
    unique_identifier: Optional[str] = None  # Roll number etc
    unique_identifier_otp: str  # Four digit OTP

    created_at: datetime = datetime.now()
    status: ClosedLoopUserState = ClosedLoopUserState.UN_VERIFIED


class UserType(str, Enum):
    """User type enum"""

    CUSTOMER = 1  # Student, Faculty, Staff, etc.
    VENDOR = 2  # Shopkeeper, Society, Student Council etc.
    ADMIN = 3  # Admin of the closed loop system
    PAYMENT_GATEWAY = 4  # Payment gateway


# This can goto authentication domain
@dataclass
class User:
    """
    User entity - Aggregate root
    """

    # Unique identifiers for the user
    id: str
    personal_email: str
    forget_password_otp: str  # Four digit OTP

    closed_loops: List[ClosedLoopUser] = field(default_factory=list)

    qr_code: str
    pin: str
    wallet_id: str
    user_type: UserType  # Previously role
    phone_number: str = ""
    email: str = ""  # Personal email
    full_name: str = ""
    is_active: bool = True
