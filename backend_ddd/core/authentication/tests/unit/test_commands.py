"""Unit tests for commands."""
import pytest
from core.entrypoint.uow import FakeUnitOfWork
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.domain import model as auth_mdl
from core.authentication.domain import exceptions as auth_ex
from core.authentication.entrypoint import exceptions as auth_cmd_ex
from core.authentication.entrypoint import anti_corruption as acl
from uuid import uuid4


def test_create_closed_loop(seed_auth_closed_loop):
    uow = FakeUnitOfWork()
    closed_loop_id = str(uuid4())
    seed_auth_closed_loop(closed_loop_id, uow)

    fetched_closed_loop = uow.closed_loops.get(closed_loop_id)

    assert fetched_closed_loop.id == closed_loop_id
    uow.close_connection()


def test_create_user(mocker):
    # create a new user
    # try to create an already created unverified user
    # try to create an already created verified user
    uow = FakeUnitOfWork()
    uid = str(uuid4())
    pmt_svc = acl.FakePaymentService()

    mocker.patch("core.api.utils.firebaseUidToUUID", return_value=uid)
    auth_cmd.create_user(
        personal_email="abcd@efgh.com",
        password="abcd1234",
        raw_phone_number="3000000000",
        user_type="CUSTOMER",
        full_name="Suleman Mahmood",
        location=(
            20.8752,
            56.2123,
        ),
        uow=uow,
        fb_svc=acl.FakeFirebaseService(),
    )
    fetched_user = uow.users.get(user_id=uid)

    assert fetched_user.personal_email.value == "abcd@efgh.com"
    assert fetched_user.phone_number.value == "+923000000000"
    assert fetched_user.user_type.name == "CUSTOMER"
    assert fetched_user.full_name == "Suleman Mahmood"
    assert fetched_user.location.latitude == 20.8752
    assert fetched_user.location.longitude == 56.2123

    fake_fb_svc = acl.FakeFirebaseService()
    fake_fb_svc.set_user_exists(True)

    # using the same phone number again to trip the exception
    auth_cmd.create_user(
        personal_email="new@new.com",
        password="newpass123",
        raw_phone_number="3000000000",
        user_type="CUSTOMER",
        full_name="New name",
        location=(20.8752, 56.2123),
        uow=uow,
        fb_svc=fake_fb_svc,
    )

    fetched_user = uow.users.get(user_id=uid)

    # assert that the details are updated
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
        raw_phone_number="3000000000",
        user_type="CUSTOMER",
        full_name="Another Name",
        location=(20.8752, 56.2123),
        uow=uow,
        fb_svc=fake_fb_svc,
    )

    fetched_user = uow.users.get(user_id=uid)

    # assert that the details are not changed
    assert fetched_user.personal_email.value == "new@new.com"
    assert fetched_user.phone_number.value == "+923000000000"
    assert fetched_user.user_type.name == "CUSTOMER"
    assert fetched_user.full_name == "New name"
    assert fetched_user.location.latitude == 20.8752
    assert fetched_user.location.longitude == 56.2123


def test_change_name(seed_auth_user):
    uow = FakeUnitOfWork()
    user, _ = seed_auth_user(uow)

    auth_cmd.change_name(user_id=user.id, new_name="New Name", uow=uow)

    fetched_user = uow.users.get(user_id=user.id)

    assert fetched_user.id == user.id
    assert fetched_user.full_name == "New Name"

    with pytest.raises(auth_ex.InvalidNameException, match="empty name passed"):
        auth_cmd.change_name(user_id=user.id, new_name="", uow=uow)


def test_change_pin(seed_auth_user):
    uow = FakeUnitOfWork()
    user, _ = seed_auth_user(uow)

    auth_cmd.change_pin(user_id=user.id, new_pin="5678", uow=uow)

    fetched_user = uow.users.get(user_id=user.id)

    assert fetched_user.id == user.id
    assert fetched_user.pin == "5678"

    with pytest.raises(
        auth_ex.InvalidPinException, match="passed pin is same as old pin"
    ):
        auth_cmd.change_pin(user_id=user.id, new_pin="5678", uow=uow)

    with pytest.raises(auth_ex.InvalidPinException, match="pin is not 4 digits long"):
        auth_cmd.change_pin(user_id=user.id, new_pin="56789", uow=uow)
        auth_cmd.change_pin(user_id=user.id, new_pin="567", uow=uow)

    with pytest.raises(
        auth_ex.InvalidPinException, match="pin contains non numeric characters"
    ):
        auth_cmd.change_pin(user_id=user.id, new_pin="567a", uow=uow)

    with pytest.raises(auth_ex.InvalidPinException, match="forbidden pin passed"):
        auth_cmd.change_pin(user_id=user.id, new_pin="0000", uow=uow)


