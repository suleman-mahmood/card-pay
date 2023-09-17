"""tests for authentication model"""

from uuid import uuid4
import pytest
from ...domain.model import (
    User,
    ClosedLoop,
    ClosedLoopVerificationType,
    ClosedLoopUser,
    ClosedLoopUserState,
    UserType,
)
from ...domain.exceptions import InvalidOtpException


def test_users_have_unique_otps(seed_user):  # why are we testing this?
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

    user.verify_otp(otp=otp)

    # Test that the otp changes upon validation
    with pytest.raises(InvalidOtpException) as e_info:
        user.verify_otp(otp=otp)
        assert str(e_info.value) == "Otps don't match"


def test_deactivate_user(seed_user):  # new method?
    """Test deactivate user"""
    user = seed_user()
    user.toggle_active()

    assert user.is_active is False


def test_change_name(seed_user):  # new method?
    """Test change name"""
    user = seed_user()
    new_name = "Malik M. Moaz"
    user.change_name(new_name)

    assert user.full_name == new_name


def test_change_pin(seed_user):
    """Test change pin"""
    user = seed_user()
    new_pin = "1234"
    user.set_pin(new_pin)

    assert user.pin == new_pin


def test_verify_phone_number(seed_user):  # how will phone number be verified?
    """Test verify phone number"""
    user = seed_user()
    otp = user.otp

    user.verify_phone_number(otp=otp)

    assert user.is_phone_number_verified is True


def test_register_open_closed_loop(seed_user, seed_closed_loop):
    """Test user tries to join closed loop"""
    user = seed_user()
    closed_loop = seed_closed_loop()
    closed_loop_user = ClosedLoopUser(
        closed_loop_id=closed_loop.id,
        unique_identifier=None,
    )

    closed_loop_user.verify_unique_identifier(otp=None)
    user.register_closed_loop(closed_loop_user)

    assert len(user.closed_loops) == 1
    assert user.closed_loops[closed_loop.id].closed_loop_id == closed_loop.id
    assert user.closed_loops[closed_loop.id].status == ClosedLoopUserState.VERIFIED


def test_register_closed_loop(seed_user, seed_closed_loop):
    """Test user tries to join closed loop"""
    user = seed_user()
    closed_loop = seed_closed_loop()
    closed_loop_user = ClosedLoopUser(
        closed_loop_id=closed_loop.id,
        unique_identifier="1234567890",
    )

    user.register_closed_loop(closed_loop_user)

    assert len(user.closed_loops) == 1
    assert user.closed_loops[closed_loop.id].closed_loop_id == closed_loop.id
    assert user.closed_loops[closed_loop.id].status == ClosedLoopUserState.UN_VERIFIED


def test_verify_closed_loop(seed_user, seed_closed_loop):
    """Test verify closed loop"""
    user = seed_user()
    closed_loop = seed_closed_loop()
    closed_loop_user = ClosedLoopUser(
        closed_loop_id=closed_loop.id,
        unique_identifier="1234567890",
    )

    user.register_closed_loop(closed_loop_user)

    otp = closed_loop_user.unique_identifier_otp

    user.verify_closed_loop(closed_loop_id=closed_loop.id, otp=otp)

    assert user.closed_loops[closed_loop.id].status == ClosedLoopUserState.VERIFIED
