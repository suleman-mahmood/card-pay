"""event command tests"""
import copy
from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from core.entrypoint.uow import AbstractUnitOfWork, FakeUnitOfWork
from core.event.domain import exceptions as event_mdl_ex
from core.event.domain import model as event_mdl
from core.event.entrypoint import anti_corruption as acl
from core.event.entrypoint import commands as event_cmd

REGISTRATION_START = datetime.now() + timedelta(minutes=1)
REGISTRATION_END = datetime.now() + timedelta(minutes=2)
EVENT_START = datetime.now() + timedelta(minutes=3)
EVENT_END = datetime.now() + timedelta(minutes=4)


def seed_event_cmd(
    seed_event,
    uow: AbstractUnitOfWork,
    closed_loop_id: str = str(uuid4()),
) -> event_mdl.Event:
    event = seed_event(
        registration_start_timestamp=REGISTRATION_START,
        registration_end_timestamp=REGISTRATION_END,
        event_start_timestamp=EVENT_START,
        event_end_timestamp=EVENT_END,
        closed_loop_id=closed_loop_id,
    )

    event_cmd.create(
        id=event.id,
        status=event.status,
        registrations=event.registrations,
        cancellation_reason=event.cancellation_reason,
        name=event.name,
        organizer_id=event.organizer_id,
        venue=event.venue,
        capacity=event.capacity,
        description=event.description,
        image_url=event.image_url,
        closed_loop_id=event.closed_loop_id,
        registration_start_timestamp=event.registration_start_timestamp,
        registration_end_timestamp=event.registration_end_timestamp,
        event_start_timestamp=event.event_start_timestamp,
        event_end_timestamp=event.event_end_timestamp,
        registration_fee=event.registration_fee,
        event_type=event_mdl.EventType.INTERNAL.name,
        uow=uow,
        auth_acl=acl.FakeAuthenticationService(),
    )
    return event


def test_create_event(seed_event):
    uow = FakeUnitOfWork()
    event = seed_event_cmd(seed_event=seed_event, uow=uow)

    fetched_event = uow.events.get(event_id=event.id)
    assert event == fetched_event
    assert fetched_event.status == event_mdl.EventStatus.DRAFT


def test_publish_event(seed_event):
    uow = FakeUnitOfWork()
    event = seed_event_cmd(seed_event=seed_event, uow=uow)

    event_cmd.publish(event_id=event.id, uow=uow)
    fetched_event = uow.events.get(event_id=event.id)

    assert fetched_event.status == event_mdl.EventStatus.APPROVED


def test_update(seed_event):
    uow = FakeUnitOfWork()
    event = seed_event_cmd(seed_event=seed_event, uow=uow)

    event_cmd.update(
        event_id=event.id,
        name=event.name,
        venue=event.venue,
        capacity=event.capacity,
        description=event.description,
        image_url=event.image_url,
        registration_start_timestamp=event.registration_start_timestamp,
        registration_end_timestamp=event.registration_end_timestamp,
        event_start_timestamp=event.event_start_timestamp,
        event_end_timestamp=event.event_end_timestamp,
        registration_fee=event.registration_fee,
        current_time=datetime.now(),
        uow=uow,
    )
    fetched_event = uow.events.get(event_id=event.id)

    assert fetched_event == event


def test_register_user_closed_loop(seed_event):
    uow = FakeUnitOfWork()

    user_id = str(uuid4())
    qr_id = str(uuid4())
    closed_loop_id = str(uuid4())

    event = seed_event_cmd(seed_event=seed_event, closed_loop_id=closed_loop_id, uow=uow)

    event_form_data = [
        event_mdl.EventFormDataItem(question="What is your name?", answer="Khuzaima"),
        event_mdl.EventFormDataItem(question="What is your age?", answer=21),
    ]

    with pytest.raises(event_mdl_ex.EventNotApproved):
        event_cmd.register_user_closed_loop(
            event_id=event.id,
            qr_id=qr_id,
            user_id=user_id,
            users_closed_loop_ids=[closed_loop_id],
            event_form_data={"fields": event_form_data},
            current_time=datetime.now(),
            uow=uow,
            paid_registrations_count=0,
        )

    event_cmd.publish(event_id=event.id, uow=uow)
    event_cmd.register_user_closed_loop(
        event_id=event.id,
        qr_id=qr_id,
        user_id=user_id,
        users_closed_loop_ids=[closed_loop_id],
        event_form_data={"fields": event_form_data},
        current_time=REGISTRATION_START,
        uow=uow,
        paid_registrations_count=0,
    )
    fetched_event = uow.events.get(event_id=event.id)

    assert fetched_event.registrations == {
        user_id: event_mdl.Registration(
            qr_id=qr_id,
            user_id=user_id,
            attendance_status=event_mdl.EventAttendanceStatus.UN_ATTENDED,
            event_form_data={"fields": event_form_data},
            paypro_id=None,
        )
    }


