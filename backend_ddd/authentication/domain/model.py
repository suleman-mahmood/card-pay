"""authentication domain model"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime
from .utils import _generate_4_digit_otp
from .exceptions import InvalidOtpException


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


class ClosedLoopVerificationType(str, Enum):
    """Closed loop verification type"""

    NONE = 1
    ROLLNUMBER = 2
    EMAIL = 3
    MEMBERSHIP_ID = 4


@dataclass
class ClosedLoop:
    """Closed loop entity - Aggregate root"""

    id: str
    name: str
    logo_url: str
    description: str
    verification_type: ClosedLoopVerificationType


class ClosedLoopUserState(str, Enum):
    """Closed loop enum"""

    UN_VERIFIED = 1
    PENDING = 2
    VERIFIED = 3


@dataclass
class ClosedLoopUser:
    """Closed loop entity"""

    id: str
    closed_loop_id: str

    unique_identifier: Optional[str] = None  # Roll number etc
    unique_identifier_otp: str = field(default_factory=_generate_4_digit_otp)
    status: ClosedLoopUserState = ClosedLoopUserState.UN_VERIFIED
    created_at: datetime = datetime.now()


class UserType(str, Enum):
    """User type enum"""

    CUSTOMER = 1  # Student, Faculty, Staff, etc.
    VENDOR = 2  # Shopkeeper, Society, Student Council etc.
    ADMIN = 3  # Admin of the closed loop system
    PAYMENT_GATEWAY = 4  # Payment gateway
    CARDPAY = 5  # Cardpay


@dataclass(frozen=True)
class PersonalEmail:
    """Personal email value object"""

    value: str


@dataclass(frozen=True)
class PhoneNumber:
    """Phone number value object"""

    value: str


@dataclass
class User:
    """
    User entity - Aggregate root
    """

    # Unique identifiers for the user
    id: str
    personal_email: PersonalEmail
    phone_number: PhoneNumber
    user_type: UserType  # Previously role
    pin: str
    full_name: str
    wallet_id: str

    is_active: bool = True
    is_phone_number_verified: bool = False
    closed_loops: List[ClosedLoopUser] = field(default_factory=list)  # use dict here?

    otp: str = field(default_factory=_generate_4_digit_otp)
    otp_generated_at: datetime = field(default_factory=datetime.now)

    @property
    def qr_code(self) -> str:
        """QR code"""
        return self.id

    def register_closed_loop(self, closed_loop_user: ClosedLoopUser) -> None:
        """Register closed loop"""
        self.closed_loops.append(closed_loop_user)

    # def verify_closed_loop(self, )

    def change_name(self, name: str) -> None:
        """to change name"""
        self.full_name = name

    def set_pin(self, pin: str) -> None:
        """to set/update pin"""
        self.pin = pin

    def toggle_active(self) -> bool:
        """Toggle active"""
        self.is_active = not self.is_active

        return self.is_active

    def verify_otp(self, otp: str) -> bool:
        """Verify OTP"""
        if self.otp != otp:
            raise InvalidOtpException("Otps don't match")

        self.generate_new_otp()
        return True

    def verify_phone_number(self, otp: str) -> None:
        """Verify phone number"""
        if self.verify_otp(otp):
            self.is_phone_number_verified = True

    def generate_new_otp(self) -> None:
        """Generate OTP"""
        self.otp = _generate_4_digit_otp()
        self.otp_generated_at = datetime.now()
