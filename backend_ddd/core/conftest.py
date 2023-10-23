import os
from copy import deepcopy
from datetime import datetime
from random import randint
from typing import Tuple
from uuid import uuid4

import pytest
import sentry_sdk
from core.api.api import app as flask_app
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import anti_corruption as auth_acl
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.entrypoint.uow import AbstractUnitOfWork, FakeUnitOfWork, UnitOfWork
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import commands as pmt_cmd


@pytest.fixture(autouse=True)
def initialize_pytest_config(mocker):
    os.environ["DB_HOST"] = os.environ["DB_HOST_LOCAL"]
    os.environ["DB_NAME"] = os.environ["DB_NAME_LOCAL"]
    os.environ["DB_USER"] = os.environ["DB_USER_LOCAL"]
    os.environ["DB_PASSWORD"] = os.environ["DB_PASSWORD_LOCAL"]
    os.environ["DB_PORT"] = os.environ["DB_PORT_LOCAL"]

    os.environ["EMAIL_USER"] = ""
    os.environ["EMAIL_PASSWORD"] = ""

    # PayPro stuff
    os.environ["USERNAME"] = ""
    os.environ["CLIENT_ID"] = ""
    os.environ["CLIENT_SECRET"] = ""
    os.environ["PAYPRO_BASE_URL"] = ""
    os.environ["TOKEN_VALIDITY"] = ""

    os.environ["SMS_API_TOKEN"] = ""
    os.environ["SMS_API_SECRET"] = ""
    os.environ["RETOOL_SECRET"] = ""

    mocker.patch("core.comms.entrypoint.commands.send_otp_sms", return_value=None)
    mocker.patch("core.comms.entrypoint.commands.send_marketing_sms", return_value=None)
    mocker.patch("core.comms.entrypoint.commands.send_email", return_value=None)
    mocker.patch(
        "core.authentication.entrypoint.firebase_service.create_user",
        return_value=None,
    )
    mocker.patch(
        "core.authentication.entrypoint.firebase_service.update_password",
        return_value=None,
    )
    mocker.patch(
        "core.authentication.entrypoint.firebase_service.update_password_and_name",
        return_value=None,
    )
    mocker.patch("core.authentication.entrypoint.firebase_service.get_user", return_value="")


@pytest.fixture()
def app():
    app = flask_app
    sentry_sdk.init(transport=print)  # Disable the initialized sentry
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def _generate_random_raw_phone_number() -> str:
    return str(randint(3000000000, 3999999999))


@pytest.fixture()
def seed_api_customer():
    def _seed_api_user(mocker, client):
        user_id = str(uuid4())
        mocker.patch("core.api.utils.firebaseUidToUUID", return_value=user_id)

        client.post(
            "http://127.0.0.1:5000/api/v1/create-user",
            json={
                "personal_email": "26100279@lums.edu.pk",
                "password": "cardpay123",
                "phone_number": _generate_random_raw_phone_number(),
                "user_type": "CUSTOMER",
                "full_name": "Shaheer Ahmad",
                "location": [24.8607, 67.0011],
            },
        )

        return user_id

    return _seed_api_user

@pytest.fixture()
def seed_api_vendor():
    def _seed_api_vendor(mocker, client, closed_loop_id):
        SECRET_KEY = os.environ["RETOOL_SECRET"]
        phone_number = "3763045384"
        user_id = str(uuid4())
        mocker.patch("core.api.utils.firebaseUidToUUID", return_value=user_id)
        mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)

        client.post(
            "http://127.0.0.1:5000/api/v1/auth-retools-create-vendor",
            json={
                "personal_email": "zak@zak.com",
                "password": "cardpay123",
                "phone_number": phone_number,
                "full_name": "Zain Ali",
                "longitude": 24.8607,
                "latitude": 67.0011,
                "closed_loop_id": closed_loop_id,
                "RETOOL_SECRET": SECRET_KEY,
            }
        )

        return user_id

    return _seed_api_vendor


@pytest.fixture()
def seed_api_cardpay(seed_api_customer):
    def _seed_api_cardpay(mocker, client):
        user_id = seed_api_customer(mocker, client)

        uow = UnitOfWork()
        sql = """
            insert into starred_wallet_id (wallet_id)
            values (%(user_id)s);
        """
        uow.dict_cursor.execute(sql, {"user_id": user_id})
        uow.commit_close_connection()

        return user_id

    return _seed_api_cardpay


@pytest.fixture()
def seed_api_admin():
    def _seed_api_user(mocker, client):
        user_id = str(uuid4())
        mocker.patch("core.api.utils.firebaseUidToUUID", return_value=user_id)

        client.post(
            "http://127.0.0.1:5000/api/v1/create-user",
            json={
                "personal_email": "26100279@lums.edu.pk",
                "password": "cardpay123",
                "phone_number": "3269507526",
                "user_type": "ADMIN",
                "full_name": "Suleman Mahmood",
                "location": [24.8607, 67.0011],
            },
        )

        return user_id

    return _seed_api_user


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
def seed_auth_event_organizer():
    def _seed_auth_event_organizer(
        uow: AbstractUnitOfWork,
    ) -> auth_mdl.User:
        user_id = str(uuid4())
        user = auth_mdl.User(
            id=user_id,
            personal_email=auth_mdl.PersonalEmail(value="mlkmoaz@party.com"),
            phone_number=auth_mdl.PhoneNumber(value="+9230349522255"),
            user_type=auth_mdl.UserType.EVENT_ORGANIZER,
            pin="5877",
            full_name="Malik M. Moaz",
            location=auth_mdl.Location(latitude=0, longitude=0),
            wallet_id=user_id,
        )
        wallet = pmt_mdl.Wallet(id=user_id, qr_id=str(uuid4()), balance=0)
        uow.transactions.add_wallet(
            wallet=wallet,
        )
        uow.users.add(user)

        return user

    return _seed_auth_event_organizer


