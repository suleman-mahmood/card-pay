import concurrent.futures
import threading
import time
from json import loads

import pytest
from core.api import utils
from core.api.event_codes import EventCode
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.tests.e2e import test_api as auth_test_api
from core.conftest import (
    _create_closed_loop_helper,
    _marketing_setup,
    _register_user_in_closed_loop,
    _verify_phone_number,
    _verify_user_in_closed_loop,
)
from core.entrypoint.uow import UnitOfWork
from core.payment.entrypoint import queries as pmt_qry
from core.payment.entrypoint.queries import get_wallet_balance
from core.api import utils
from core.authentication.tests.e2e import test_api as auth_test_api
from uuid import uuid4


def _post_p2p_push_transaction(client, url, json_data, headers):
    """
    A python function to make a POST request to the execute-p2p-push-transaction endpoint.
    Threads do badtameezi when you try client.post directly in the thread.
    """

    response = client.post(url, json=json_data, headers=headers)
    return response


def test_execute_p2p_push_one_to_many_valid(
    seed_api_admin, seed_api_cardpay, seed_api_customer, add_1000_wallet, mocker, client
):
    """
    Testing NUMBER_OF_RECIPIENTS transactions in parallel. Setup invloves one sender and NUMBER_OF_RECIPIENTS recipients.
    All transactions are valid and should be executed successfully. In the end the sender wallet balance should be 0.
    """
    cardpay_id = seed_api_cardpay(mocker, client)

    NUMBER_OF_RECIPIENTS = 10

    sender_id = seed_api_customer(mocker, client)
    recipient_ids = [seed_api_customer(mocker, client) for _ in range(NUMBER_OF_RECIPIENTS)]
    closed_loop_id = _create_closed_loop_helper(client)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    client.post(
        "http://127.0.0.1:5000/api/v1/add-and-set-missing-marketing-weightages-to-zero",
        json={
            "RETOOL_SECRET": "",
        },
        headers=headers,
    )

    _verify_phone_number(sender_id, mocker, client)
    for recipient_id in recipient_ids:
        _verify_phone_number(recipient_id, mocker, client)

    _register_user_in_closed_loop(
        mocker,
        client,
        sender_id,
        closed_loop_id,
        auth_test_api._get_random_unique_identifier(),
    )
    for recipient_id, _ in zip(recipient_ids, range(NUMBER_OF_RECIPIENTS)):
        _register_user_in_closed_loop(
            mocker,
            client,
            recipient_id,
            closed_loop_id,
            auth_test_api._get_random_unique_identifier(),
        )

    uow = UnitOfWork()
    sender = uow.users.get(user_id=sender_id)
    recipients = [uow.users.get(user_id=recipient_id) for recipient_id in recipient_ids]
    uow.close_connection()

    otp = sender.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, otp)

    otps = [
        recipient.closed_loops[closed_loop_id].unique_identifier_otp for recipient in recipients
    ]
    for recipient_id, otp in zip(recipient_ids, otps):
        _verify_user_in_closed_loop(mocker, client, recipient_id, closed_loop_id, otp)

    uow = UnitOfWork()
    sender_unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
        user_id=sender_id, closed_loop_id=closed_loop_id, uow=uow
    )
    recipient_unique_identifiers = [
        auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
            user_id=recipient_id, closed_loop_id=closed_loop_id, uow=uow
        )
        for recipient_id in recipient_ids
    ]
    add_1000_wallet(uow=uow, wallet_id=sender_id)
    uow.commit_close_connection()

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)

    post_requests = [
        {
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 10,
            "closed_loop_id": closed_loop_id,
        }
        for recipient_unique_identifier in recipient_unique_identifiers
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(post_requests)) as executor:
        # Create a list to store the futures
        futures = []
        for request_data in post_requests:
            future = executor.submit(
                _post_p2p_push_transaction,
                client,
                "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
                request_data,
                headers,
            )
            futures.append(future)
        # Wait for all futures to complete
        concurrent.futures.wait(futures)
        # Extract and check the results of each POST request
        for future, request_data in zip(futures, post_requests):
            response = future.result()
            payload = loads(response.data.decode())

            assert (
                payload
                == utils.Response(
                    message="p2p push transaction executed successfully",
                    status_code=201,
                ).__dict__
            )

    post_requests = [
        {
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 90,
            "closed_loop_id": closed_loop_id,
        }
        for recipient_unique_identifier in recipient_unique_identifiers
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(post_requests)) as executor:
        # Create a list to store the futures
        futures = []

        for request_data in post_requests:
            future = executor.submit(
                _post_p2p_push_transaction,
                client,
                "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
                request_data,
                headers,
            )
            futures.append(future)

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

        # Extract and check the results of each POST request
        for future, request_data in zip(futures, post_requests):
            response = future.result()
            payload = loads(response.data.decode())

            assert payload["message"] == "p2p push transaction executed successfully"
            assert response.status_code == 200

    uow = UnitOfWork()
    sender_balance = get_wallet_balance(wallet_id=sender_id, uow=uow)
    assert sender_balance == 0


