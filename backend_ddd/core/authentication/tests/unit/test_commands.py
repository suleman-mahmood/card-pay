"""Unit tests for commands."""
import pytest
from core.entrypoint.uow import UnitOfWork
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.domain import model as auth_mdl
from core.authentication.domain import exceptions as auth_ex
from core.authentication.entrypoint import exceptions as auth_cmd_ex
from uuid import uuid4

def test_create_closed_loop(seed_auth_closed_loop):
    uow = UnitOfWork()
    closed_loop = seed_auth_closed_loop(uow)

    fetched_closed_loop = uow.closed_loops.get(closed_loop.id)

    assert fetched_closed_loop == closed_loop
    uow.close_connection()

def test_create_user(mocker):

    #create a new user
    #try to create an already created unverified user
    #try to create an already created verified user
    uow = UnitOfWork()
    uid = str(uuid4())

    mocker.patch("core.api.utils.firebaseUidToUUID", return_value=uid)
    auth_cmd.create_user(
        personal_email="abcd@efgh.com",
        password="abcd1234",
        phone_number="3000000000",
        user_type="CUSTOMER",
        full_name="Suleman Mahmood",
        location=(20.8752 , 56.2123,),
        uow=uow,
    )
    fetched_user = uow.users.get(user_id=uid)

    assert fetched_user.personal_email.value == "abcd@efgh.com"
    assert fetched_user.phone_number.value == "+923000000000"
    assert fetched_user.user_type.name == "CUSTOMER" 
    assert fetched_user.full_name == "Suleman Mahmood"
    assert fetched_user.location.latitude == 20.8752
    assert fetched_user.location.longitude == 56.2123
    
    #using the same phone number again to trip the exception
    mocker.patch("core.authentication.entrypoint.commands.firebase_create_user", side_effect=Exception("User already exists"))
    auth_cmd.create_user(
        personal_email="new@new.com",
        password="newpass123",
        phone_number="3000000000",
        user_type="CUSTOMER",
        full_name="New name",
        location=(20.8752 , 56.2123),
        uow=uow,
    )

    fetched_user = uow.users.get(user_id=uid)

    #assert that the details are updated
    assert fetched_user.personal_email.value == "new@new.com"
    assert fetched_user.phone_number.value == "+923000000000"
    assert fetched_user.user_type.name == "CUSTOMER" 
    assert fetched_user.full_name == "New name"
    assert fetched_user.location.latitude == 20.8752
    assert fetched_user.location.longitude == 56.2123

    auth_cmd.verify_phone_number(user_id=uid, otp=fetched_user.otp, uow=uow)

    auth_cmd.create_user(
        personal_email="new2@new2.com",
        password="new2pass123",
        phone_number="3000000000",
        user_type="CUSTOMER",
        full_name="Another Name",
        location=(20.8752 , 56.2123),
        uow=uow,
    )

    fetched_user = uow.users.get(user_id=uid)
    
    #assert that the details are not changed
    assert fetched_user.personal_email.value == "new@new.com"
    assert fetched_user.phone_number.value == "+923000000000"
    assert fetched_user.user_type.name == "CUSTOMER" 
    assert fetched_user.full_name == "New name"
    assert fetched_user.location.latitude == 20.8752
    assert fetched_user.location.longitude == 56.2123

def test_change_name(seed_auth_user):
    uow = UnitOfWork()
    user = seed_auth_user(uow)
    
    auth_cmd.change_name(user_id=user.id, new_name="New Name", uow=uow)

    fetched_user = uow.users.get(user_id=user.id)

    assert fetched_user.id == user.id
    assert fetched_user.full_name == "New Name"

    with pytest.raises(auth_ex.InvalidNameException, match = "empty name passed"):
        auth_cmd.change_name(user_id=user.id, new_name="", uow=uow)


def test_change_pin(seed_auth_user):
    uow = UnitOfWork()
    user = seed_auth_user(uow)
    
    auth_cmd.change_pin(user_id=user.id, new_pin="5678", uow=uow)

    fetched_user = uow.users.get(user_id=user.id)

    assert fetched_user.id == user.id
    assert fetched_user.pin == "5678"

    with pytest.raises(auth_ex.InvalidPinException, match="passed pin is same as old pin"):
        auth_cmd.change_pin(user_id=user.id, new_pin="5678", uow=uow)

    with pytest.raises(auth_ex.InvalidPinException, match="pin is not 4 digits long"):
        auth_cmd.change_pin(user_id=user.id, new_pin="56789", uow=uow)
        auth_cmd.change_pin(user_id=user.id, new_pin="567", uow=uow)

    with pytest.raises(auth_ex.InvalidPinException, match="pin contains non numeric characters"):
        auth_cmd.change_pin(user_id=user.id, new_pin="567a", uow=uow)

    with pytest.raises(auth_ex.InvalidPinException, match="forbidden pin passed"):
        auth_cmd.change_pin(user_id=user.id, new_pin="0000", uow=uow)