def test_register_user_open_loop(seed_event):
    uow = FakeUnitOfWork()

    qr_id = str(uuid4())

    event = seed_event_cmd(seed_event=seed_event, closed_loop_id="", uow=uow)

    event_form_data = [
        event_mdl.EventFormDataItem(question="What is your name?", answer="Khuzaima"),
        event_mdl.EventFormDataItem(question="What is your age?", answer=21),
    ]

    event_cmd.publish(event_id=event.id, uow=uow)
    event_cmd.register_user_open_loop(
        event_id=event.id,
        qr_id=qr_id,
        event_form_data={"fields": event_form_data},
        current_time=REGISTRATION_START,
        uow=uow,
        paypro_id="",
        paid_registrations_count=0,
    )
    fetched_event = uow.events.get(event_id=event.id)

    assert fetched_event.registrations == {
        qr_id: event_mdl.Registration(
            qr_id=qr_id,
            user_id=qr_id,
            attendance_status=event_mdl.EventAttendanceStatus.UN_ATTENDED,
            event_form_data={"fields": event_form_data},
            paypro_id="",
        )
    }


def test_mark_attendance(seed_event):
    uow = FakeUnitOfWork()

    user_id = str(uuid4())
    qr_id = str(uuid4())
    closed_loop_id = str(uuid4())

    event = seed_event_cmd(seed_event=seed_event, closed_loop_id=closed_loop_id, uow=uow)

    event_cmd.publish(event_id=event.id, uow=uow)
    event_cmd.register_user_closed_loop(
        event_id=event.id,
        qr_id=qr_id,
        user_id=user_id,
        users_closed_loop_ids=[closed_loop_id],
        event_form_data={"fields": []},
        current_time=REGISTRATION_START,
        uow=uow,
        paid_registrations_count=0,
    )

    fetched_event = uow.events.get(event_id=event.id)
    assert fetched_event.registrations == {
        user_id: event_mdl.Registration(
            qr_id=qr_id,
            user_id=user_id,
            attendance_status=event_mdl.EventAttendanceStatus.UN_ATTENDED,
            event_form_data={"fields": []},
            paypro_id=None,
        )
    }
    event_cmd.mark_attendance(
        event_id=event.id,
        registration_id=user_id,
        current_time=REGISTRATION_START,
        uow=uow,
    )

    fetched_event = uow.events.get(event_id=event.id)
    assert fetched_event.registrations == {
        user_id: event_mdl.Registration(
            qr_id=qr_id,
            user_id=user_id,
            attendance_status=event_mdl.EventAttendanceStatus.ATTENDED,
            event_form_data={"fields": []},
            paypro_id=None,
        )
    }


def test_cancel(seed_event):
    uow = FakeUnitOfWork()

    closed_loop_id = str(uuid4())

    event = seed_event_cmd(seed_event=seed_event, closed_loop_id=closed_loop_id, uow=uow)

    with pytest.raises(event_mdl_ex.EventNotApproved):
        event_cmd.cancel(
            event_id=event.id,
            cancellation_reason="Meri marzi",
            current_time=REGISTRATION_START,
            uow=uow,
        )

    event_cmd.publish(event_id=event.id, uow=uow)
    event_cmd.cancel(
        event_id=event.id,
        cancellation_reason="Meri marzi",
        current_time=REGISTRATION_START,
        uow=uow,
    )

    fetched_event = uow.events.get(event_id=event.id)
    assert fetched_event.status == event_mdl.EventStatus.CANCELLED


def test_add_form_schema(seed_event):
    uow = FakeUnitOfWork()

    closed_loop_id = str(uuid4())

    event = seed_event_cmd(seed_event=seed_event, closed_loop_id=closed_loop_id, uow=uow)

    event_cmd.publish(event_id=event.id, uow=uow)

    event.status = event_mdl.EventStatus.APPROVED
    fetched_event = copy.deepcopy(uow.events.get(event_id=event.id))
    assert fetched_event == event

    event.event_form_schema = {
        "fields": [
            event_mdl.EventFormSchemaItem(
                question="What is your name?",
                type=event_mdl.QuestionType.INPUT_STR,
                validation=[
                    event_mdl.ValidationRule(type=event_mdl.ValidationEnum.REQUIRED, value=True),
                    event_mdl.ValidationRule(type=event_mdl.ValidationEnum.MIN_LENGTH, value=10),
                    event_mdl.ValidationRule(type=event_mdl.ValidationEnum.MAX_LENGTH, value=25),
                ],
                options=[],
            ),
            event_mdl.EventFormSchemaItem(
                question="What is your name?",
                type=event_mdl.QuestionType.INPUT_STR,
                validation=[
                    event_mdl.ValidationRule(type=event_mdl.ValidationEnum.REQUIRED, value=True),
                    event_mdl.ValidationRule(type=event_mdl.ValidationEnum.MIN_LENGTH, value=10),
                    event_mdl.ValidationRule(type=event_mdl.ValidationEnum.MAX_LENGTH, value=25),
                ],
                options=[],
            ),
        ]
    }

    event_cmd.add_form_schema(
        event_id=event.id,
        event_form_schema=event.event_form_schema,
        current_time=REGISTRATION_START - timedelta(minutes=1),
        uow=uow,
    )

    fetched_event = uow.events.get(event_id=event.id)
    assert fetched_event == event

    with pytest.raises(event_mdl.ex.RegistrationStarted):
        event_cmd.add_form_schema(
            event_id=event.id,
            event_form_schema=event.event_form_schema,
            current_time=REGISTRATION_START + timedelta(minutes=1),
            uow=uow,
        )
