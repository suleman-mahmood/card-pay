import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from core.event.domain import model as mdl, exceptions as ex

# valid event timestamps
REGISTRATION_START = datetime.now() + timedelta(seconds=1)
REGISTRATION_END = datetime.now() + timedelta(seconds=2)
EVENT_START = datetime.now() + timedelta(seconds=3)
EVENT_END = datetime.now() + timedelta(seconds=4)


def event_time_validator(event: mdl.Event) -> mdl.Event:
    event.registration_start_timestamp = datetime.now() + timedelta(seconds=1)
    event.registration_end_timestamp = datetime.now() + timedelta(seconds=2)
    event.event_start_timestamp = datetime.now() + timedelta(seconds=3)
    event.event_end_timestamp = datetime.now() + timedelta(seconds=4)

    return event


def test_publish(seed_event):
    event: mdl.Event = seed_event(status=mdl.EventStatus.APPROVED)

    with pytest.raises(
        ex.EventNotDrafted, match="Only events in draft may be published."
    ):
        event.publish()

    event.registration_start_timestamp = datetime.now() + timedelta(seconds=3)
    event.status = mdl.EventStatus.DRAFT

    with pytest.raises(
        ex.EventRegistrationEndsAfterStart,
        match="Event registration end timestamp must be after event registration start timestamp.",
    ):
        event.publish()

    event_time_validator(event)
    event.event_end_timestamp = datetime.now() + timedelta(seconds=2)

    with pytest.raises(
        ex.EventEndsBeforeStartTime,
        match="Event end timestamp must be after event start timestamp.",
    ):
        event.publish()

    event_time_validator(event)
    event.event_start_timestamp = datetime.now()

    with pytest.raises(
        ex.EventStartsBeforeRegistrationTime,
        match="Event start timestamp cannot be before event registration start timestamp.",
    ):
        event.publish()

    event_time_validator(event)
    event.registration_end_timestamp = datetime.now() + timedelta(seconds=5)

    with pytest.raises(
        ex.EventEndsBeforeRegistrationStartTime,
        match="Event end timestamp cannot be before event registration end timestamp.",
    ):
        event.publish()

    event_time_validator(event)

    with pytest.raises(
        ex.EventTicketPriceNegative,
        match="Event registration charges cannot be negative.",
    ):
        event.registration_fee = -1
        event.publish()

    event.registration_fee = 1

    with pytest.raises(
        ex.EventCapacityExceeded, match="Event capacity cannot be less than 1."
    ):
        event.capacity = 0
        event.publish()

    event.capacity = 1

    assert event.status == mdl.EventStatus.DRAFT

    event.publish()

    assert event.status == mdl.EventStatus.APPROVED


def test_update(seed_event):
    event: mdl.Event = seed_event()

    with pytest.raises(
        ex.EventUpdatePastEventEnd,
        match="Cannot update event after it has ended.",
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=1,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
            registration_fee=1,
            current_time=EVENT_END + timedelta(minutes=1),
        )

    with pytest.raises(
        ex.EventFeeUpdateAfterStart,
        match="Cannot update event registration fee if registration has begun.",
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=1,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
            registration_fee=2,
            current_time=REGISTRATION_START + timedelta(seconds=0.5),
        )

    with pytest.raises(
        ex.EventTicketPriceNegative,
        match="Event registration charges cannot be negative.",
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=1,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
            registration_fee=-1,
            current_time=REGISTRATION_START - timedelta(seconds=1),
        )

    with pytest.raises(
        ex.EventRegistrationTimeUpdateAfterStart,
        match="Cannot update event registration start timestamp to an earlier date if registration has begun.",
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=1,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_START - timedelta(seconds=1),
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
            registration_fee=1,
            current_time=REGISTRATION_START,
        )

    with pytest.raises(
        ex.EventRegistrationEndsAfterStart,
        match="Event registration end timestamp must be after event registration start timestamp.",
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=1,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_END,
            registration_end_timestamp=REGISTRATION_START,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
            registration_fee=1,
            current_time=datetime.now(),
        )

    with pytest.raises(
        ex.EventEndsBeforeStartTime,
        match="Event end timestamp must be after event start timestamp.",
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=1,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_END,
            event_end_timestamp=EVENT_START,
            registration_fee=1,
            current_time=datetime.now(),
        )

    with pytest.raises(
        ex.EventStartsBeforeRegistrationTime,
        match="Event start timestamp cannot be before event registration start timestamp.",
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=1,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=REGISTRATION_START - timedelta(seconds=1),
            event_end_timestamp=EVENT_END,
            registration_fee=1,
            current_time=datetime.now(),
        )

    with pytest.raises(
        ex.EventEndsBeforeRegistrationStartTime,
        match="Event end timestamp cannot be before event registration end timestamp.",
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=1,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=REGISTRATION_START,
            event_end_timestamp=REGISTRATION_END - timedelta(seconds=1),
            registration_fee=1,
            current_time=datetime.now(),
        )

    event.capacity = 2

    with pytest.raises(
        ex.EventCapacityExceeded,
        match="Event capacity cannot be lesser than original capacity.",
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=1,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=REGISTRATION_START,
            event_end_timestamp=REGISTRATION_END,
            registration_fee=1,
            current_time=datetime.now(),
        )

    with pytest.raises(
        ex.EventCapacityNonInteger, match="Event capacity must be an integer."
    ):
        event.update(
            name="CARD PAY FAIR",
            venue="SDSB B2",
            capacity=2.5,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=REGISTRATION_START,
            event_end_timestamp=REGISTRATION_END,
            registration_fee=1,
            current_time=datetime.now(),
        )

    event.update(
        name="MOAZ FAIR",
        venue="HOCKEY GROUND",
        capacity=2,
        description="The ultimate ahhm.",
        image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
        registration_start_timestamp=REGISTRATION_START - timedelta(seconds=1),
        registration_end_timestamp=REGISTRATION_END - timedelta(seconds=2),
        event_start_timestamp=EVENT_START - timedelta(seconds=3),
        event_end_timestamp=EVENT_END - timedelta(seconds=4),
        registration_fee=10000,
        current_time=REGISTRATION_START - timedelta(seconds=2),
    )

    assert event.name == "MOAZ FAIR"
    assert event.venue == "HOCKEY GROUND"
    assert event.capacity == 2
    assert event.description == "The ultimate ahhm."
    assert event.registration_start_timestamp == REGISTRATION_START - timedelta(
        seconds=1
    )
    assert event.registration_end_timestamp == REGISTRATION_END - timedelta(seconds=2)
    assert event.event_start_timestamp == EVENT_START - timedelta(seconds=3)
    assert event.event_end_timestamp == EVENT_END - timedelta(seconds=4)
    assert event.registration_fee == 10000


