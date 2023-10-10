"""event command tests"""
from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from core.entrypoint.uow import AbstractUnitOfWork, FakeUnitOfWork
from core.event.domain import exceptions as event_mdl_ex
from core.event.domain import model as event_mdl
from core.event.entrypoint import anti_corruption as acl
from core.event.entrypoint import commands as event_cmd

REGISTRATION_START = datetime.now() + timedelta(seconds=1)
REGISTRATION_END = datetime.now() + timedelta(seconds=2)
EVENT_START = datetime.now() + timedelta(seconds=3)
EVENT_END = datetime.now() + timedelta(seconds=4)


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


def test_register_user(seed_event):
    uow = FakeUnitOfWork()

    user_id = str(uuid4())
    qr_id = str(uuid4())
    closed_loop_id = str(uuid4())

    event = seed_event_cmd(seed_event=seed_event, closed_loop_id=closed_loop_id, uow=uow)

    with pytest.raises(event_mdl_ex.EventNotApproved):
        event_cmd.register_user(
            event_id=event.id,
            qr_id=qr_id,
            user_id=user_id,
            users_closed_loop_ids=[closed_loop_id],
            current_time=datetime.now(),
            uow=uow,
        )

    event_cmd.publish(event_id=event.id, uow=uow)
    event_cmd.register_user(
        event_id=event.id,
        qr_id=qr_id,
        user_id=user_id,
        users_closed_loop_ids=[closed_loop_id],
        current_time=REGISTRATION_START,
        uow=uow,
    )
    fetched_event = uow.events.get(event_id=event.id)

    assert fetched_event.registrations == {
        user_id: event_mdl.Registration(
            qr_id=qr_id,
            user_id=user_id,
            attendance_status=event_mdl.EventAttendanceStatus.UN_ATTENDED,
        )
    }


def test_mark_attendance(seed_event):
    uow = FakeUnitOfWork()

    user_id = str(uuid4())
    qr_id = str(uuid4())
    closed_loop_id = str(uuid4())

    event = seed_event_cmd(seed_event=seed_event, closed_loop_id=closed_loop_id, uow=uow)

    event_cmd.publish(event_id=event.id, uow=uow)
    event_cmd.register_user(
        event_id=event.id,
        qr_id=qr_id,
        user_id=user_id,
        users_closed_loop_ids=[closed_loop_id],
        current_time=REGISTRATION_START,
        uow=uow,
    )

    fetched_event = uow.events.get(event_id=event.id)
    assert fetched_event.registrations == {
        user_id: event_mdl.Registration(
            qr_id=qr_id,
            user_id=user_id,
            attendance_status=event_mdl.EventAttendanceStatus.UN_ATTENDED,
        )
    }
    event_cmd.mark_attendance(
        event_id=event.id,
        user_id=user_id,
        current_time=REGISTRATION_START,
        uow=uow,
    )

    fetched_event = uow.events.get(event_id=event.id)
    assert fetched_event.registrations == {
        user_id: event_mdl.Registration(
            qr_id=qr_id,
            user_id=user_id,
            attendance_status=event_mdl.EventAttendanceStatus.ATTENDED,
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