def test_execute_p2p_push_one_to_many_all_invalid(
    seed_api_admin, seed_api_cardpay, seed_api_customer, add_1000_wallet, mocker, client
):
    """
    Testing NUMBER_OF_RECIPIENTS transactions in parallel. Setup invloves one sender and NUMBER_OF_RECIPIENTS recipients.
    All transactions are invalid and should be respond with an 'insufficient balance in sender' exception.
    In the end the sender wallet balance should be exactly the same as in the beginning.
    """
    cardpay_id = seed_api_cardpay(mocker, client)

    NUMBER_OF_RECIPIENTS = 10

    sender_id = seed_api_customer(mocker, client)
    recipient_ids = [seed_api_customer(mocker, client) for _ in range(NUMBER_OF_RECIPIENTS)]
    closed_loop_id = _create_closed_loop_helper(client)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    client.post(
        "http://127.0.0.1:5000/api/v1/add-and-set-missing-marketing-weightages-to-zero",
        json={
            "RETOOL_SECRET": "",
        },
        headers=headers,
    )

    _verify_phone_number(sender_id, mocker, client)
    for recipient_id in recipient_ids:
        _verify_phone_number(recipient_id, mocker, client)

    _register_user_in_closed_loop(
        mocker,
        client,
        sender_id,
        closed_loop_id,
        auth_test_api._get_random_unique_identifier(),
    )
    for recipient_id, _ in zip(recipient_ids, range(NUMBER_OF_RECIPIENTS)):
        _register_user_in_closed_loop(
            mocker,
            client,
            recipient_id,
            closed_loop_id,
            auth_test_api._get_random_unique_identifier(),
        )

    uow = UnitOfWork()
    sender = uow.users.get(user_id=sender_id)
    recipients = [uow.users.get(user_id=recipient_id) for recipient_id in recipient_ids]
    uow.close_connection()

    otp = sender.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, otp)

    otps = [
        recipient.closed_loops[closed_loop_id].unique_identifier_otp for recipient in recipients
    ]
    for recipient_id, otp in zip(recipient_ids, otps):
        _verify_user_in_closed_loop(mocker, client, recipient_id, closed_loop_id, otp)

    uow = UnitOfWork()
    sender_unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
        user_id=sender_id, closed_loop_id=closed_loop_id, uow=uow
    )
    recipient_unique_identifiers = [
        auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
            user_id=recipient_id, closed_loop_id=closed_loop_id, uow=uow
        )
        for recipient_id in recipient_ids
    ]
    add_1000_wallet(uow=uow, wallet_id=sender_id)
    uow.commit_close_connection()

    post_requests = [
        {
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 2000,
            "closed_loop_id": closed_loop_id,
        }
        for recipient_unique_identifier in recipient_unique_identifiers
    ]
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(post_requests)) as executor:
        # Create a list to store the futures
        futures = []

        for request_data in post_requests:
            future = executor.submit(
                _post_p2p_push_transaction,
                client,
                "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
                request_data,
                headers,
            )
            futures.append(future)

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

        # Extract and check the results of each POST request
        for future, request_data in zip(futures, post_requests):
            response = future.result()
            payload = loads(response.data.decode())

            assert payload["message"] == "Insufficient balance in sender's wallet"
            assert EventCode[payload["event_code"]] == EventCode.DEFAULT_EVENT
            assert response.status_code == 400

    uow = UnitOfWork()
    sender_balance = get_wallet_balance(wallet_id=sender_id, uow=uow)
    assert sender_balance == 1000


