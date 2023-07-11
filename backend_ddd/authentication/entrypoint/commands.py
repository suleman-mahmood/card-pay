"""Authentication commands"""
from typing import Optional, Tuple

from backend_ddd.entrypoint.uow import AbstractUnitOfWork
from backend_ddd.payment.entrypoint import commands as payment_commands
from backend_ddd.comms.entrypoint import commands as comms_commands
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
    user_id: str,
    personal_email: str,
    phone_number: str,
    user_type: str,
    pin: str,
    full_name: str,
    location: Tuple[float, float],
    uow: AbstractUnitOfWork,
) -> User:
    """Create user"""
    location_object = Location(latitude=location[0], longitude=location[1])

    with uow:
        wallet = payment_commands.create_wallet(uow)
        user = User(
            id=user_id,
            personal_email=PersonalEmail(value=personal_email),
            phone_number=PhoneNumber(value=phone_number),
            user_type=UserType.__members__[user_type],
            pin=pin,
            full_name=full_name,
            wallet_id=wallet.id,
            location=location_object,
        )

        uow.users.add(user)

    comms_commands.send_sms(content=user.otp, to=phone_number)

    return user


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

    comms_commands.send_email(
        subject="Verify email | Otp",
        text=user.otp,
        to=user.personal_email,
    )

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
