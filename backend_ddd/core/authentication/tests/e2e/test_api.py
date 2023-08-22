from json import loads
from uuid import uuid4

from core.api import utils


def test_base_url_api(client):
    response = client.get("http://127.0.0.1:5000/api/v1")

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="Welcome to the backend",
            status_code=200,
        ).__dict__
    )


def test_create_user_api(mocker, client):
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value="")
    mocker.patch("core.api.utils.firebaseUidToUUID", return_value=str(uuid4()))

    mocker.patch(
        "core.authentication.entrypoint.commands.firebase_create_user", return_value=""
    )
    mocker.patch("core.comms.entrypoint.commands.send_otp_sms", return_value=None)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    response = client.post(
        "http://127.0.0.1:5000/api/v1/create-user",
        json={
            "personal_email": "26100279@lums.edu.pk",
            "password": "cardpay123",
            "phone_number": "090078601",
            "user_type": "CUSTOMER",
            "full_name": "Shaheer Ahmad",
            "location": [24.8607, 67.0011],
        },
        headers=headers,
    )

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="User created successfully",
            status_code=201,
        ).__dict__
    )
