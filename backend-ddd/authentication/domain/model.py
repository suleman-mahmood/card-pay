from dataclasses import dataclass


@dataclass
class User:
    """User entity"""

    id: str
    email_verification_otp: str = ""  # Four digit OTP
    forget_password_otp: str = ""  # Four digit OTP
