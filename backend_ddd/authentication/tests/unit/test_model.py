import pytest
from ...domain.model import (
    User,
    ClosedLoop,
    ClosedLoopUser,
    ClosedLoopUserState,
    UserType,
)
from ...domain.exceptions import InvalidOtpException
from uuid import uuid4


def test_users_have_unique_otps(seed_user):
    """Test create user"""
    user1 = seed_user()
    user2 = seed_user()

    assert user1.otp != user2.otp
    assert user1.qr_code != user2.qr_code


def test_user_verified_otp(seed_user):
    """Test user verified otp"""
    user = seed_user()
    otp = user.otp

    with pytest.raises(InvalidOtpException) as e_info:
        user.verify_otp(otp="0000")
        assert str(e_info.value) == "Otps don't match"

    assert user.verify_otp(otp=otp)

    # Test that the otp changes upon validation
    with pytest.raises(InvalidOtpException) as e_info:
        user.verify_otp(otp=otp)
        assert str(e_info.value) == "Otps don't match"


def test_deactivate_user():
    """Test deactivate user"""


def test_change_name():
    """Test change name"""


def test_change_pin():
    """Test change pin"""


def test_verify_phone_number():
    """Test verify phone number"""


def test_register_closed_loop():
    """Test register closed loop"""


def test_verify_closed_loop():
    """Test verify closed loop"""
