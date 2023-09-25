import os
from json import loads
from random import randint
from uuid import uuid4

import pytest
from core.api import utils
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.conftest import (
    _create_closed_loop_helper,
    _register_user_in_closed_loop,
    _verify_phone_number,
    _verify_user_in_closed_loop,
)
from core.entrypoint.uow import UnitOfWork


def _get_random_unique_identifier() -> str:
    random_number = randint(20000000, 29999999)
    return str(random_number)


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
    user_id = str(uuid4())
    mocker.patch("core.api.utils.firebaseUidToUUID", return_value=user_id)

    response = client.post(
        "http://127.0.0.1:5000/api/v1/create-user",
        json={
            "personal_email": "26100279@lums.edu.pk",
            "password": "cardpay123",
            "phone_number": "3269507542",
            "user_type": "CUSTOMER",
            "full_name": "Shaheer Ahmad",
            "location": [24.8607, 67.0011],
        },
    )

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="User created successfully",
            status_code=201,
        ).__dict__
    )

    response = client.post(
        "http://127.0.0.1:5000/api/v1/create-user",
        json={
            "personal_email": "26100279@lums.edu.pk",
            "password": "cardpay123",
            "phone_number": "3269507542",
            "user_type": "CUSTOMER",
            "full_name": "Shaheer Ahmad",
            # "location": [24.8607, 67.0011],
        },
    )
    payload = loads(response.data.decode())
    assert payload["message"] == "invalid json payload, missing or extra parameters"
    assert payload["event_code"] == "DEFAULT_EVENT"

    response = client.post(
        "http://127.0.0.1:5000/api/v1/create-user",
        json={
            "personal_email": "26100279@lums.edu.pk",
            "password": "cardpay123",
            "phone_number": "3269507542",
            "user_type": "CUSTOMER",
            "full_name": "Shaheer Ahmad",
            "location": [24.8607, 67.0011],
            "extra": "extra",
        },
    )
    payload = loads(response.data.decode())
    assert payload["message"] == "invalid json payload, missing or extra parameters"
    assert payload["event_code"] == "DEFAULT_EVENT"

    mocker.patch(
        "core.authentication.entrypoint.firebase_service.create_user",
        side_effect=Exception("User already exists"),
    )

    response = client.post(
        "http://127.0.0.1:5000/api/v1/create-user",
        json={
            "personal_email": "26100279@lums.edu.pk",
            "password": "cardpay123",
            "phone_number": "3269507542",
            "user_type": "CUSTOMER",
            "full_name": "Shaheer Ahmad",
            "location": [24.8607, 67.0011],
        },
    )

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="User created successfully",
            status_code=201,
        ).__dict__
    )


def test_create_closed_loop_api(client):
    SECRET_KEY = os.environ["RETOOL_SECRET"]
    response = client.post(
        "http://127.0.0.1:5000/api/v1/create-closed-loop",
        json={
            "name": "LUMS",
            "logo_url": "sample/url",
            "description": "Harvard of Pakistan",
            "verification_type": "ROLLNUMBER",
            "regex": "[0-9]{8}",
            "RETOOL_SECRET": SECRET_KEY,
        },
    )

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="Closed loop created successfully",
            status_code=201,
        ).__dict__
    )


def test_get_all_closed_loops_api(seed_api_customer, mocker, client):
    user_id = seed_api_customer(mocker, client)
    closed_loop_id = _create_closed_loop_helper(client)
    closed_loop_id_2 = _create_closed_loop_helper(client)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)
    client.post(
        "http://127.0.0.1:5000/api/v1/register-closed-loop",
        json={
            "closed_loop_id": closed_loop_id,
            "unique_identifier": _get_random_unique_identifier(),
        },
        headers=headers,
    )
    client.post(
        "http://127.0.0.1:5000/api/v1/register-closed-loop",
        json={
            "closed_loop_id": closed_loop_id_2,
            "unique_identifier": _get_random_unique_identifier(),
        },
        headers=headers,
    )

    response = client.get("http://127.0.0.1:5000/api/v1/get-all-closed-loops", headers=headers)

    payload = loads(response.data.decode())
    assert payload["message"] == "User is not verified"
    assert response.status_code == 400

    _verify_phone_number(user_id, mocker, client)

    response = client.get("http://127.0.0.1:5000/api/v1/get-all-closed-loops", headers=headers)

    assert closed_loop_id_2 in [
        closed_loop["id"] for closed_loop in loads(response.data.decode())["data"]
    ]
    assert closed_loop_id in [
        closed_loop["id"] for closed_loop in loads(response.data.decode())["data"]
    ]