def test_execute_p2p_push_one_to_many_half_valid_invalid(
    seed_api_admin, seed_api_cardpay, seed_api_customer, add_1000_wallet, mocker, client
):
    """
    Testing NUMBER_OF_RECIPIENTS transactions in parallel. Setup invloves one sender and NUMBER_OF_RECIPIENTS recipients.
    Half transactions are invalid and half are valid and should be respond with an 'insufficient balance in sender' exception
    for half and 'executed successfully' for half. In the end the sender wallet balance should be exactly the same as in the beginning.
    """
    cardpay_id = seed_api_cardpay(mocker, client)

    NUMBER_OF_RECIPIENTS = 10

    sender_id = seed_api_customer(mocker, client)
    recipient_ids = [seed_api_customer(mocker, client) for _ in range(NUMBER_OF_RECIPIENTS)]
    closed_loop_id = _create_closed_loop_helper(client)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    client.post(
        "http://127.0.0.1:5000/api/v1/add-and-set-missing-marketing-weightages-to-zero",
        json={
            "RETOOL_SECRET": "",
        },
        headers=headers,
    )

    _verify_phone_number(sender_id, mocker, client)
    for recipient_id in recipient_ids:
        _verify_phone_number(recipient_id, mocker, client)

    _register_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, "26100274")
    for recipient_id, _ in zip(recipient_ids, range(NUMBER_OF_RECIPIENTS)):
        _register_user_in_closed_loop(
            mocker,
            client,
            recipient_id,
            closed_loop_id,
            auth_test_api._get_random_unique_identifier(),
        )

    uow = UnitOfWork()
    sender = uow.users.get(user_id=sender_id)
    recipients = [uow.users.get(user_id=recipient_id) for recipient_id in recipient_ids]
    uow.close_connection()

    otp = sender.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, otp)

    otps = [
        recipient.closed_loops[closed_loop_id].unique_identifier_otp for recipient in recipients
    ]
    for recipient_id, otp in zip(recipient_ids, otps):
        _verify_user_in_closed_loop(mocker, client, recipient_id, closed_loop_id, otp)

    uow = UnitOfWork()
    sender_unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
        user_id=sender_id, closed_loop_id=closed_loop_id, uow=uow
    )
    recipient_unique_identifiers = [
        auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
            user_id=recipient_id, closed_loop_id=closed_loop_id, uow=uow
        )
        for recipient_id in recipient_ids
    ]
    add_1000_wallet(uow=uow, wallet_id=sender_id)
    uow.commit_close_connection()

    post_requests = [
        {
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 200,
            "closed_loop_id": closed_loop_id,
        }
        for recipient_unique_identifier in recipient_unique_identifiers
    ]
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(post_requests)) as executor:
        # Create a list to store the futures
        futures = []

        for request_data in post_requests:
            future = executor.submit(
                _post_p2p_push_transaction,
                client,
                "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
                request_data,
                headers,
            )
            futures.append(future)

        concurrent.futures.wait(futures)

        valid_txns = 0
        invalid_txns = 0

        for future, request_data in zip(futures, post_requests):
            response = future.result()
            payload = loads(response.data.decode())

            if response.status_code == 200:
                valid_txns += 1
            else:
                invalid_txns += 1

        assert valid_txns == 5
        assert invalid_txns == 5


