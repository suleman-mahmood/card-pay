class InvalidOtpException(Exception):
    """exception raised for when a user enters an incorrect otp"""

class ClosedLoopException(Exception):
    """exception raised for when a user enters an invalid closed loop"""

class VerificationException(Exception):
    """exception raised for when a user defies verification logic"""