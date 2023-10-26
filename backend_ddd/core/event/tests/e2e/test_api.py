import os
from datetime import datetime, timedelta
from json import loads
from uuid import uuid4

from core.api import utils
from core.authentication.entrypoint import queries as auth_qry
from core.conftest import (
    _create_closed_loop_helper,
    _marketing_setup,
    _register_user_in_closed_loop,
    _verify_phone_number,
    _verify_user_in_closed_loop,
)
from core.entrypoint.uow import UnitOfWork
from core.event.domain import model as mdl
from core.event.entrypoint import anti_corruption as acl
from core.event.entrypoint import commands as cmd


def test_add_event_form(seed_api_customer, add_1000_wallet, mocker, client):
    sender_id = seed_api_customer(mocker, client)
    closed_loop_id = _create_closed_loop_helper(client)

    _verify_phone_number(sender_id, mocker, client)
    _register_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, "26100279")

    uow = UnitOfWork()
    sender = uow.users.get(user_id=sender_id)
    uow.commit_close_connection()

    otp = sender.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, otp)

    uow = UnitOfWork()
    add_1000_wallet(uow=uow, wallet_id=sender_id)
    uow.commit_close_connection()

    event_id = str(uuid4())

    uow = UnitOfWork()
    event = mdl.Event(
        id=event_id,
        status=mdl.EventStatus.APPROVED,
        registrations={},
        cancellation_reason="",
        name="Heavy Event",
        organizer_id=sender_id,
        venue="SDSB B1",
        capacity=50,
        description="No description",
        image_url="",
        closed_loop_id=closed_loop_id,
        event_start_timestamp=datetime.now() + timedelta(hours=5) + timedelta(minutes=3),
        event_end_timestamp=datetime.now() + timedelta(hours=5) + timedelta(minutes=4),
        registration_start_timestamp=datetime.now() + timedelta(hours=5) + timedelta(minutes=1),
        registration_end_timestamp=datetime.now() + timedelta(hours=5) + timedelta(minutes=2),
        registration_fee=500,
        event_form_schema={"fields": []},
    )
    uow.events.add(event=event)
    uow.commit_close_connection()

    SECRET_KEY = os.environ["RETOOL_SECRET"]

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    response = client.post(
        "http://127.0.0.1:5000/api/v1/form-schema",
        json={
            "RETOOL_SECRET": SECRET_KEY,
            "event_id": event_id,
            "event_form_schema": {
                "fields": [
                    {
                        "question": "What is your name?",
                        "type": "INPUT_STR",
                        "validation": [
                            {"type": "MIN_LENGTH", "value": 1},
                            {"type": "MAX_LENGTH", "value": 25},
                            {"type": "REQUIRED", "value": True},
                        ],
                        "options": [],
                    },
                    {
                        "question": "What is your batch?",
                        "type": "MULTIPLE_CHOICE",
                        "validation": [{"type": "REQUIRED", "value": True}],
                        "options": ["2021", "2022", "2023", "2024"],
                    },
                ]
            },
        },
        headers=headers,
    )

    payload = loads(response.data.decode())
    assert (
        payload
        == utils.Response(message="Schema attached successfully", status_code=200, data={}).__dict__
    )


def test_register_event(seed_api_customer, add_1000_wallet, mocker, client):
    sender_id = seed_api_customer(mocker, client)
    closed_loop_id = _create_closed_loop_helper(client)

    recipient_id = seed_api_customer(mocker, client)

    event_id = str(uuid4())

    _verify_phone_number(sender_id, mocker, client)
    _register_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, "26100279")

    _verify_phone_number(recipient_id, mocker, client)
    _register_user_in_closed_loop(mocker, client, recipient_id, closed_loop_id, "23100128")

    uow = UnitOfWork()
    sender = uow.users.get(user_id=sender_id)
    recipient = uow.users.get(user_id=sender_id)
    uow.commit_close_connection()

    otp = sender.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(mocker, client, sender_id, closed_loop_id, otp)

    otp = recipient.closed_loops[closed_loop_id].unique_identifier_otp
    _verify_user_in_closed_loop(mocker, client, recipient_id, closed_loop_id, otp)

    uow = UnitOfWork()
    add_1000_wallet(uow=uow, wallet_id=sender_id)
    uow.commit_close_connection()

    uow = UnitOfWork()
    event = mdl.Event(
        id=event_id,
        status=mdl.EventStatus.APPROVED,
        registrations={},
        cancellation_reason="",
        name="Heavy Event",
        organizer_id=recipient_id,
        venue="SDSB B1",
        capacity=50,
        description="No description",
        image_url="",
        closed_loop_id=closed_loop_id,
        event_start_timestamp=datetime.now() + timedelta(hours=5) + timedelta(minutes=3),
        event_end_timestamp=datetime.now() + timedelta(hours=5) + timedelta(minutes=4),
        registration_start_timestamp=datetime.now() + timedelta(hours=5) + timedelta(minutes=1),
        registration_end_timestamp=datetime.now() + timedelta(hours=5) + timedelta(minutes=2),
        registration_fee=500,
        event_form_schema={"fields": []},
    )
    uow.events.add(event=event)
    uow.commit_close_connection()

    SECRET_KEY = os.environ["RETOOL_SECRET"]

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }
    response = client.post(
        "http://127.0.0.1:5000/api/v1/form-schema",
        json={
            "RETOOL_SECRET": SECRET_KEY,
            "event_id": event_id,
            "event_form_schema": {
                "fields": [
                    {
                        "question": "What is your name?",
                        "type": "INPUT_STR",
                        "validation": [
                            {"type": "MIN_LENGTH", "value": 1},
                            {"type": "MAX_LENGTH", "value": 25},
                            {"type": "REQUIRED", "value": True},
                        ],
                        "options": [],
                    },
                    {
                        "question": "What is your batch?",
                        "type": "MULTIPLE_CHOICE",
                        "validation": [{"type": "REQUIRED", "value": True}],
                        "options": ["2021", "2022", "2023", "2024"],
                    },
                ]
            },
        },
        headers=headers,
    )

    payload = loads(response.data.decode())
    assert (
        payload
        == utils.Response(message="Schema attached successfully", status_code=200, data={}).__dict__
    )

    uow = UnitOfWork()
    event.registration_start_timestamp = datetime.now()
    uow.events.save(event=event)
    uow.commit_close_connection()

    response = client.post(
        "http://127.0.0.1:5000/api/v1/vendor-app/register-event",
        json={
            "event_id": event_id,
            "event_form_data": {
                "fields": [
                    {"question": "What is your name?", "answer": "khuzaima"},
                    {"question": "What is your batch?", "answer": 2023},
                ]
            },
            "full_name": "Suleman Mahmood",
            "phone_number": "+923333462677",
            "email": "sulemanmahmood99@gmail.com",
        },
        headers=headers,
    )

    payload = loads(response.data.decode())
    assert (
        payload
        == utils.Response(
            message="User successfully registered for the event",
            status_code=200,
            data={"checkout_url": ""},
        ).__dict__
    )
