from datetime import datetime, timedelta
from typing import List
from uuid import uuid4

import pytest
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import anti_corruption as auth_acl
from core.authentication.entrypoint import commands as auth_cmd
from core.entrypoint.uow import UnitOfWork
from core.event.domain import model as mdl
from core.event.entrypoint import commands as cmd
from core.event.entrypoint import exceptions as ex
from core.event.entrypoint import queries as qry
from core.event.entrypoint import view_models as vm


def test_get_live_events(seed_verified_auth_event_organizer, seed_event_cmd):
    uow = UnitOfWork()

    closed_loop_id = str(uuid4())
    auth_cmd.create_closed_loop(
        id=closed_loop_id,
        name="Test Closed Loop",
        logo_url="https://www.google.com",
        description="Test Closed Loop",
        verification_type="NONE",
        regex="",
        uow=uow,
    )

    event_organizer: auth_mdl.User = seed_verified_auth_event_organizer(uow)
    auth_cmd.register_closed_loop(
        user_id=event_organizer.id,
        closed_loop_id=closed_loop_id,
        unique_identifier="1234",
        uow=uow,
        auth_svc=auth_acl.AuthenticationService(),
    )

    events = qry.get_live_events(
        closed_loop_id=closed_loop_id,
        uow=uow,
    )
    assert len(events) == 0

    event: mdl.Event = seed_event_cmd(
        uow=uow,
        closed_loop_id=closed_loop_id,
        organizer_id=event_organizer.id,
    )
    cmd.publish(event_id=event.id, uow=uow)

    events: List[vm.EventDTO] = qry.get_live_events(
        closed_loop_id=closed_loop_id,
        uow=uow,
    )

    event = uow.events.get(event_id=event.id)

    assert len(events) == 1
    assert events[0] == vm.EventDTO(
        id=event.id,
        status=event.status,
        cancellation_reason=event.cancellation_reason,
        name=event.name,
        organizer_name=event_organizer.full_name,
        venue=event.venue,
        capacity=event.capacity,
        description=event.description,
        image_url=event.image_url,
        closed_loop_id=event.closed_loop_id,
        event_start_timestamp=event.event_start_timestamp,
        event_end_timestamp=event.event_end_timestamp,
        registration_start_timestamp=event.registration_start_timestamp,
        registration_end_timestamp=event.registration_end_timestamp,
        registration_fee=event.registration_fee,
        event_form_schema={"fields": []},
        qr_id=None,
    )

    uow.close_connection()


def test_get_live_events_with_type(seed_verified_auth_event_organizer, seed_event_cmd):
    uow = UnitOfWork()

    closed_loop_id = str(uuid4())
    auth_cmd.create_closed_loop(
        id=closed_loop_id,
        name="Test Closed Loop",
        logo_url="https://www.google.com",
        description="Test Closed Loop",
        verification_type="NONE",
        regex="",
        uow=uow,
    )

    event_organizer: auth_mdl.User = seed_verified_auth_event_organizer(uow)
    auth_cmd.register_closed_loop(
        user_id=event_organizer.id,
        closed_loop_id=closed_loop_id,
        unique_identifier="1234",
        uow=uow,
        auth_svc=auth_acl.AuthenticationService(),
    )

    event: mdl.Event = seed_event_cmd(
        uow=uow,
        closed_loop_id=closed_loop_id,
        organizer_id=event_organizer.id,
        event_type=mdl.EventType.INTERNAL,
    )
    cmd.publish(event_id=event.id, uow=uow)

    events: List[vm.EventDTO] = qry.get_live_events(
        closed_loop_id=closed_loop_id,
        uow=uow,
        event_type=mdl.EventType.EXTERNAL,
    )

    event = uow.events.get(event_id=event.id)
    assert len(events) == 0

    events: List[vm.EventDTO] = qry.get_live_events(
        closed_loop_id=closed_loop_id,
        uow=uow,
        event_type=mdl.EventType.INTERNAL,
    )
    event = uow.events.get(event_id=event.id)

    assert len(events) == 1
    assert events[0] == vm.EventDTO(
        id=event.id,
        status=event.status,
        cancellation_reason=event.cancellation_reason,
        name=event.name,
        organizer_name=event_organizer.full_name,
        venue=event.venue,
        capacity=event.capacity,
        description=event.description,
        image_url=event.image_url,
        closed_loop_id=event.closed_loop_id,
        event_start_timestamp=event.event_start_timestamp,
        event_end_timestamp=event.event_end_timestamp,
        registration_start_timestamp=event.registration_start_timestamp,
        registration_end_timestamp=event.registration_end_timestamp,
        registration_fee=event.registration_fee,
        event_form_schema={"fields": []},
        qr_id=None,
    )

    uow.close_connection()


