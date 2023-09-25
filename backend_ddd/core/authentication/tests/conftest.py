"""Fixtures for seeding data for tests."""
from copy import deepcopy
from datetime import datetime
from typing import Tuple
from uuid import uuid4

import pytest
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import commands as auth_cmd
from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.domain import model as pmt_mdl


@pytest.fixture
def seed_user():
    def _seed_user() -> auth_mdl.User:
        uid = str(uuid4())

        return auth_mdl.User(
            id=uid,
            personal_email=auth_mdl.PersonalEmail(value="sulemanmahmood99@gmail.com"),
            user_type=auth_mdl.UserType.CUSTOMER,
            phone_number=auth_mdl.PhoneNumber(value="3000000000"),
            pin="0000",
            full_name="Suleman Mahmood",
            location=auth_mdl.Location(latitude=0, longitude=0),
            wallet_id=uid,
        )

    return _seed_user


@pytest.fixture
def seed_closed_loop():
    def _seed_closed_loop() -> auth_mdl.ClosedLoop:
        return auth_mdl.ClosedLoop(
            id=str(uuid4()),
            name="Test Loop",
            logo_url="https://www.google.com",
            description="This is a test loop.",
            regex="No regex yet",
            verification_type=auth_mdl.ClosedLoopVerificationType.ROLLNUMBER,
        )

    return _seed_closed_loop


@pytest.fixture
def seed_closed_loop_user():
    def _seed_closed_loop_user() -> auth_mdl.ClosedLoopUser:
        return auth_mdl.ClosedLoopUser(
            id=str(uuid4()),
            closed_loop_id=str(uuid4()),
            created_at=datetime.now(),
            status=auth_mdl.ClosedLoopUserState.UN_VERIFIED,
            unique_identifier=None,
            unique_identifier_otp="1234",
        )

    return _seed_closed_loop_user


@pytest.fixture
def seed_auth_user():
    def _seed_auth_user(
        uow: AbstractUnitOfWork,
    ) -> Tuple[auth_mdl.User, pmt_mdl.Wallet]:
        user_id = str(uuid4())
        user = auth_mdl.User(
            id=user_id,
            personal_email=auth_mdl.PersonalEmail(value="mlkmoaz@gmail.com"),
            phone_number=auth_mdl.PhoneNumber(value="03034952255"),
            user_type=auth_mdl.UserType.CUSTOMER,
            pin="0000",
            full_name="Malik Muhammad Moaz",
            location=auth_mdl.Location(latitude=13.2311, longitude=98.4888),
            wallet_id=user_id,
        )
        wallet: pmt_mdl.Wallet = pmt_mdl.Wallet(id=user_id, qr_id=str(uuid4()), balance=0)
        uow.transactions.add_wallet(
            wallet=wallet,
        )
        uow.users.add(user)

        return deepcopy(user), deepcopy(wallet)

    return _seed_auth_user


@pytest.fixture
def seed_verified_auth_user(seed_auth_user):
    def _seed_auth_user(
        uow: AbstractUnitOfWork,
    ) -> Tuple[auth_mdl.User, pmt_mdl.Wallet]:
        user, wallet = seed_auth_user(uow)
        auth_cmd.verify_phone_number(
            user_id=user.id,
            otp=user.otp,
            uow=uow,
        )
        return user, wallet

    return _seed_auth_user


@pytest.fixture
def seed_auth_closed_loop():
    def _seed_auth_closed_loop(id: str, uow: AbstractUnitOfWork):
        auth_cmd.create_closed_loop(
            id=id,
            name="Test Closed Loop",
            logo_url="https://test.com/logo.png",
            description="Test description",
            regex="No regex yet",
            verification_type="NONE",
            uow=uow,
        )

    return _seed_auth_closed_loop


