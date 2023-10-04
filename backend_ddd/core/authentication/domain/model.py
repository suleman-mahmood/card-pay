"""
Authentication domain model
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
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Tuple
from uuid import uuid4

from core.authentication.domain import exceptions as ex
from core.authentication.domain.utils import _generate_4_digit_otp

PK_CODE = "92"


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
    regex: Optional[str]
    verification_type: ClosedLoopVerificationType

    created_at: datetime = field(default_factory=datetime.now)

    def update_closed_loop(
        self,
        name: str,
        logo_url: str,
        description: str,
    ) -> None:
        """Update closed loop"""
        self.name = name
        self.logo_url = logo_url
        self.description = description


class ClosedLoopUserState(str, Enum):
    """Closed loop enum"""

    UN_VERIFIED = 1
    VERIFIED = 2


@dataclass
class ClosedLoopUser:
    """Closed loop entity"""

    closed_loop_id: str
    unique_identifier: Optional[str]  # Roll number etc

    id: str = field(default_factory=lambda: str(uuid4()))
    unique_identifier_otp: str = field(default_factory=_generate_4_digit_otp)
    status: ClosedLoopUserState = ClosedLoopUserState.UN_VERIFIED
    created_at: datetime = field(default_factory=datetime.now)

    def verify_unique_identifier(self, otp: Optional[str]) -> None:
        """Verify unique identifier"""
        if self.status == ClosedLoopUserState.VERIFIED:
            raise ex.VerificationException("User is already in closed loop")

        if self.unique_identifier is not None and self.unique_identifier_otp != otp:
            raise ex.InvalidOtpException("Unique identifier otp doesn't match")

        self.status = ClosedLoopUserState.VERIFIED


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

    value: str  # +923333462677

    @property
    def email(self) -> str:
        return self.sms + "@cardpay.com.pk"

    @property
    def sms(self) -> str:
        return self.value.replace("+", "")

    @classmethod
    def from_api(cls, phone_number) -> "PhoneNumber":
        new_phone_number = "+" + PK_CODE + phone_number
        return PhoneNumber(value=new_phone_number)


@dataclass
class Location:
    """Location value object"""

    latitude: float
    longitude: float


@dataclass
class User:
    """
    User entity - Aggregate root
    """

    id: str  # Unique identifiers for the user
    personal_email: PersonalEmail
    phone_number: PhoneNumber
    user_type: UserType  # Previously role
    pin: str
    full_name: str
    wallet_id: str
    location: Location

    is_active: bool = True
    is_phone_number_verified: bool = False
    closed_loops: Dict[str, ClosedLoopUser] = field(default_factory=dict)
    otp: str = field(default_factory=_generate_4_digit_otp)
    otp_generated_at: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def qr_code(self) -> str:
        """QR code"""
        return self.id

    def change_name(self, name: str) -> None:
        """to change name"""
        if name == "":
            raise ex.InvalidNameException("empty name passed")

        self.full_name = name

    def set_pin(self, pin: str) -> None:
        """to set/update pin"""
        if len(pin) != 4:
            raise ex.InvalidPinException("pin is not 4 digits long")

        if pin == self.pin:
            raise ex.InvalidPinException("passed pin is same as old pin")

        if not pin.isnumeric():
            raise ex.InvalidPinException("pin contains non numeric characters")

        if pin == "0000":
            raise ex.InvalidPinException("forbidden pin passed")

        self.pin = pin

    def toggle_active(self) -> bool:
        """Toggle active"""
        self.is_active = not self.is_active

        return self.is_active

    def verify_otp(self, otp: str):
        """Verify OTP"""
        if self.otp != otp:
            raise ex.InvalidOtpException("Otps don't match")

        self._generate_new_otp()

    def _generate_new_otp(self) -> None:
        """Generate OTP"""
        self.otp = _generate_4_digit_otp()
        self.otp_generated_at = datetime.now()

    def verify_phone_number(self, otp: str) -> None:
        """Verify phone number"""
        # if phone number verified, raise exception
        if self.is_phone_number_verified:
            raise ex.VerificationException("Phone number already verified")

        self.verify_otp(otp)
        self.is_phone_number_verified = True

    def register_closed_loop(self, closed_loop_user: ClosedLoopUser) -> None:
        """Register closed loop"""
        self.closed_loops[closed_loop_user.closed_loop_id] = closed_loop_user

    def verify_closed_loop(self, closed_loop_id: str, otp: str) -> None:
        """Verify closed loop"""
        closed_loop_user = self.closed_loops.get(closed_loop_id)

        if not closed_loop_user:
            raise ex.ClosedLoopException("Closed loop not found")

        if closed_loop_user.status == ClosedLoopUserState.VERIFIED:
            raise ex.VerificationException("User is already verified")

        closed_loop_user.verify_unique_identifier(otp)

        self.closed_loops[closed_loop_id] = closed_loop_user
