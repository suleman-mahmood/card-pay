"""Authentication commands"""
import firebase_admin

from firebase_admin import auth
from typing import Optional, Tuple

from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.entrypoint import commands as payment_commands
from core.payment.entrypoint import queries as pmt_qry
from core.comms.entrypoint import commands as comms_commands
from core.api import utils
from core.api.event_codes import EventCode
from core.authentication.entrypoint import queries as qry
from core.authentication.entrypoint import exceptions as ex
from core.payment.domain import model as pmt_mdl
from core.authentication.domain import model as auth_mdl
from core.payment.domain import exceptions as pmt_domain_exc

PK_CODE = "92"
LUMS_CLOSED_LOOP_ID = "a3024e7d-e59c-4c65-8066-ab0349248d2b"


def create_closed_loop(
    name: str,
    logo_url: str,
    description: str,
    verification_type: str,
    regex: Optional[str],
    uow: AbstractUnitOfWork,
):
    """Create closed loop"""
    with uow:
        closed_loop = auth_mdl.ClosedLoop(
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
    phone_number: str,
    user_type: str,
    full_name: str,
    location: Tuple[float, float],
    uow: AbstractUnitOfWork,
) -> Tuple[EventCode, str]:
    """Create user"""
    location_object = auth_mdl.Location(latitude=location[0], longitude=location[1])

    # TODO: get these representations from PhoneNumber domain object instead
    phone_email = PK_CODE + phone_number + "@cardpay.com.pk"
    phone_number_with_country_code = "+" + PK_CODE + phone_number
    phone_number_sms = PK_CODE + phone_number

    user_already_exists = False
    firebase_uid = ""
    try:
        firebase_uid = firebase_create_user(
            phone_email=phone_email,
            phone_number=phone_number_with_country_code,
            password=password,
            full_name=full_name,
        )
    except:
        user_already_exists = True

    if not user_already_exists:
        user_id = utils.firebaseUidToUUID(firebase_uid)

        payment_commands.create_wallet(user_id=user_id, uow=uow)
        user = auth_mdl.User(
            id=user_id,
            personal_email=auth_mdl.PersonalEmail(value=personal_email),
            phone_number=auth_mdl.PhoneNumber(value=phone_number_with_country_code),
            user_type=auth_mdl.UserType.__members__[user_type],
            pin="0000",  # TODO: fix this
            full_name=full_name,
            wallet_id=user_id,
            location=location_object,
        )
        uow.users.add(user)

        if user.user_type is auth_mdl.UserType.CUSTOMER:
            comms_commands.send_otp_sms(
                full_name=user.full_name, to=phone_number_sms, otp_code=user.otp
            )

        return EventCode.OTP_SENT, user_id
    else:
        with uow:
            firebase_uid = firebase_get_user(email=phone_email)
            user_id = utils.firebaseUidToUUID(firebase_uid)
            fetched_user = uow.users.get(user_id=user_id)

            if fetched_user.is_phone_number_verified:
                return EventCode.USER_VERIFIED, user_id
            else:
                firebase_update_password(
                    firebase_uid=firebase_uid,
                    new_password=password,
                    new_full_name=full_name,
                )

                # Update user details
                user = auth_mdl.User(
                    id=user_id,
                    personal_email=auth_mdl.PersonalEmail(value=personal_email),
                    phone_number=auth_mdl.PhoneNumber(
                        value=phone_number_with_country_code
                    ),
                    user_type=auth_mdl.UserType.__members__[user_type],
                    pin="0000",  # TODO: fix this
                    full_name=full_name,
                    wallet_id=user_id,
                    location=location_object,
                )
                uow.users.save(user)

                if user.user_type is auth_mdl.UserType.CUSTOMER:
                    comms_commands.send_otp_sms(
                        full_name=fetched_user.full_name,
                        to=phone_number_sms,
                        otp_code=fetched_user.otp,
                    )
                return EventCode.OTP_SENT, user_id


def change_name(user_id: str, new_name: str, uow: AbstractUnitOfWork):
    """Change a user's name"""
    with uow:
        user = uow.users.get(user_id=user_id)
        user.change_name(new_name)
        uow.users.save(user)

    return user


def change_pin(user_id: str, new_pin: str, uow: AbstractUnitOfWork):
    """Change pin"""
    with uow:
        user = uow.users.get(user_id=user_id)
        user.set_pin(new_pin)
        uow.users.save(user)

    return user


def user_toggle_active(user_id: str, uow: AbstractUnitOfWork):
    """Toggle user active"""
    with uow:
        user = uow.users.get(user_id=user_id)
        user.toggle_active()
        uow.users.save(user)

    return user