def test_register_closed_loop_api(seed_api_customer, mocker, client):
    # Create closed loop

    user_id = seed_api_customer(mocker, client)
    closed_loop_id = _create_closed_loop_helper(client)
    unique_identifier = _get_random_unique_identifier()

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)
    response = client.post(
        "http://127.0.0.1:5000/api/v1/register-closed-loop",
        json={
            "closed_loop_id": closed_loop_id,
            "unique_identifier": unique_identifier,
        },
        headers=headers,
    )

    payload = loads(response.data.decode())
    assert payload["message"] == "User is not verified"
    assert response.status_code == 400

    _verify_phone_number(user_id, mocker, client)

    response = client.post(
        "http://127.0.0.1:5000/api/v1/register-closed-loop",
        json={"closed_loop_id": closed_loop_id, "unique_identifier": unique_identifier},
        headers=headers,
    )

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="User registered into loop successfully",
            status_code=200,
        ).__dict__
    )


@pytest.mark.parametrize(
    "json_body",
    [
        ({}),
        (
            {
                "referral_unique_identifier": None,
            }
        ),
        (
            {
                "referral_unique_identifier": "",
            }
        ),
    ],
)
def test_verify_closed_loop_api(seed_api_customer, mocker, client, json_body):
    user_id = seed_api_customer(mocker, client)
    closed_loop_id = _create_closed_loop_helper(client)

    _verify_phone_number(user_id, mocker, client)
    _register_user_in_closed_loop(
        mocker, client, user_id, closed_loop_id, _get_random_unique_identifier()
    )

    uow = UnitOfWork()
    user = uow.users.get(user_id)
    uow.close_connection()

    otp = user.closed_loops[closed_loop_id].unique_identifier_otp

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    response = client.post(
        "http://127.0.0.1:5000/api/v1/verify-closed-loop",
        json={
            "closed_loop_id": closed_loop_id,
            "unique_identifier_otp": otp,
            **json_body,
        },
        headers=headers,
    )
    assert (
        loads(response.data.decode())
        == utils.Response(
            message="Closed loop verified successfully",
            status_code=200,
        ).__dict__
    )


def test_verify_closed_loop_with_referral_api(seed_api_customer, mocker, client):
    closed_loop_id = _create_closed_loop_helper(client)

    user_id = seed_api_customer(mocker, client)
    _verify_phone_number(user_id, mocker, client)
    _register_user_in_closed_loop(
        mocker, client, user_id, closed_loop_id, _get_random_unique_identifier()
    )

    referral_unique_identifier = _get_random_unique_identifier()
    referral_id = seed_api_customer(mocker, client)
    _verify_phone_number(referral_id, mocker, client)

    _register_user_in_closed_loop(
        mocker=mocker,
        client=client,
        user_id=referral_id,
        closed_loop_id=closed_loop_id,
        unique_identifier=referral_unique_identifier,
    )

    uow = UnitOfWork()
    referral_user = uow.users.get(user_id=referral_id)
    referral_otp = referral_user.closed_loops[closed_loop_id].unique_identifier_otp
    uow.close_connection()

    _verify_user_in_closed_loop(
        mocker=mocker,
        client=client,
        user_id=referral_id,
        closed_loop_id=closed_loop_id,
        unique_identifier_otp=referral_otp,
    )

    uow = UnitOfWork()
    user = uow.users.get(user_id=user_id)
    uow.close_connection()

    otp = user.closed_loops[closed_loop_id].unique_identifier_otp

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    response = client.post(
        "http://127.0.0.1:5000/api/v1/verify-closed-loop",
        json={
            "closed_loop_id": closed_loop_id,
            "unique_identifier_otp": otp,
            "referral_unique_identifier": referral_unique_identifier,
        },
        headers=headers,
    )
    assert (
        loads(response.data.decode())
        == utils.Response(
            message="Closed loop verified successfully",
            status_code=200,
        ).__dict__
    )


def test_verify_phone_number_api(seed_api_customer, mocker, client):
    user_id = seed_api_customer(mocker, client)

    uow = UnitOfWork()
    user = uow.users.get(user_id)
    otp = user.otp
    uow.close_connection()

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)

    response = client.post(
        "http://127.0.0.1:5000/api/v1/verify-phone-number",
        json={"otp": otp},
        headers=headers,
    )

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="Phone number verified successfully",
            status_code=200,
        ).__dict__
    )


def test_change_pin_api(seed_api_customer, mocker, client):
    user_id = seed_api_customer(mocker, client)
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    response = client.post(
        "http://127.0.0.1:5000/api/v1/change-pin",
        json={"new_pin": "1234"},
        headers=headers,
    )

    payload = loads(response.data.decode())
    assert payload["message"] == "User is not verified"
    assert response.status_code == 400

    _verify_phone_number(user_id, mocker, client)
    response = client.post(
        "http://127.0.0.1:5000/api/v1/change-pin",
        json={"new_pin": "1234"},
        headers=headers,
    )

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="Pin changed successfully",
            status_code=200,
        ).__dict__
    )


