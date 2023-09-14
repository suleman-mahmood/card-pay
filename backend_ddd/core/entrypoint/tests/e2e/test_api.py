"""api tests for general purpose queries and tasks"""

import pytest
import os

from json import loads
from uuid import uuid4

from core.entrypoint.uow import UnitOfWork


def test_get_latest_force_update_version(client):
    """test get_latest_force_update_version /get-latest-force-update-version"""

    sql = """
    insert into
        version_history (id, latest_version, force_update_version)
    values
        (%s, %s, %s)
    """
    uow = UnitOfWork()
    uow.cursor.execute(sql, (str(uuid4()), "1.0.0", "1.0.0"))
    uow.commit_close_connection()

    response = client.get(
        "http://127.0.0.1:5000/api/v1/get-latest-force-update-version"
    )
    data = loads(response.data.decode())
    message = data["message"]
    status_code = data["status_code"]

    assert message == "App latest and force update version returned successfully"
    assert status_code == 200


random_uid = str(uuid4())


@pytest.mark.parametrize(
    "json_body, response_body",
    [
        (
            {},
            [
                {
                    "StatusCode": "01",
                    "InvoiceID": None,
                    "Description": "Invalid Data. Username or password is invalid",
                }
            ],
        ),
        (
            {
                "username": "",
            },
            [
                {
                    "StatusCode": "01",
                    "InvoiceID": None,
                    "Description": "Invalid Data. Username or password is invalid",
                }
            ],
        ),
        (
            {
                "password": "",
            },
            [
                {
                    "StatusCode": "01",
                    "InvoiceID": None,
                    "Description": "Invalid Data. Username or password is invalid",
                }
            ],
        ),
        (
            {
                "Password": "",
                "Username": "",
            },
            [
                {
                    "StatusCode": "01",
                    "InvoiceID": None,
                    "Description": "Invalid Data. Username or password is invalid",
                }
            ],
        ),
        (
            {
                "username": "",
                "password": "",
            },
            [
                {
                    "StatusCode": "01",
                    "InvoiceID": None,
                    "Description": "Invalid Data. Username or password is invalid",
                }
            ],
        ),
        (
            {
                "username": "",
                "password": "",
                "csvinvoiceids": "",
            },
            [
                {
                    "StatusCode": "02",
                    "InvoiceID": None,
                    "Description": "Service Failure",
                }
            ],
        ),
        (
            {
                "username": os.environ.get("PAYPRO_USERNAME"),
                "password": os.environ.get("PAYPRO_PASSWORD"),
                "csvinvoiceids": "",
            },
            [],
        ),
        (
            {
                "username": os.environ.get("PAYPRO_USERNAME"),
                "password": os.environ.get("PAYPRO_PASSWORD"),
                "csvinvoiceids": random_uid,
            },
            [
                {
                    "StatusCode": "03",
                    "InvoiceID": random_uid,
                    "Description": "No records found.",
                }
            ],
        ),
        (
            {
                "username": os.environ.get("PAYPRO_USERNAME"),
                "password": os.environ.get("PAYPRO_PASSWORD"),
                "csvinvoiceids": f"{random_uid}, {random_uid}",
            },
            [
                {
                    "StatusCode": "03",
                    "InvoiceID": random_uid,
                    "Description": "No records found.",
                },
                {
                    "StatusCode": "03",
                    "InvoiceID": random_uid,
                    "Description": "No records found.",
                },
            ],
        ),
    ],
)
def test_pay_pro_callback(client, json_body, response_body):
    headers = {"Content-Type": "application/json"}
    response = client.post(
        "http://127.0.0.1:5000/api/v1/pay-pro-callback", json=json_body, headers=headers
    )
    data = loads(response.data.decode())

    assert data == response_body