def verify_otp(user_id: str, otp: str, uow: AbstractUnitOfWork):
    """Verify OTP"""
    with uow:
        user = uow.users.get(user_id=user_id)
        user.verify_otp(otp)
        uow.users.save(user)

    return user


def verify_phone_number(user_id: str, otp: str, uow: AbstractUnitOfWork):
    """Verify Phone Number"""
    with uow:
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

    if qry.verified_unique_identifier_already_exists(
        closed_loop_id=closed_loop_id,
        unique_identifier=unique_identifier,
        uow=uow,
    ):
        raise ex.UniqueIdentifierAlreadyExistsException(
            "This User already exists in this organization"
        )

    _register_closed_loop(
        user=user,
        closed_loop_id=closed_loop_id,
        unique_identifier=unique_identifier,
        uow=uow,
    )

    if user.user_type is auth_mdl.UserType.CUSTOMER:
        comms_commands.send_email(
            subject="Verify closed loop | Otp",
            text=user.closed_loops[closed_loop_id].unique_identifier_otp,
            to=f"{unique_identifier}@lums.edu.pk",  # TODO: fix this
        )

    return user


def verify_closed_loop(
    user_id: str,
    closed_loop_id: str,
    unique_identifier_otp: str,
    uow: AbstractUnitOfWork,
):
    """Request/Register to join a closed loop"""
    user = uow.users.get(user_id=user_id)

    assert not qry.verified_unique_identifier_already_exists(
        closed_loop_id=closed_loop_id,
        unique_identifier=user.closed_loops[closed_loop_id].unique_identifier,
        uow=uow,
    )

    user.verify_closed_loop(closed_loop_id=closed_loop_id, otp=unique_identifier_otp)
    uow.users.save(user)

    if closed_loop_id != LUMS_CLOSED_LOOP_ID:
        return user

    unique_identifier = user.closed_loops[closed_loop_id].unique_identifier
    assert unique_identifier is not None

    try:
        firestore_user_id = qry.user_id_from_firestore(
            unique_identifier=unique_identifier, uow=uow
        )
    except ex.UserNotInFirestore:
        # This is not an old LUMS user, so just return
        return user

    _migrate_user(user_id=user_id, firestore_user_id=firestore_user_id, uow=uow)

    return user


def _migrate_user(user_id: str, firestore_user_id: str, uow: AbstractUnitOfWork):
    fetched_wallet_balance = qry.wallet_balance_from_firestore(
        user_id=firestore_user_id, uow=uow
    )
    cardpay_wallet_id = pmt_qry.get_starred_wallet_id(uow=uow)

    try:
        payment_commands.execute_transaction(
            sender_wallet_id=cardpay_wallet_id,
            recipient_wallet_id=user_id,
            amount=fetched_wallet_balance,
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.CARD_PAY,
            uow=uow,
        )
    except pmt_domain_exc.TransactionNotAllowedException:
        pass

    sql = """
        update users_firestore
        set migrated=true
        where id=%(user_id)s;

        update wallets_firestore
        set migrated=true
        where id=%(user_id)s;
    """

    uow.cursor.execute(
        sql,
        {
            "user_id": firestore_user_id,
        },
    )


def firebase_create_user(
    phone_email: str,
    phone_number: str,
    password: str,
    full_name: str,
) -> str:
    user_record = firebase_admin.auth.create_user(
        email=phone_email,
        email_verified=False,
        phone_number=phone_number,
        password=password,
        display_name=full_name,
        disabled=False,
    )

    return user_record.uid


def firebase_update_password(firebase_uid: str, new_password: str, new_full_name: str):
    firebase_admin.auth.update_user(
        uid=firebase_uid,
        password=new_password,
        display_name=new_full_name,
    )


def firebase_get_user(email: str) -> str:
    user_record = auth.get_user_by_email(email=email)

    return user_record.uid


def create_vendor_through_retool(
    personal_email: str,
    password: str,
    phone_number: str,
    full_name: str,
    location: Tuple[float, float],
    closed_loop_id: str,
    unique_identifier: Optional[str],
    uow: AbstractUnitOfWork,
):
    """
    assumption: each vendor can only belong to a single closed loop
    """

    _, user_id = create_user(
        personal_email=personal_email,
        password=password,
        phone_number=phone_number,
        user_type="VENDOR",
        full_name=full_name,
        location=location,
        uow=uow,
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
    )

    return user


def auth_retools_update_closed_loop(
    closed_loop_id: str,
    name: str,
    logo_url: str,
    description: str,
    verification_type: str,
    regex: Optional[str],
    uow: AbstractUnitOfWork,
):
    """Update closed loop"""
    with uow:
        closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop_id)
        closed_loop.update_closed_loop(
            name=name,
            logo_url=logo_url,
            description=description,
        )
        uow.closed_loops.save(closed_loop)

    return closed_loop