def test_get_user_api(seed_api_customer, mocker, client):
    user_id = seed_api_customer(mocker, client)
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    response = client.get("http://127.0.0.1:5000/api/v1/get-user", headers=headers)
    payload = loads(response.data.decode())
    assert payload["message"] == "User is not verified"
    assert response.status_code == 400

    _verify_phone_number(user_id, mocker, client)
    response = client.get("http://127.0.0.1:5000/api/v1/get-user", headers=headers)

    x = loads(response.data.decode())
    assert x["message"] == "User returned successfully"
    assert x["status_code"] == 200
    assert x["data"]["id"] == user_id


def test_get_user_balance_api(seed_api_customer, mocker, client):
    user_id = seed_api_customer(mocker, client)

    uow = UnitOfWork()
    balance = auth_qry.get_user_balance(
        user_id=user_id,
        uow=uow,
    )
    uow.close_connection()

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    response = client.get("http://127.0.0.1:5000/api/v1/get-user-balance", headers=headers)

    payload = loads(response.data.decode())

    assert response.status_code == 400
    assert payload["message"] == "User is not verified"

    _verify_phone_number(user_id, mocker, client)
    response = client.get("http://127.0.0.1:5000/api/v1/get-user-balance", headers=headers)

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="User balance returned successfully",
            status_code=200,
            data={
                "balance": balance,
            },
        ).__dict__
    )


def test_authenticate_token(seed_api_customer, mocker, client):
    user_id = seed_api_customer(mocker, client)
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)

    headers = {
        "Authorization": "pytest_auth_token",
        "Content-Type": "application/json",
    }
    response = client.get("http://127.0.0.1:5000/api/v1/get-user", headers=headers)
    payload = loads(response.data.decode())
    assert payload["message"] == "Unauthorized, invalid header"
    assert response.status_code == 401

    headers = {
        "Authorization": "",
        "Content-Type": "application/json",
    }
    response = client.get("http://127.0.0.1:5000/api/v1/get-user", headers=headers)
    payload = loads(response.data.decode())
    assert payload["message"] == "Unauthorized, invalid header"
    assert response.status_code == 401

    headers = {
        "Authorization": "Bearer ",
        "Content-Type": "application/json",
    }
    response = client.get("http://127.0.0.1:5000/api/v1/get-user", headers=headers)
    payload = loads(response.data.decode())
    assert payload["message"] == "Unauthorized, invalid header"
    assert response.status_code == 401

    headers = {
        "Authorization": "Bearer",
        "Content-Type": "application/json",
    }
    response = client.get("http://127.0.0.1:5000/api/v1/get-user", headers=headers)
    payload = loads(response.data.decode())
    assert payload["message"] == "Unauthorized, invalid header"
    assert response.status_code == 401

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    _verify_phone_number(user_id, mocker, client)
    response = client.get("http://127.0.0.1:5000/api/v1/get-user", headers=headers)

    x = loads(response.data.decode())
    assert x["message"] == "User returned successfully"
    assert x["status_code"] == 200
    assert x["data"]["id"] == user_id


# TODO: need to write the test for create vendor
# def test_auth_retools_create_vendor(mocker, client):

#     uow = UnitOfWork()
#     auth_cmd.create_closed_loop(
#         name="retool e2e testing",
#         logo_url="xyz.com",
#         description="create vendor e2e testing",
#         verification_type="ROLLNUMBER",
#         regex="[0-9]{8}",
#         uow = uow,
#     )
#     closed_loop_id = auth_qry._get_latest_closed_loop_id(
#         uow
#     )

#     user_id = str(uuid4())
#     SECRET_KEY = os.environ["RETOOL_SECRET"]

#     mocker.patch("core.api.utils.firebaseUidToUUID", return_value=user_id)
#     mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user_id)

#     #passing incorrect secret key
#     response = client.post(
#         "http://127.0.0.1:5000/api/v1/auth-retools-create-vendor",
#         json={
#             "personal_email": "zak@zak.com",
#             "password": "cardpay123",
#             "phone_number": "3763936384",
#             "full_name": "Zain vendor retool",
#             "longitude": 24.8607,
#             "latitude": 67.0011,
#             "closed_loop_id": closed_loop_id,
#             "RETOOL_SECRET": "",
#         }
#     )

#     print(loads(response.data.decode()))
#     print(response.status_code)

# response = client.post(
#     "http://127.0.0.1:5000/api/v1/auth-retools-create-vendor",
#     json={
#         "personal_email": "zak@zak.com",
#         "password": "cardpay123",
#         "phone_number": "3763936384",
#         "full_name": "Zain vendor retool",
#         "longitude": 24.8607,
#         "latitude": 67.0011,
#         "closed_loop_id": closed_loop_id,
#         "RETOOL_SECRET": SECRET_KEY,
#     }
# )

# assert loads(response.data.decode()) == utils.Response(
#     message="Vendor created successfully",
#     status_code=201,
# ).__dict__