def test_get_registered_events(
    seed_verified_auth_event_organizer, seed_verified_auth_user, seed_event_cmd
):
    uow = UnitOfWork()

    closed_loop_id = str(uuid4())
    auth_cmd.create_closed_loop(
        id=closed_loop_id,
        name="Test Closed Loop",
        logo_url="https://www.google.com",
        description="Test Closed Loop",
        verification_type="NONE",
        regex="",
        uow=uow,
    )

    event_organizer: auth_mdl.User = seed_verified_auth_event_organizer(uow)
    auth_cmd.register_closed_loop(
        user_id=event_organizer.id,
        closed_loop_id=closed_loop_id,
        unique_identifier="1234",
        uow=uow,
        auth_svc=auth_acl.AuthenticationService(),
    )

    event: mdl.Event = seed_event_cmd(
        uow=uow,
        closed_loop_id=closed_loop_id,
        organizer_id=event_organizer.id,
    )
    cmd.publish(event_id=event.id, uow=uow)

    user: auth_mdl.User
    user, _ = seed_verified_auth_user(uow)

    events = qry.get_registered_events(
        user_id=user.id,
        uow=uow,
    )
    assert len(events) == 0

    event_form_data = [
        mdl.EventFormDataItem(question="What is your name?", answer="Khuzaima"),
        mdl.EventFormDataItem(question="What is your age?", answer=21),
    ]

    cmd.register_user_closed_loop(
        event_id=event.id,
        qr_id=str(uuid4()),
        user_id=user.id,
        users_closed_loop_ids=[closed_loop_id],
        current_time=datetime.now() + timedelta(minutes=1.5),
        event_form_data={"fields": event_form_data},
        uow=uow,
        paid_registrations_count=0,
    )

    events: List[vm.EventDTO] = qry.get_registered_events(
        user_id=user.id,
        uow=uow,
    )

    event = uow.events.get(event_id=event.id)

    assert len(events) == 1
    assert events[0] == vm.EventDTO(
        id=event.id,
        status=event.status,
        cancellation_reason=event.cancellation_reason,
        name=event.name,
        organizer_name=event_organizer.full_name,
        venue=event.venue,
        capacity=event.capacity,
        description=event.description,
        image_url=event.image_url,
        closed_loop_id=event.closed_loop_id,
        event_start_timestamp=event.event_start_timestamp,
        event_end_timestamp=event.event_end_timestamp,
        registration_start_timestamp=event.registration_start_timestamp,
        registration_end_timestamp=event.registration_end_timestamp,
        registration_fee=event.registration_fee,
        event_form_schema={"fields": []},
        qr_id=event.registrations[user.id].qr_id,
    )

    uow.close_connection()


