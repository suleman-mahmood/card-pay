import pytest
import os
from core.api.api import app as flask_app
from core.authentication.domain import model as auth_mdl
from uuid import uuid4

@pytest.fixture(scope="session", autouse=True)
def initialize_pytest_config():
    os.environ["DB_HOST"] = os.environ["DB_HOST_LOCAL"]
    os.environ["DB_NAME"] = os.environ["DB_NAME_LOCAL"]
    os.environ["DB_USER"] = os.environ["DB_USER_LOCAL"]
    os.environ["DB_PASSWORD"] = os.environ["DB_PASSWORD_LOCAL"]
    os.environ["DB_PORT"] = os.environ["DB_PORT_LOCAL"]


@pytest.fixture()
def app():
    app = flask_app
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

        mocker.patch(
            "core.authentication.entrypoint.commands.firebase_create_user", return_value=""
        )
        mocker.patch("core.comms.entrypoint.commands.send_otp_sms", return_value=None)

        client.post(
            "http://127.0.0.1:5000/api/v1/create-user",
            json={
                "personal_email": "26100279@lums.edu.pk",
                "password": "cardpay123",
                "phone_number": "090078601",
                "user_type": "CUSTOMER",
                "full_name": "Shaheer Ahmad",
                "location": [24.8607, 67.0011],
            }
        )

        return user_id
    return _seed_api_user

@pytest.fixture()
def seed_api_admin():
    def _seed_api_user(mocker, client):

        user_id = str(uuid4())
        mocker.patch("core.api.utils.firebaseUidToUUID", return_value=user_id)

        mocker.patch(
            "core.authentication.entrypoint.commands.firebase_create_user", return_value=""
        )
        mocker.patch("core.comms.entrypoint.commands.send_otp_sms", return_value=None)

        client.post(
            "http://127.0.0.1:5000/api/v1/create-user",
            json={
                "personal_email": "26100279@lums.edu.pk",
                "password": "cardpay123",
                "phone_number": "090078601",
                "user_type": "ADMIN",
                "full_name": "Shaheer Ahmad",
                "location": [24.8607, 67.0011],
            }
        )

        return user_id
    return _seed_api_user    