def test_register(seed_event):
    event: mdl.Event = seed_event()

    user_id = str(uuid4())

    with pytest.raises(
        ex.EventNotApproved,
        match="Cannot register to an event that is not approved.",
    ):
        event.register_user(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=[],
            current_time=datetime.now(),
        )

    event.status = mdl.EventStatus.APPROVED

    with pytest.raises(
        ex.EventNotApprovedException,
        match="Registration has not started yet.",
    ):
        event.register_user(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=[],
            current_time=REGISTRATION_START - timedelta(seconds=1),
        )

    with pytest.raises(ex.RegistrationEnded, match="Registration time has passed."):
        event.register_user(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=[],
            current_time=REGISTRATION_END + timedelta(seconds=1),
        )

    with pytest.raises(
        ex.UserInvalidClosedLoop,
        match="User is not allowed to register for this event.",
    ):
        event.register_user(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=[],
            current_time=REGISTRATION_START,
        )

    qr_id = str(uuid4())
    user_id = str(uuid4())
    closed_loop_id = str(uuid4())
    users_closed_loop_ids = [closed_loop_id]

    event.closed_loop_id = closed_loop_id

    event.register_user(
        qr_id=qr_id,
        user_id=user_id,
        users_closed_loop_ids=users_closed_loop_ids,
        current_time=REGISTRATION_START + timedelta(seconds=0.5),
    )

    assert event.registrations[user_id].qr_id == qr_id
    assert event.registrations[user_id].user_id == user_id
    assert (
        event.registrations[user_id].attendance_status
        == mdl.EventAttendanceStatus.UN_ATTENDED
    )

    with pytest.raises(
        ex.EventCapacityExceeded,
        match="This event is already at capacity.",
    ):
        event.register_user(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=users_closed_loop_ids,
            current_time=REGISTRATION_START + timedelta(seconds=0.5),
        )

    event.capacity = 2

    with pytest.raises(
        ex.RegistrationAlreadyExists,
        match="User has already registered with the event.",
    ):
        event.register_user(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=users_closed_loop_ids,
            current_time=REGISTRATION_START + timedelta(seconds=0.5),
        )

    assert len(event.registrations) == 1


def test_mark_attenance(seed_event, seed_registration):
    event: mdl.Event = seed_event()
    registration: mdl.Registration = seed_registration()

    with pytest.raises(
        ex.EventNotApproved,
        match="Cannot mark attendance for an event that is not approved.",
    ):
        event.mark_attendance(
            registraion_qr_id=registration.qr_id,
            current_time=datetime.now(),
        )

    event.status = mdl.EventStatus.APPROVED

    with pytest.raises(ex.AttendancePostEventException, match="Event has ended."):
        event.mark_attendance(
            registraion_qr_id=registration.qr_id,
            current_time=EVENT_END + timedelta(seconds=1),
        )

    with pytest.raises(
        ex.EventRegistrationNotStarted, match="Attendance has not started yet."
    ):
        event.mark_attendance(
            registraion_qr_id=registration.qr_id,
            current_time=REGISTRATION_START - timedelta(seconds=1),
        )

    with pytest.raises(
        ex.RegistrationDoesNotExist,
        match="User has not registered for this event.",
    ):
        event.mark_attendance(
            registraion_qr_id=registration.qr_id,
            current_time=REGISTRATION_START + timedelta(seconds=0.5),
        )

    event.registrations[registration.qr_id] = registration
    event.mark_attendance(
        registraion_qr_id=registration.qr_id,
        current_time=REGISTRATION_START + timedelta(seconds=0.5),
    )

    with pytest.raises(
        ex.UserIsAlreadyMarkedPresent,
        match="User has already marked attendance for this event.",
    ):
        event.mark_attendance(
            registraion_qr_id=registration.qr_id,
            current_time=REGISTRATION_START + timedelta(seconds=0.5),
        )

    assert registration.attendance_status == mdl.EventAttendanceStatus.ATTENDED


def test_cancel(seed_event):
    event: mdl.Event = seed_event()

    with pytest.raises(
        ex.EventNotApproved,
        match="Only approved events may be cancelled.",
    ):
        event.cancel(
            cancellation_reason="",
            current_time=REGISTRATION_END,
        )

    event.status = mdl.EventStatus.APPROVED

    with pytest.raises(
        ex.EventEnded,
        match="Event has already ended. Cannot cancel event after it has ended",
    ):
        event.cancel(
            cancellation_reason="",
            current_time=EVENT_END + timedelta(seconds=1),
        )

    event.cancel(
        cancellation_reason="aisay he, dil kr rha tha",
        current_time=REGISTRATION_END,
    )

    assert event.status == mdl.EventStatus.CANCELLED
    assert event.cancellation_reason == "aisay he, dil kr rha tha"
