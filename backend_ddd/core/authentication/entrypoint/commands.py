"""Authentication commands"""
from typing import Optional, Tuple

from core.entrypoint.uow import AbstractUnitOfWork
from core.comms.entrypoint import commands as comms_cmd
from core.api import utils
from core.api.event_codes import EventCode
from core.authentication.entrypoint import exceptions as svc_ex
from core.payment.entrypoint import commands as pmt_cmd
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import anti_corruption as acl

LUMS_CLOSED_LOOP_ID = "f23a19c5-040c-4924-830d-d1b687238c2b"
PAYPRO_USER_ID = "bd85b580-9510-4596-afc4-b737eeb3d492"


def create_closed_loop(
    id: str,
    name: str,
    logo_url: str,
    description: str,
    verification_type: str,
    regex: Optional[str],
    uow: AbstractUnitOfWork,
):
    """Create closed loop"""
    closed_loop = auth_mdl.ClosedLoop(
        id=id,
        name=name,
        logo_url=logo_url,
        description=description,
        regex=regex,
        verification_type=auth_mdl.ClosedLoopVerificationType.__members__[
            verification_type
        ],
    )
    uow.closed_loops.add(closed_loop)

    return closed_loop


def create_user(
    personal_email: str,
    password: str,
    raw_phone_number: str,
    user_type: str,
    full_name: str,
    location: Tuple[float, float],
    uow: AbstractUnitOfWork,
    fb_svc: acl.AbstractFirebaseService,
) -> Tuple[EventCode, str, bool]:
    """Create user"""
    location_object = auth_mdl.Location(latitude=location[0], longitude=location[1])
    phone_number = auth_mdl.PhoneNumber.from_api(phone_number=raw_phone_number)

    user_already_exists = False
    firebase_uid = ""
    try:
        firebase_uid = fb_svc.create_user(
            phone_email=phone_number.email,
            phone_number=phone_number.value,
            password=password,
            full_name=full_name,
        )
    except:
        user_already_exists = True

    if not user_already_exists:
        user_id = utils.firebaseUidToUUID(firebase_uid)
        pmt_cmd.create_wallet(user_id=user_id, uow=uow)
        user = auth_mdl.User(
            id=user_id,
            personal_email=auth_mdl.PersonalEmail(value=personal_email),
            phone_number=phone_number,
            user_type=auth_mdl.UserType.__members__[user_type],
            pin="0000",
            full_name=full_name,
            wallet_id=user_id,
            location=location_object,
        )
        uow.users.add(user)

        if user.user_type is auth_mdl.UserType.CUSTOMER:
            comms_cmd.send_otp_sms(
                full_name=user.full_name,
                to=phone_number.sms,
                otp_code=user.otp,
            )

        return EventCode.OTP_SENT, user_id, True
    else:
        firebase_uid = fb_svc.get_user(email=phone_number.email)
        user_id = utils.firebaseUidToUUID(firebase_uid)
        fetched_user = uow.users.get(user_id=user_id)

        if fetched_user.is_phone_number_verified:
            return EventCode.USER_VERIFIED, user_id, False
        else:
            fb_svc.update_password(
                firebase_uid=firebase_uid,
                new_password=password,
                new_full_name=full_name,
            )

            # Update user details
            user = auth_mdl.User(
                id=user_id,
                personal_email=auth_mdl.PersonalEmail(value=personal_email),
                phone_number=phone_number,
                user_type=auth_mdl.UserType.__members__[user_type],
                pin="0000",
                full_name=full_name,
                wallet_id=user_id,
                location=location_object,
            )
            uow.users.save(user)

            if user.user_type is auth_mdl.UserType.CUSTOMER:
                comms_cmd.send_otp_sms(
                    full_name=fetched_user.full_name,
                    to=phone_number.sms,
                    otp_code=fetched_user.otp,
                )
            return EventCode.OTP_SENT, user_id, False


def change_name(user_id: str, new_name: str, uow: AbstractUnitOfWork):
    """Change a user's name"""
    user = uow.users.get(user_id=user_id)
    user.change_name(new_name)
    uow.users.save(user)

    return user


def change_pin(user_id: str, new_pin: str, uow: AbstractUnitOfWork):
    """Change pin"""
    user = uow.users.get(user_id=user_id)
    user.set_pin(new_pin)
    uow.users.save(user)

    return user


def user_toggle_active(user_id: str, uow: AbstractUnitOfWork):
    """Toggle user active"""
    user = uow.users.get(user_id=user_id)
    user.toggle_active()
    uow.users.save(user)

    return user


def verify_phone_number(user_id: str, otp: str, uow: AbstractUnitOfWork):
    """Verify Phone Number"""
    user = uow.users.get(user_id=user_id)
    user.verify_phone_number(otp)
    uow.users.save(user)

    return user


