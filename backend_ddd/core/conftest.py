import os
from uuid import uuid4

import pytest
import sentry_sdk
from core.api.api import app as flask_app
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.entrypoint.uow import UnitOfWork


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
    mocker.patch("core.authentication.entrypoint.firebase_service.get_user", return_value="")


@pytest.fixture()
def app():
    app = flask_app
    sentry_sdk.init(None)  # Disable the initialized sentry
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


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
                "phone_number": "3269507526",
                "user_type": "CUSTOMER",
                "full_name": "Shaheer Ahmad",
                "location": [24.8607, 67.0011],
            },
        )

        return user_id

    return _seed_api_user


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
