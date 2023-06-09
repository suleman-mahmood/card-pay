from dataclasses import dataclass, field
from typing import List
from enum import Enum
from datetime import datetime
from uuid import uuid4


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
    email_verification_otp: str  # Four digit OTP
    forget_password_otp: str  # Four digit OTP
    qr_code: str
    pin: str
    wallet_id: str
    user_type: UserType  # Previously role
    phone_number: str = ""
    email: str = ""  # Personal email
    full_name: str = ""
    is_active: bool = True