@pytest.fixture
def seed_auth_vendor():
    def _seed_auth_vendor(
        uow: AbstractUnitOfWork,
    ) -> Tuple[auth_mdl.User, pmt_mdl.Wallet]:
        user_id = str(uuid4())
        user = auth_mdl.User(
            id=user_id,
            personal_email=auth_mdl.PersonalEmail(value="zainalikhokhar40@gmail.com"),
            phone_number=auth_mdl.PhoneNumber(value="+923123456789"),
            user_type=auth_mdl.UserType.VENDOR,
            pin="1234",
            full_name="Zain Ali Khokhar",
            location=auth_mdl.Location(latitude=0, longitude=0),
            wallet_id=user_id,
        )
        wallet = pmt_mdl.Wallet(id=user_id, qr_id=str(uuid4()), balance=0)
        uow.transactions.add_wallet(
            wallet=wallet,
        )
        uow.users.add(user)

        return user, wallet

    return _seed_auth_vendor


@pytest.fixture
def seed_verified_auth_vendor(seed_auth_vendor):
    def _seed_auth_vendor(
        uow: AbstractUnitOfWork,
    ) -> Tuple[auth_mdl.User, pmt_mdl.Wallet]:
        user, wallet = seed_auth_vendor(uow)
        auth_cmd.verify_phone_number(
            user_id=user.id,
            otp=user.otp,
            uow=uow,
        )
        return user, wallet

    return _seed_auth_vendor


# # work on this layta
# @pytest.fixture
# def seed_p2p_admin_customer_mocker_client():
#     def _seed_p2p_admin_customer_mocker_client(mocker, client):
#         sender_id = seed_api_customer(mocker, client)
#         recipient_id = seed_api_customer(mocker, client)
#         closed_loop_id = _create_closed_loop_helper(client)

#     headers = {
#         "Authorization": "Bearer pytest_auth_token",
#         "Content-Type": "application/json",
#     }

#     _verify_phone_number(recipient_id, mocker, client)
#     _verify_phone_number(sender_id, mocker, client)

#     _register_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, "26100274")
#     _register_user_in_closed_loop(
#         mocker, client, recipient_id, closed_loop_id, "26100290"
#     )

#     uow = UnitOfWork()
#     sender = uow.users.get(user_id=sender_id)
#     recipient = uow.users.get(user_id=recipient_id)
#     uow.close_connection()

#     otp = sender.closed_loops[closed_loop_id].unique_identifier_otp
#     _verify_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, otp)

#     otp = recipient.closed_loops[closed_loop_id].unique_identifier_otp
#     _verify_user_in_closed_loop(mocker, client, recipient_id, closed_loop_id, otp)

#     uow = UnitOfWork()
#     recipient_unique_identifier = auth_qry.get_unique_identifier_from_user_id(
#         user_id=recipient_id, uow=uow
#     )
#     sender_unique_identifier = auth_qry.get_unique_identifier_from_user_id(
#         user_id=sender_id, uow=uow
#     )
#     uow.transactions.add_1000_wallet(wallet_id=sender_id)
#     uow.commit_close_connection()

#     _marketing_setup(seed_api_admin, client, mocker, "P2P_PUSH", "10")

#     mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
#     response = client.post(
#         "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
#         json={
#             "recipient_unique_identifier": recipient_unique_identifier,
#             "amount": 100,
#             "closed_loop_id": closed_loop_id,
#         },
#         headers=headers,
#     )


@pytest.fixture
def seed_auth_cardpay():
    def _seed_auth_cardpay(uow: AbstractUnitOfWork) -> auth_mdl.User:
        user_id = str(uuid4())
        user = auth_mdl.User(
            id=user_id,
            personal_email=auth_mdl.PersonalEmail(value="cpay@gmail.com"),
            phone_number=auth_mdl.PhoneNumber(value="+923123456987"),
            user_type=auth_mdl.UserType.CARDPAY,
            pin="1234",
            full_name="Card Pay",
            location=auth_mdl.Location(latitude=0, longitude=0),
            wallet_id=user_id,
        )

        uow.transactions.add_wallet(
            wallet=pmt_mdl.Wallet(id=user_id, qr_id=str(uuid4()), balance=0)
        )
        uow.users.add(user)

        return user

    return _seed_auth_cardpay


@pytest.fixture
def seed_verified_auth_cardpay(seed_auth_cardpay):
    def _seed_auth_cardpay(uow: AbstractUnitOfWork) -> auth_mdl.User:
        user = seed_auth_cardpay(uow)
        auth_cmd.verify_phone_number(
            user_id=user.id,
            otp=user.otp,
            uow=uow,
        )
        return user

    return _seed_auth_cardpay