def test_execute_p2p_push_api(
    seed_api_admin, seed_api_customer, seed_api_cardpay, add_1000_wallet, mocker, client
):
    sender_id = seed_api_customer(mocker, client)
    recipient_id = seed_api_customer(mocker, client)
    cardpay_id = seed_api_cardpay(mocker, client)

    closed_loop_id = _create_closed_loop_helper(client)
    sender_unique_identifier = "26100274"
    recipient_unique_identifier = "26100290"

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    client.post(
        "http://127.0.0.1:5000/api/v1/add-and-set-missing-marketing-weightages-to-zero",
        json={
            "RETOOL_SECRET": "",
        },
        headers=headers,
    )

    _verify_phone_number(recipient_id, mocker, client)
    _verify_phone_number(sender_id, mocker, client)

    _register_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, "26100274")
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
    recipient_unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
        user_id=recipient_id, closed_loop_id=closed_loop_id, uow=uow
    )
    sender_unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
        user_id=sender_id, closed_loop_id=closed_loop_id, uow=uow
    )

    add_1000_wallet(uow=uow, wallet_id=sender_id)
    uow.commit_close_connection()

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

    assert payload["message"] == "Constraint violated, sender and recipient wallets are the same"
    assert EventCode[payload["event_code"]] == EventCode.DEFAULT_EVENT
    assert response.status_code == 400

def _seed_customer_vendor_waiter(
    seed_api_customer, mocker, client, seed_api_vendor, uow
):
    closed_loop_id = _create_closed_loop_helper(client)
    customer_id = seed_api_customer(mocker, client)
    vendor_id = seed_api_vendor(mocker, client, closed_loop_id)
    waiter_id = seed_api_vendor(mocker, client, closed_loop_id)

    _verify_phone_number(customer_id, mocker, client)
    _register_user_in_closed_loop(
        mocker, client, customer_id, closed_loop_id, "26100279"
    )
    customer = uow.users.get(user_id=customer_id)

    customer_otp = customer.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(
        mocker, client, customer.id, closed_loop_id, customer_otp
    )

    return customer_id, vendor_id, waiter_id, closed_loop_id


def test_execute_qr_transaction_v2_api_incorrect_QR_version(
    seed_api_customer, mocker, client, seed_api_vendor, get_qr_id_from_user_id
):
    uow = UnitOfWork()
    customer_id, vendor_id, waiter_id, closed_loop_id = _seed_customer_vendor_waiter(
        seed_api_customer, mocker, client, seed_api_vendor, uow
    )

    vendor_qr_id = get_qr_id_from_user_id(vendor_id, uow)
    waiter_qr_id = get_qr_id_from_user_id(waiter_id, uow)

    uow.commit_close_connection()

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=customer_id)
    
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    
    response = client.post(
      "http://127.0.0.1:5000/api/v1/execute-qr-transaction-v2",
      json={
            "vendor_qr_id": vendor_qr_id,
            "waiter_qr_id": waiter_qr_id,
            "bill_amount": 100,
            "tip_amount": 10,
            "v": 3,
          },
          headers=headers,
      )
    
    payload = loads(response.data.decode())
    assert payload["message"] == "Invalid QR version"
    assert response.status_code == 400


def test_execute_qr_transaction_v2_api_incorrect_vendor_qr_id(
    seed_api_customer, mocker, client, seed_api_vendor
):
    uow = UnitOfWork()
    customer_id, vendor_id, waiter_id, closed_loop_id = _seed_customer_vendor_waiter(
        seed_api_customer, mocker, client, seed_api_vendor, uow
    )

    uow.commit_close_connection()

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=customer_id)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    response = client.post(
        "http://127.0.0.1:5000/api/v1/execute-qr-transaction-v2",
        json={
            "vendor_qr_id": str(uuid4()),
            "waiter_qr_id": str(uuid4()),
            "bill_amount": 100,
            "tip_amount": 10,
            "v": 2,
        },
        headers=headers,
    )

    payload = loads(response.data.decode())
    assert payload["message"] == "Invalid QR code"
    assert response.status_code == 400


