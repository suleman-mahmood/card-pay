"""Authentication commands"""
import firebase_admin

from firebase_admin import auth
from typing import Optional, Tuple

from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.entrypoint import commands as payment_commands
from core.comms.entrypoint import commands as comms_commands
from core.api import utils
from core.api.event_codes import EventCode
from ..domain.model import (
    ClosedLoopUser,
    ClosedLoopVerificationType,
    ClosedLoop,
    User,
    UserType,
    PersonalEmail,
    PhoneNumber,
    Location,
)

PK_CODE = "92"


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
        closed_loop = ClosedLoop(
            name=name,
            logo_url=logo_url,
            description=description,
            regex=regex,
            verification_type=ClosedLoopVerificationType.__members__[verification_type],
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
    location_object = Location(latitude=location[0], longitude=location[1])

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

        with uow:
            wallet = payment_commands.create_wallet(user_id=user_id, uow=uow)
            user = User(
                id=user_id,
                personal_email=PersonalEmail(value=personal_email),
                phone_number=PhoneNumber(value=phone_number_with_country_code),
                user_type=UserType.__members__[user_type],
                pin="0000",  # TODO: fix this
                full_name=full_name,
                wallet_id=wallet.id,
                location=location_object,
            )

            uow.users.add(user)

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


def register_closed_loop(
    user_id: str,
    closed_loop_id: str,
    unique_identifier: Optional[str],
    uow: AbstractUnitOfWork,
):
    """Request/Register to join a closed loop"""
    with uow:
        user = uow.users.get(user_id=user_id)
        closed_loop_user = ClosedLoopUser(
            closed_loop_id=closed_loop_id, unique_identifier=unique_identifier
        )
        user.register_closed_loop(closed_loop_user=closed_loop_user)
        uow.users.save(user)

    comms_commands.send_email(
        subject="Verify closed loop | Otp",
        text=user.otp,
        to=user.personal_email.value,
    )

    return user


def verify_closed_loop(
    user_id: str,
    closed_loop_id: str,
    unique_identifier_otp: str,
    uow: AbstractUnitOfWork,
):
    """Request/Register to join a closed loop"""
    with uow:
        user = uow.users.get(user_id=user_id)
        user.verify_closed_loop(
            closed_loop_id=closed_loop_id, otp=unique_identifier_otp
        )
        uow.users.save(user)

    return user


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


def firebase_get_user(email: str) -> str:
    user_record = auth.get_user_by_email(email=email)

    return user_record.uid