@pytest.fixture
def seed_verified_auth_event_organizer(seed_auth_event_organizer):
    def _seed_verified_auth_event_organizer(
        uow: AbstractUnitOfWork,
    ) -> auth_mdl.User:
        user = seed_auth_event_organizer(uow)
        auth_cmd.verify_phone_number(
            user_id=user.id,
            otp=user.otp,
            uow=uow,
        )
        return user

    return _seed_verified_auth_event_organizer


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
def seed_verified_auth_cardpay_fake(seed_auth_cardpay):
    def _seed_auth_cardpay(uow: AbstractUnitOfWork) -> auth_mdl.User:
        user = seed_auth_cardpay(uow)
        auth_cmd.verify_phone_number(
            user_id=user.id,
            otp=user.otp,
            uow=uow,
        )
        return user

    return _seed_auth_cardpay


@pytest.fixture
def seed_starred_wallet(add_1000_wallet):
    def _seed_starred_wallet(uow: AbstractUnitOfWork):
        user_id = str(uuid4())

        user = auth_mdl.User(
            id=user_id,
            personal_email=auth_mdl.PersonalEmail(value="mlkmoaz@gmail.com"),
            phone_number=auth_mdl.PhoneNumber(value="03269507423"),
            user_type=auth_mdl.UserType.CUSTOMER,
            pin="1234",
            full_name="CardPay",
            location=auth_mdl.Location(latitude=0, longitude=0),
            wallet_id=user_id,
            is_phone_number_verified=True,
        )

        pmt_cmd.create_wallet(user_id=user_id, uow=uow)
        uow.users.add(user)

        add_1000_wallet(wallet_id=user_id, uow=uow)

        delete_sql = """
            delete from starred_wallet_id
        """
        uow.cursor.execute(delete_sql)

        sql = """
            insert into starred_wallet_id
            values (%s)
        """
        uow.cursor.execute(sql, [user_id])
        return user_id

    return _seed_starred_wallet


@pytest.fixture
def add_1000_wallet():
    def add_1000_wallet_factory(uow: AbstractUnitOfWork, wallet_id: str):
        # update wallet balance
        sql = """
                update wallets
                set balance = %s
                where id=%s
            """
        uow.cursor.execute(
            sql,
            [
                1000,
                wallet_id,
            ],
        )

    return add_1000_wallet_factory


@pytest.fixture
def add_1000_wallet_fake():
    def add_1000_wallet_factory(uow: FakeUnitOfWork, wallet_id: str):
        # update wallet balance
        wallet = uow.transactions.wallets[wallet_id]
        wallet.balance += 1000
        uow.transactions.wallets[wallet_id] = wallet

    return add_1000_wallet_factory


# API TEST HELPER FUNCTIONS


def _create_closed_loop_helper(client):
    uow = UnitOfWork()
    closed_loop_id = str(uuid4())
    auth_cmd.create_closed_loop(
        id=closed_loop_id,
        name="LUMS",
        logo_url="sample/url",
        description="Harvard of Pakistan",
        verification_type="ROLLNUMBER",
        regex="[0-9]{8}",
        uow=uow,
    )
    uow.commit_close_connection()

    return closed_loop_id


def _register_user_in_closed_loop(mocker, client, user_id, closed_loop_id, unique_identifier):
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    client.post(
        "http://127.0.0.1:5000/api/v1/register-closed-loop",
        json={"closed_loop_id": closed_loop_id, "unique_identifier": unique_identifier},
        headers=headers,
    )


def _verify_user_in_closed_loop(mocker, client, user_id, closed_loop_id, unique_identifier_otp):
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    client.post(
        "http://127.0.0.1:5000/api/v1/verify-closed-loop",
        json={
            "closed_loop_id": closed_loop_id,
            "unique_identifier_otp": unique_identifier_otp,
            "referral_unique_identifier": "",
        },
        headers=headers,
    )
    return


def _marketing_setup(seed_api_admin, client, mocker, weightage_type, weightage_value):
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    mocker.patch(
        "core.api.utils._get_uid_from_bearer",
        return_value=seed_api_admin(mocker, client),
    )
    client.post(
        "http://127.0.0.1:5000/api/v1/add-weightage",
        json={"weightage_type": weightage_type, "weightage_value": weightage_value},
        headers=headers,
    )
    # No need for this in execute p2p push
    # client.post(
    #     "http://127.0.0.1:5000/api/v1/set-cashback-slabs",
    #     json = {
    #         "cashback_slabs": [[0, 100, "PERCENTAGE", 0.1], [100, 200, "PERCENTAGE", 0.2]]
    #     }
    # )
    return


def _verify_phone_number(user_id, mocker, client):
    uow = UnitOfWork()
    user = uow.users.get(user_id)
    otp = user.otp
    uow.close_connection()

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)

    client.post(
        "http://127.0.0.1:5000/api/v1/verify-phone-number",
        json={"otp": otp},
        headers=headers,
    )
    return