def test_execute_qr_transaction_v2_api_low_balance_for_bill(
    seed_api_customer,
    mocker,
    client,
    seed_api_vendor,
    add_1000_wallet,
    get_qr_id_from_user_id,
):
    uow = UnitOfWork()
    customer_id, vendor_id, waiter_id, closed_loop_id = _seed_customer_vendor_waiter(
        seed_api_customer, mocker, client, seed_api_vendor, uow
    )

    vendor_qr_id = get_qr_id_from_user_id(vendor_id, uow)
    waiter_qr_id = get_qr_id_from_user_id(waiter_id, uow)

    add_1000_wallet(uow=uow, wallet_id=customer_id)

    uow.commit_close_connection()

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=customer_id)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    response = client.post(
        "http://127.0.0.1:5000/api/v1/execute-qr-transaction-v2",
        json={
            "vendor_qr_id": vendor_qr_id,
            "waiter_qr_id": waiter_qr_id,
            "bill_amount": 1001,
            "tip_amount": 10,
            "v": 2,
        },
        headers=headers,
    )

    payload = loads(response.data.decode())
    assert payload["message"] == "Insufficient balance in sender's wallet"
    assert response.status_code == 400


def test_execute_qr_transaction_v2_api_incorrect_waiter_qr_id(
    seed_api_customer,
    mocker,
    client,
    seed_api_vendor,
    add_1000_wallet,
    get_qr_id_from_user_id,
):
    uow = UnitOfWork()
    customer_id, vendor_id, waiter_id, closed_loop_id = _seed_customer_vendor_waiter(
        seed_api_customer, mocker, client, seed_api_vendor, uow
    )

    vendor_qr_id = get_qr_id_from_user_id(vendor_id, uow)
    waiter_qr_id = get_qr_id_from_user_id(waiter_id, uow)

    add_1000_wallet(uow=uow, wallet_id=customer_id)

    uow.commit_close_connection()

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=customer_id)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    response = client.post(
        "http://127.0.0.1:5000/api/v1/execute-qr-transaction-v2",
        json={
            "vendor_qr_id": vendor_qr_id,
            "waiter_qr_id": str(uuid4()),
            "bill_amount": 999,
            "tip_amount": 10,
            "v": 2,
        },
        headers=headers,
    )
    payload = loads(response.data.decode())
    assert payload["message"] == "Vendor QR transaction executed successfully, Waiter transaction failed (Invalid QR code)"
    assert payload["status_code"] == 201
    assert payload["event_code"] == EventCode.WAITER_QR_KNOWN_FAILURE

def test_execute_qr_transaction_v2_api_low_balance_for_tip(
    seed_api_customer,
    mocker,
    client,
    seed_api_vendor,
    add_1000_wallet,
    get_qr_id_from_user_id,
):
    
    uow = UnitOfWork()
    customer_id, vendor_id, waiter_id, closed_loop_id = _seed_customer_vendor_waiter(
        seed_api_customer, mocker, client, seed_api_vendor, uow
    )

    vendor_qr_id = get_qr_id_from_user_id(vendor_id, uow)
    waiter_qr_id = get_qr_id_from_user_id(waiter_id, uow)

    add_1000_wallet(uow=uow, wallet_id=customer_id)

    uow.commit_close_connection()

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=customer_id)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    response = client.post(
        "http://127.0.0.1:5000/api/v1/execute-qr-transaction-v2",
        json={
            "vendor_qr_id": vendor_qr_id,
            "waiter_qr_id": waiter_qr_id,
            "bill_amount": 900,
            "tip_amount": 101,
            "v": 2,
          },
        headers=headers,
    )

          
    payload = loads(response.data.decode())
    assert payload["message"] == "Vendor QR transaction executed successfully, Waiter transaction failed (Insufficient balance in sender's wallet)"
    assert payload["status_code"] == 201
    assert payload["event_code"] == EventCode.WAITER_QR_TRANSACTION_FAILED