def test_user_toggle_active(seed_auth_user):
    uow = FakeUnitOfWork()
    user, _ = seed_auth_user(uow)

    auth_cmd.user_toggle_active(user_id=user.id, uow=uow)

    fetched_user = uow.users.get(user_id=user.id)

    assert fetched_user.id == user.id
    assert fetched_user.is_active == (not user.is_active)


def test_verify_phone_number(seed_auth_user):
    uow = FakeUnitOfWork()
    user, _ = seed_auth_user(uow)
    otp = user.otp

    auth_cmd.verify_phone_number(user_id=user.id, otp=otp, uow=uow)

    assert uow.users.get(user.id).is_phone_number_verified

    with pytest.raises(
        auth_ex.VerificationException, match="Phone number already verified"
    ):
        auth_cmd.verify_phone_number(user_id=user.id, otp=otp, uow=uow)


def test_register_closed_loopc(seed_auth_user, seed_auth_closed_loop):
    uow = FakeUnitOfWork()
    auth_svc = acl.FakeAuthenticationService()
    user, _ = seed_auth_user(uow)
    user_2, _ = seed_auth_user(uow)
    closed_loop_id = str(uuid4())
    closed_loop_2_id = str(uuid4())
    seed_auth_closed_loop(id=closed_loop_id, uow=uow)
    seed_auth_closed_loop(id=closed_loop_2_id, uow=uow)

    auth_cmd.register_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop_id,
        unique_identifier=None,
        uow=uow,
        auth_svc=auth_svc,
    )

    fetched_user = uow.users.get(user_id=user.id)

    assert fetched_user.closed_loops[closed_loop_id].closed_loop_id == closed_loop_id

    auth_cmd.register_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop_2_id,
        unique_identifier="26100233",
        uow=uow,
        auth_svc=auth_svc,
    )

    fetched_user = uow.users.get(user_id=user.id)

    assert (
        fetched_user.closed_loops[closed_loop_2_id].closed_loop_id == closed_loop_2_id
    )

    # successfully register user_2 in closed_loop_2 with the same unique identifier since user is unverified
    auth_cmd.register_closed_loop(
        user_id=user_2.id,
        closed_loop_id=closed_loop_2_id,
        unique_identifier="26100233",
        uow=uow,
        auth_svc=auth_svc,
    )

    fetched_user = uow.users.get(user_id=user_2.id)

    assert (
        fetched_user.closed_loops[closed_loop_2_id].closed_loop_id == closed_loop_2_id
    )

    auth_cmd.verify_closed_loop(
        user_id=user_2.id,
        closed_loop_id=closed_loop_2_id,
        unique_identifier_otp=fetched_user.closed_loops[
            closed_loop_2_id
        ].unique_identifier_otp,
        ignore_migration=False,
        uow=uow,
        auth_svc=auth_svc,
    )

    # another user with the same unique identifier tries to register in closed_loop_2
    auth_svc.set_verified_unique_identifier_already_exists(True)
    with pytest.raises(
        auth_cmd_ex.UniqueIdentifierAlreadyExistsException,
        match="This User already exists in this organization",
    ):
        auth_cmd.register_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop_2_id,
            unique_identifier="26100233",
            uow=uow,
            auth_svc=auth_svc,
        )


def test_verify_closed_loop(seed_auth_user, seed_auth_closed_loop):
    # closed loop not found, verifiaction error

    uow = FakeUnitOfWork()
    user, _ = seed_auth_user(uow)
    auth_svc = acl.FakeAuthenticationService()
    closed_loop_id = str(uuid4())
    seed_auth_closed_loop(id=closed_loop_id, uow=uow)

    auth_cmd.register_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop_id,
        unique_identifier="24100163",
        uow=uow,
        auth_svc=auth_svc,
    )

    fetched_user = uow.users.get(user_id=user.id)

    otp = fetched_user.closed_loops[closed_loop_id].unique_identifier_otp

    with pytest.raises(auth_ex.InvalidOtpException):
        auth_cmd.verify_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop_id,
            unique_identifier_otp="0000",
            ignore_migration=False,
            uow=uow,
            auth_svc=auth_svc,
        )

    fetched_user = uow.users.get(user_id=user.id)

    assert (
        fetched_user.closed_loops[closed_loop_id].status
        == auth_mdl.ClosedLoopUserState.UN_VERIFIED
    )

    auth_cmd.verify_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop_id,
        unique_identifier_otp=otp,
        ignore_migration=False,
        uow=uow,
        auth_svc=auth_svc,
    )

    fetched_user = uow.users.get(user_id=user.id)

    assert (
        fetched_user.closed_loops[closed_loop_id].status
        == auth_mdl.ClosedLoopUserState.VERIFIED
    )

    # violate the invariant
    auth_svc.set_verified_unique_identifier_already_exists(True)
    with pytest.raises(AssertionError):
        auth_cmd.verify_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop_id,
            unique_identifier_otp=otp,
            ignore_migration=False,
            uow=uow,
            auth_svc=auth_svc,
        )


