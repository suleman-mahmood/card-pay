from random import randint


def _generate_4_digit_otp() -> str:
    """Generate 4 digit OTP"""
    return str(randint(1000, 9999))
