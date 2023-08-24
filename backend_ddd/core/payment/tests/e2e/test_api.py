import pytest
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.payment.entrypoint import queries as pmt_qry
from core.entrypoint.uow import UnitOfWork
from core.conftest import (
    _create_closed_loop_helper,
    _register_user_in_closed_loop,
    _verify_user_in_closed_loop,
    _marketing_setup,
    _verify_phone_number,
)
from json import loads
from core.api import utils

import os


def test_execute_p2p_push_api(seed_api_admin, seed_api_customer, mocker, client):
    
    sender_id = seed_api_customer(mocker, client)
    recipient_id = seed_api_customer(mocker, client)
    closed_loop_id = _create_closed_loop_helper(client)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    _register_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, "26100279")
    _register_user_in_closed_loop(mocker, client, recipient_id, closed_loop_id, "26100290")
   
    uow = UnitOfWork()
    sender = uow.users.get(user_id=sender_id)
    recipient = uow.users.get(user_id=recipient_id)
    uow.close_connection()

    otp = sender.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, otp)
    
    otp = recipient.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(mocker, client, recipient_id, closed_loop_id, otp)
    
    uow = UnitOfWork()
    recipient_unique_identifier = auth_qry.get_unique_identifier_from_user_id(
        user_id=recipient_id, uow=uow
    )
    sender_unique_identifier = auth_qry.get_unique_identifier_from_user_id(
        user_id=sender_id, uow=uow
    )
    uow.transactions.add_1000_wallet(wallet_id=sender_id)
    uow.commit_close_connection()

    _marketing_setup(seed_api_admin, client, mocker, "P2P_PUSH", "10")
    
    #execute
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
    respnonse = client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 100,
            "closed_loop_id": closed_loop_id
        },
        headers=headers
    )

    assert loads(respnonse.data.decode()) == utils.Response(
            message="User is not verified",
            status_code=400,
        ).__dict__

    _verify_phone_number(recipient_id, mocker, client)
    _verify_phone_number(sender_id, mocker, client)

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
    respnonse = client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 100,
            "closed_loop_id": closed_loop_id
        },
        headers=headers
    )

    assert loads(respnonse.data.decode()) == utils.Response(
            message="p2p push transaction executed successfully",
            status_code=201,
        ).__dict__

    respnonse = client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 0,
            "closed_loop_id": closed_loop_id
        },
        headers=headers
    )

    assert loads(respnonse.data.decode()) == utils.Response(
            message="Amount is zero or negative",
            status_code=400,
        ).__dict__

    respnonse = client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": sender_unique_identifier,
            "amount": 100,
            "closed_loop_id": closed_loop_id
        },
        headers=headers
    )

    assert loads(respnonse.data.decode()) == utils.Response(
            message="Constraint violated, sender and recipient wallets are the same",
            status_code=400,
        ).__dict__