def test_create_vendor(seed_auth_closed_loop, mocker):
    uow = FakeUnitOfWork()
    closed_loop_id = str(uuid4())
    seed_auth_closed_loop(closed_loop_id, uow)
    uid = str(uuid4())

    mocker.patch("core.api.utils.firebaseUidToUUID", return_value=uid)
    user_id, _ = auth_cmd.create_vendor_through_retool(
        personal_email="vendor@test.com",
        password="vendor1234",
        phone_number="3123456789",
        full_name="Vendor Name",
        location=(20.8752, 56.2123),
        closed_loop_id=closed_loop_id,
        unique_identifier=None,
        uow=uow,
        auth_svc=acl.FakeAuthenticationService(),
        fb_svc=acl.FakeFirebaseService(),
    )

    fetched_user = uow.users.get(user_id=user_id)

    assert fetched_user.personal_email.value == "vendor@test.com"
    assert fetched_user.phone_number.value == "+923123456789"
    assert fetched_user.user_type == auth_mdl.UserType.VENDOR
    assert fetched_user.full_name == "Vendor Name"
    assert fetched_user.location.latitude == 20.8752
    assert fetched_user.location.longitude == 56.2123
    assert fetched_user.closed_loops[closed_loop_id].closed_loop_id == closed_loop_id

    # vendor should be active and vendors closed loop account should be verified
    assert fetched_user.is_active == True
    assert fetched_user.is_phone_number_verified == True
    assert (
        fetched_user.closed_loops[closed_loop_id].status
        == auth_mdl.ClosedLoopUserState.VERIFIED
    )

    # creating a vendor with same phone number
    # since the vendor is verified, it should throw an exception and user detaild should not be updated
    fake_fb_svc = acl.FakeFirebaseService()
    fake_fb_svc.set_user_exists(True)

    with pytest.raises(
        auth_ex.VerificationException, match="Phone number already verified"
    ):
        auth_cmd.create_vendor_through_retool(
            personal_email="abc@abc.com",
            password="abc1234342",
            phone_number="3123456789",
            full_name="New Name",
            location=(10, 20),
            closed_loop_id=closed_loop_id,
            unique_identifier=None,
            uow=uow,
            auth_svc=acl.FakeAuthenticationService(),
            fb_svc=fake_fb_svc,
        )

    fetched_user = uow.users.get(user_id=user_id)

    assert fetched_user.personal_email.value == "vendor@test.com"
    assert fetched_user.phone_number.value == "+923123456789"
    assert fetched_user.user_type == auth_mdl.UserType.VENDOR
    assert fetched_user.full_name == "Vendor Name"
    assert fetched_user.location.latitude == 20.8752
    assert fetched_user.location.longitude == 56.2123
    assert fetched_user.closed_loops[closed_loop_id].closed_loop_id == closed_loop_id

    # vendor should be active and vendors closed loop account should be verified
    assert fetched_user.is_active == True
    assert fetched_user.is_phone_number_verified == True
    assert (
        fetched_user.closed_loops[closed_loop_id].status
        == auth_mdl.ClosedLoopUserState.VERIFIED
    )

    uow.close_connection()


def test_update_closed_loop(seed_auth_closed_loop):
    uow = FakeUnitOfWork()
    closed_loop_id = str(uuid4())
    seed_auth_closed_loop(closed_loop_id, uow)

    auth_cmd.auth_retools_update_closed_loop(
        closed_loop_id=closed_loop_id,
        name="Updated Name",
        logo_url="www.updated.com",
        description="Updated Description",
        uow=uow,
    )

    fetched_closed_loop = uow.closed_loops.get(closed_loop_id)

    assert fetched_closed_loop.name == "Updated Name"
    assert fetched_closed_loop.logo_url == "www.updated.com"
    assert fetched_closed_loop.description == "Updated Description"

    uow.close_connection()