def _register_closed_loop(
    user: auth_mdl.User,
    closed_loop_id: str,
    unique_identifier: Optional[str],
    uow: AbstractUnitOfWork,
):
    closed_loop_user = auth_mdl.ClosedLoopUser(
        closed_loop_id=closed_loop_id, unique_identifier=unique_identifier
    )
    user.register_closed_loop(closed_loop_user=closed_loop_user)
    uow.users.save(user)


def register_closed_loop(
    user_id: str,
    closed_loop_id: str,
    unique_identifier: Optional[str],
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
):
    """Request/Register to join a closed loop.
    Invariant: Multiple unverified closed_loop_users in a single closed loop with the same unique identifier can exist.
    """

    user = uow.users.get(user_id=user_id)

    if unique_identifier is None:
        _register_closed_loop(
            user=user,
            closed_loop_id=closed_loop_id,
            unique_identifier=unique_identifier,
            uow=uow,
        )
        return user

    if auth_svc.verified_unique_identifier_already_exists(
        closed_loop_id=closed_loop_id,
        unique_identifier=unique_identifier,
        uow=uow,
    ):
        raise svc_ex.UniqueIdentifierAlreadyExistsException(
            "This User already exists in this organization"
        )

    _register_closed_loop(
        user=user,
        closed_loop_id=closed_loop_id,
        unique_identifier=unique_identifier,
        uow=uow,
    )

    if user.user_type is auth_mdl.UserType.CUSTOMER:
        comms_cmd.send_email(
            subject="Verify closed loop | Otp",
            text=user.closed_loops[closed_loop_id].unique_identifier_otp,
            to=f"{unique_identifier}@lums.edu.pk",  # TODO: fix this
        )

    return user


def verify_closed_loop(
    user_id: str,
    closed_loop_id: str,
    unique_identifier_otp: str,
    ignore_migration: bool,
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
) -> Tuple[bool, int]:
    """Request/Register to join a closed loop"""
    user = uow.users.get(user_id=user_id)

    assert not auth_svc.verified_unique_identifier_already_exists(
        closed_loop_id=closed_loop_id,
        unique_identifier=user.closed_loops[closed_loop_id].unique_identifier,
        uow=uow,
    )

    user.verify_closed_loop(closed_loop_id=closed_loop_id, otp=unique_identifier_otp)
    uow.users.save(user)

    if closed_loop_id != LUMS_CLOSED_LOOP_ID or ignore_migration:
        return False, 0

    unique_identifier = user.closed_loops[closed_loop_id].unique_identifier
    assert unique_identifier is not None

    try:
        firestore_user_id = auth_svc.user_id_from_firestore(
            unique_identifier=unique_identifier, uow=uow
        )
    except svc_ex.UserNotInFirestore:
        # This is not an old LUMS user, so just return
        return False, 0

    sql = """
        update users_firestore
        set migrated=true
        where id=%(user_id)s;

        update wallets_firestore
        set migrated=true
        where id=%(user_id)s;
    """

    uow.dict_cursor.execute(sql, {"user_id": firestore_user_id})

    try:
        fetched_wallet_balance = auth_svc.wallet_balance_from_firestore(
            user_id=firestore_user_id, uow=uow
        )
    except svc_ex.WalletNotInFirestore:
        return False, 0

    return True, fetched_wallet_balance


def create_vendor_through_retool(
    personal_email: str,
    password: str,
    phone_number: str,
    full_name: str,
    location: Tuple[float, float],
    closed_loop_id: str,
    unique_identifier: Optional[str],
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
    fb_svc: acl.AbstractFirebaseService,
) -> Tuple[str, bool]:
    """
    assumption: each vendor can only belong to a single closed loop
    """

    _, user_id, should_create_wallet = create_user(
        personal_email=personal_email,
        password=password,
        raw_phone_number=phone_number,
        user_type="VENDOR",
        full_name=full_name,
        location=location,
        uow=uow,
        fb_svc=fb_svc,
    )

    user = uow.users.get(user_id=user_id)

    user = verify_phone_number(
        user_id=user_id,
        otp=user.otp,
        uow=uow,
    )

    user = register_closed_loop(
        user_id=user_id,
        closed_loop_id=closed_loop_id,
        unique_identifier=unique_identifier,
        uow=uow,
        auth_svc=auth_svc,
    )

    otp = user.closed_loops[closed_loop_id].unique_identifier_otp
    verify_closed_loop(
        user_id=user_id,
        closed_loop_id=closed_loop_id,
        unique_identifier_otp=otp,
        ignore_migration=True,
        uow=uow,
        auth_svc=auth_svc,
    )

    return user_id, should_create_wallet


def auth_retools_update_closed_loop(
    closed_loop_id: str,
    name: str,
    logo_url: str,
    description: str,
    uow: AbstractUnitOfWork,
):
    """Update closed loop"""
    closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop_id)
    closed_loop.update_closed_loop(
        name=name,
        logo_url=logo_url,
        description=description,
    )
    uow.closed_loops.save(closed_loop)

    return closed_loop
