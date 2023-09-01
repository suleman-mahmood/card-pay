import threading
import pytest
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.api.event_codes import EventCode
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


def test_execute_p2p_push_one_to_many(
    seed_api_admin, seed_api_customer, mocker, client
):
    NUMBER_OF_RECIPIENTS = 3

    sender_id = seed_api_customer(mocker, client)
    recipient_ids = [
        seed_api_customer(mocker, client) for _ in range(NUMBER_OF_RECIPIENTS)
    ]
    closed_loop_id = _create_closed_loop_helper(client)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    _verify_phone_number(sender_id, mocker, client)
    for recipient_id in recipient_ids:
        _verify_phone_number(recipient_id, mocker, client)

    _register_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, "26100274")
    for recipient_id, _ in zip(recipient_ids, range(NUMBER_OF_RECIPIENTS)):
        _register_user_in_closed_loop(
            mocker, client, recipient_id, closed_loop_id, f"2410016{_}"
        )

    uow = UnitOfWork()
    sender = uow.users.get(user_id=sender_id)
    recipients = [uow.users.get(user_id=recipient_id) for recipient_id in recipient_ids]
    uow.close_connection()

    otp = sender.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, otp)

    otps = [
        recipient.closed_loops[closed_loop_id].unique_identifier_otp
        for recipient in recipients
    ]
    for recipient_id, otp in zip(recipient_ids, otps):
        _verify_user_in_closed_loop(mocker, client, recipient_id, closed_loop_id, otp)

    uow = UnitOfWork()
    sender_unique_identifier = auth_qry.get_unique_identifier_from_user_id(
        user_id=sender_id, uow=uow
    )
    recipient_unique_identifiers = [
        auth_qry.get_unique_identifier_from_user_id(user_id=recipient_id, uow=uow)
        for recipient_id in recipient_ids
    ]
    uow.transactions.add_1000_wallet(wallet_id=sender_id)
    uow.commit_close_connection()

    _marketing_setup(seed_api_admin, client, mocker, "P2P_PUSH", "10")

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)

    processes = []

    for recipient_unique_identifier in recipient_unique_identifiers:
        process = threading.Thread(
            target=client.post,
            args=(
                "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
                {
                    "recipient_unique_identifier": recipient_unique_identifiers,
                    "amount": 100,
                    "closed_loop_id": closed_loop_id,
                },
                headers,
            ),
        )

        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # print(processes[0])


def test_execute_p2p_push_api(seed_api_admin, seed_api_customer, mocker, client):
    sender_id = seed_api_customer(mocker, client)
    recipient_id = seed_api_customer(mocker, client)
    closed_loop_id = _create_closed_loop_helper(client)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    _verify_phone_number(recipient_id, mocker, client)
    _verify_phone_number(sender_id, mocker, client)

    _register_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, "26100274")
    _register_user_in_closed_loop(
        mocker, client, recipient_id, closed_loop_id, "26100290"
    )

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

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
    response = client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 100,
            "closed_loop_id": closed_loop_id,
        },
        headers=headers,
    )

    payload = loads(response.data.decode())

    assert (
        payload
        == utils.Response(
            message="p2p push transaction executed successfully",
            status_code=201,
        ).__dict__
    )

    response = client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 0,
            "closed_loop_id": closed_loop_id,
        },
        headers=headers,
    )

    payload = loads(response.data.decode())

    assert payload["message"] == "Amount is zero or negative"
    assert EventCode[payload["event_code"]] == EventCode.DEFAULT_EVENT
    assert response.status_code == 400

    response = client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": sender_unique_identifier,
            "amount": 100,
            "closed_loop_id": closed_loop_id,
        },
        headers=headers,
    )
    payload = loads(response.data.decode())

    assert (
        payload["message"]
        == "Constraint violated, sender and recipient wallets are the same"
    )
    assert EventCode[payload["event_code"]] == EventCode.DEFAULT_EVENT
    assert response.status_code == 400


def test_get_user_recent_transcations_api(
    seed_api_customer, seed_api_admin, mocker, client
):
    sender_id = seed_api_customer(mocker, client)
    recipient_id = seed_api_customer(mocker, client)

    closed_loop_id = _create_closed_loop_helper(client)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    _verify_phone_number(recipient_id, mocker, client)
    _verify_phone_number(sender_id, mocker, client)

    _register_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, "26100279")
    _register_user_in_closed_loop(
        mocker, client, recipient_id, closed_loop_id, "26100290"
    )

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

    # execute
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
    client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 100,
            "closed_loop_id": closed_loop_id,
        },
        headers=headers,
    )

    # now send 100 back to sender

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=recipient_id)
    client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": sender_unique_identifier,
            "amount": 100,
            "closed_loop_id": closed_loop_id,
        },
        headers=headers,
    )

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
    response = client.get(
        "http://127.0.0.1:5000/api/v1/get-user-recent-transactions", headers=headers
    )

    uow = UnitOfWork()
    txs = pmt_qry.get_all_transactions_of_a_user(
        user_id=sender_id,
        offset=0,
        page_size=50,
        uow=uow,
    )
    uow.close_connection()
    res = loads(response.data.decode())

    assert res["message"] == "User recent transactions returned successfully"
    assert res["status_code"] == 200
