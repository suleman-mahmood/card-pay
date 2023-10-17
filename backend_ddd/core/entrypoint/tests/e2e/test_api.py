"""api tests for general purpose queries and tasks"""

import os
from json import loads
from uuid import uuid4

import pytest
from core.api import utils
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.tests.e2e import test_api as auth_test_api
from core.conftest import (
    _create_closed_loop_helper,
    _register_user_in_closed_loop,
    _verify_phone_number,
    _verify_user_in_closed_loop,
)
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

    response = client.get("http://127.0.0.1:5000/api/v1/get-latest-force-update-version")
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


# def test_pay_pro_callback_successful_deposit(
#     client, mocker, seed_api_cardpay, seed_api_customer, add_1000_wallet
# ):
#     cardpay_id = seed_api_cardpay(mocker, client)
#     sender_id = seed_api_customer(mocker, client)
#     recipient_id = seed_api_customer(mocker, client)
#     closed_loop_id = _create_closed_loop_helper(client)
#     headers = {
#         "Authorization": "Bearer pytest_auth_token",
#         "Content-Type": "application/json",
#     }

#     client.post(
#         "http://127.0.0.1:5000/api/v1/add-and-set-missing-marketing-weightages-to-zero",
#         json={
#             "RETOOL_SECRET": "",
#         },
#         headers=headers,
#     )

#     _verify_phone_number(sender_id, mocker, client)
#     _verify_phone_number(recipient_id, mocker, client)

#     _register_user_in_closed_loop(
#         mocker,
#         client,
#         sender_id,
#         closed_loop_id,
#         auth_test_api._get_random_unique_identifier(),
#     )
#     _register_user_in_closed_loop(
#         mocker,
#         client,
#         recipient_id,
#         closed_loop_id,
#         auth_test_api._get_random_unique_identifier(),
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
#     sender_unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
#         user_id=sender_id, closed_loop_id=closed_loop_id, uow=uow
#     )
#     recipient_unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
#         user_id=recipient_id, closed_loop_id=closed_loop_id, uow=uow
#     )
#     add_1000_wallet(uow=uow, wallet_id=sender_id)
#     tx_id = str(uuid4())

#     sql = """
#         insert into transactions (
#             id,
#             amount,
#             mode,
#             transaction_type,
#             status,
#             sender_wallet_id,
#             recipient_wallet_id
#         )
#         values (
#             %(tx_id)s, 
#             %(amount)s, 
#             'APP_TRANSFER', 
#             'PAYMENT_GATEWAY', 
#             'PENDING', 
#             %(sender_wallet_id)s, 
#             %(recipient_wallet_id)s
#         )
#         ;
#     """
#     uow.dict_cursor.execute(
#         sql,
#         {
#             "amount": 500,
#             "sender_wallet_id": sender_id,
#             "recipient_wallet_id": recipient_id,
#             "tx_id": tx_id,
#         },
#     )

#     uow.commit_close_connection()

#     json_body = {
#         "username": os.environ.get("PAYPRO_USERNAME"),
#         "password": os.environ.get("PAYPRO_PASSWORD"),
#         "csvinvoiceids": tx_id,
#     }
#     headers = {"Content-Type": "application/json"}
#     response = client.post(
#         "http://127.0.0.1:5000/api/v1/pay-pro-callback", json=json_body, headers=headers
#     )
#     data = loads(response.data.decode())

#     assert data == [
#         {
#             "StatusCode": "00",
#             "InvoiceID": tx_id,
#             "Description": "Invoice successfully marked as paid",
#         }
#     ]

#     response = client.post(
#         "http://127.0.0.1:5000/api/v1/pay-pro-callback", json=json_body, headers=headers
#     )
#     data = loads(response.data.decode())

#     assert data == []