def test_get_attendance_details(
    seed_verified_auth_event_organizer, seed_verified_auth_user, seed_event_cmd
):
    uow = UnitOfWork()

    closed_loop_id = str(uuid4())
    auth_cmd.create_closed_loop(
        id=closed_loop_id,
        name="Test Closed Loop",
        logo_url="https://www.google.com",
        description="Test Closed Loop",
        verification_type="NONE",
        regex="",
        uow=uow,
    )

    event_organizer: auth_mdl.User = seed_verified_auth_event_organizer(uow)
    auth_cmd.register_closed_loop(
        user_id=event_organizer.id,
        closed_loop_id=closed_loop_id,
        unique_identifier="1234",
        uow=uow,
        auth_svc=auth_acl.AuthenticationService(),
    )

    event: mdl.Event = seed_event_cmd(
        uow=uow,
        closed_loop_id=closed_loop_id,
        organizer_id=event_organizer.id,
    )
    cmd.publish(event_id=event.id, uow=uow)

    user: auth_mdl.User
    user, _ = seed_verified_auth_user(uow)

    events = qry.get_registered_events(
        user_id=user.id,
        uow=uow,
    )
    assert len(events) == 0

    email = "23100011@lums.edu.pk"
    event_form_data = [
        mdl.EventFormDataItem(question="What is your name?", answer="Khuzaima"),
        mdl.EventFormDataItem(question="What is your phone number?", answer="03333837363"),
        mdl.EventFormDataItem(question="What is your email?", answer=email),
        mdl.EventFormDataItem(question="What is your age?", answer=21),
    ]

    paypro_id = str(uuid4())
    qr_id = str(uuid4())
    cmd.register_user_open_loop(
        event_id=event.id,
        qr_id=qr_id,
        current_time=datetime.now() + timedelta(minutes=1.5),
        event_form_data={"fields": event_form_data},
        tx_id="",
        uow=uow,
        paid_registrations_count=0,
    )

    attendance_details = qry.get_attendance_details(tx_id="", uow=uow)

    assert attendance_details == vm.AttendanceQrDTO(
        qr_id=qr_id, event_id=event.id, email=email, full_name="Khuzaima"
    )

    uow.close_connection()


def test_get_attendance_data(
    seed_verified_auth_event_organizer, seed_verified_auth_user, seed_event_cmd
):
    uow = UnitOfWork()

    closed_loop_id = str(uuid4())
    auth_cmd.create_closed_loop(
        id=closed_loop_id,
        name="Test Closed Loop",
        logo_url="https://www.google.com",
        description="Test Closed Loop",
        verification_type="NONE",
        regex="",
        uow=uow,
    )

    event_organizer: auth_mdl.User = seed_verified_auth_event_organizer(uow)
    auth_cmd.register_closed_loop(
        user_id=event_organizer.id,
        closed_loop_id=closed_loop_id,
        unique_identifier="1234",
        uow=uow,
        auth_svc=auth_acl.AuthenticationService(),
    )

    event: mdl.Event = seed_event_cmd(
        uow=uow,
        closed_loop_id=closed_loop_id,
        organizer_id=event_organizer.id,
    )
    cmd.publish(event_id=event.id, uow=uow)

    user: auth_mdl.User
    user, _ = seed_verified_auth_user(uow)

    events = qry.get_registered_events(
        user_id=user.id,
        uow=uow,
    )
    assert len(events) == 0

    email = "23100011@lums.edu.pk"
    event_form_data = [
        mdl.EventFormDataItem(question="What is your name?", answer="Khuzaima"),
        mdl.EventFormDataItem(question="What is your phone number?", answer="03333837363"),
        mdl.EventFormDataItem(question="What is your email?", answer=email),
        mdl.EventFormDataItem(question="What is your age?", answer=21),
    ]

    paypro_id = str(uuid4())
    qr_id = str(uuid4())
    cmd.register_user_open_loop(
        event_id=event.id,
        qr_id=qr_id,
        current_time=datetime.now() + timedelta(minutes=1.5),
        event_form_data={"fields": event_form_data},
        tx_id="",
        uow=uow,
        paid_registrations_count=0,
    )

    attendance_details = qry.get_attendance_details(tx_id="", uow=uow)

    assert attendance_details == vm.AttendanceQrDTO(
        qr_id=qr_id, event_id=event.id, email=email, full_name="Khuzaima"
    )

    event_id_from_qr = qry.get_event_from_registration(registration_id=qr_id, uow=uow)

    assert event_id_from_qr.event_id == event.id

    uow.close_connection()