def test_execute_qr_transaction_v2_api_successful_transaction(
    seed_api_customer,
    mocker,
    client,
    seed_api_vendor,
    add_1000_wallet,
    get_qr_id_from_user_id,
):
    
    uow = UnitOfWork()
    customer_id, vendor_id, waiter_id, closed_loop_id = _seed_customer_vendor_waiter(
        seed_api_customer, mocker, client, seed_api_vendor, uow
    )

    vendor_qr_id = get_qr_id_from_user_id(vendor_id, uow)
    waiter_qr_id = get_qr_id_from_user_id(waiter_id, uow)

    add_1000_wallet(uow=uow, wallet_id=customer_id)

    uow.commit_close_connection()

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=customer_id)

    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    response = client.post(
        "http://127.0.0.1:5000/api/v1/execute-qr-transaction-v2",
        json={
            "vendor_qr_id": vendor_qr_id,
            "waiter_qr_id": waiter_qr_id,
            "bill_amount": 900,
            "tip_amount": 100,
            "v": 2,
        },
        headers=headers,
    )

    payload = loads(response.data.decode())
    assert payload["message"] == "Vendor and waiter QR transaction executed successfully"
    assert payload["status_code"] == 201
    assert payload["event_code"] == EventCode.WAITER_QR_TRANSACTION_SUCCESSFUL

def test_get_user_recent_transcations_api(
    seed_api_customer, seed_api_admin, mocker, client, add_1000_wallet
):
    sender_id = seed_api_customer(mocker, client)
    recipient_id = seed_api_customer(mocker, client)

    closed_loop_id = _create_closed_loop_helper(client)
    sender_unique_identifier = "26100274"
    recipient_unique_identifier = "26100290"

    client.post(
        "http://127.0.0.1:5000/api/v1/add-and-set-missing-marketing-weightages-to-zero",
        json={
            "RETOOL_SECRET": "",
        }
        headers=headers
    }

    _verify_phone_number(recipient_id, mocker, client)
    _verify_phone_number(sender_id, mocker, client)

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
    recipient_unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
        user_id=recipient_id, closed_loop_id=closed_loop_id, uow=uow
    )
    sender_unique_identifier = auth_qry.get_unique_identifier_from_user_id_and_closed_loop_id(
        user_id=sender_id, closed_loop_id=closed_loop_id, uow=uow
    )
    add_1000_wallet(uow=uow, wallet_id=sender_id)
    uow.commit_close_connection()

    # execute
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
    client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": recipient_unique_identifier,
            "amount": 100,
            "closed_loop_id": closed_loop_id,
        }
        headers=headers
    )

    # now send 100 back to sender
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=recipient_id)
    client.post(
        "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
        json={
            "recipient_unique_identifier": sender_unique_identifier,
            "amount": 100,
            "closed_loop_id": closed_loop_id,
        }
        headers=headers
    )
        

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
    response = client.get(
        "http://127.0.0.1:5000/api/v1/get-user-recent-transactions", headers=headers
    )

    # TODO: check transactions from the incoming data
    # uow = UnitOfWork()
    # txs = pmt_qry.get_all_successful_transactions_of_a_user(
    #     user_id=sender_id,
    #     offset=0,
    #     page_size=50,
    #     uow=uow,
    # )
    # uow.close_connection()

    payload = loads(response.data.decode())

    assert payload["message"] == "User recent transactions returned successfully"
    assert payload["status_code"] == 200