def test_user_toggle_active(seed_auth_user):
    uow = UnitOfWork()
    user = seed_auth_user(uow)

    auth_cmd.user_toggle_active(user_id=user.id, uow=uow)
    
    fetched_user = uow.users.get(user_id=user.id)

    assert fetched_user.id == user.id
    assert fetched_user.is_active == (not user.is_active)


def test_verify_otp(seed_auth_user):
    uow = UnitOfWork()
    user = seed_auth_user(uow)

    otp = user.otp
    wrong_otp = "0000"

    with pytest.raises(auth_ex.InvalidOtpException, match="Otps don't match"):
        auth_cmd.verify_otp(user_id=user.id, otp=wrong_otp, uow=uow)

    assert auth_cmd.verify_otp(user_id=user.id, otp=otp, uow=uow)

def test_verify_phone_number(seed_auth_user):
    uow = UnitOfWork()
    user = seed_auth_user(uow)
    otp = user.otp

    auth_cmd.verify_phone_number(user_id=user.id, otp=otp, uow=uow)

    assert uow.users.get(user.id).is_phone_number_verified

    with pytest.raises(auth_ex.VerificationException, match = "Phone number already verified"):
        auth_cmd.verify_phone_number(user_id=user.id, otp=otp, uow=uow)


def test_register_closed_loop(seed_auth_user, seed_auth_closed_loop):
    uow = UnitOfWork()
    user = seed_auth_user(uow)
    user_2 = seed_auth_user(uow)
    closed_loop = seed_auth_closed_loop(uow)
    closed_loop_2 = seed_auth_closed_loop(uow)

    auth_cmd.register_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop.id,
        unique_identifier=None,
        uow=uow,
    )

    fetched_user = uow.users.get(user_id=user.id)

    assert fetched_user.closed_loops[closed_loop.id].closed_loop_id == closed_loop.id

    auth_cmd.register_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop_2.id,
        unique_identifier="26100233",
        uow=uow,
    )

    fetched_user = uow.users.get(user_id=user.id)

    assert fetched_user.closed_loops[closed_loop_2.id].closed_loop_id == closed_loop_2.id

    #successfully register user_2 in closed_loop_2 with the same unique identifier since user is unverified
    auth_cmd.register_closed_loop(
        user_id=user_2.id,
        closed_loop_id=closed_loop_2.id,
        unique_identifier="26100233",
        uow=uow,
    )

    fetched_user = uow.users.get(user_id=user_2.id)

    assert fetched_user.closed_loops[closed_loop_2.id].closed_loop_id == closed_loop_2.id

    auth_cmd.verify_closed_loop(
        user_id=user_2.id,
        closed_loop_id=closed_loop_2.id,
        unique_identifier_otp=fetched_user.closed_loops[closed_loop_2.id].unique_identifier_otp,
        uow=uow,
    )

    #another user with the same unique identifier tries to register in closed_loop_2
    with pytest.raises(auth_cmd_ex.UniqueIdentifierAlreadyExistsException, match="This User already exists in this organization"):
        auth_cmd.register_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop_2.id,
            unique_identifier="26100233",
            uow=uow,
        )


def test_verify_closed_loop(seed_auth_user, seed_auth_closed_loop):
    #closed loop not found, verifiaction error
    
    uow = UnitOfWork()
    user = seed_auth_user(uow)
    closed_loop = seed_auth_closed_loop(uow)

    auth_cmd.register_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop.id,
        unique_identifier="24100163",
        uow=uow,
    )

    fetched_user = uow.users.get(user_id=user.id)

    otp = fetched_user.closed_loops[closed_loop.id].unique_identifier_otp

    with pytest.raises(auth_ex.InvalidOtpException):
        auth_cmd.verify_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop.id,
            unique_identifier_otp="0000",
            uow=uow,
        )

    fetched_user = uow.users.get(user_id=user.id)

    assert (
        fetched_user.closed_loops[closed_loop.id].status
        == auth_mdl.ClosedLoopUserState.UN_VERIFIED
    )

    auth_cmd.verify_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop.id,
        unique_identifier_otp=otp,
        uow=uow,
    )

    fetched_user = uow.users.get(user_id=user.id)

    assert (
        fetched_user.closed_loops[closed_loop.id].status
        == auth_mdl.ClosedLoopUserState.VERIFIED
    )

    #violate the invariant
    with pytest.raises(AssertionError):
        auth_cmd.verify_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop.id,
            unique_identifier_otp=otp,
            uow=uow,
        )
