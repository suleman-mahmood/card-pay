from datetime import datetime, timedelta
from typing import Dict, List
from uuid import uuid4

import pytest
from core.event.domain import exceptions as ex
from core.event.domain import model as mdl

# valid event timestamps
REGISTRATION_START = datetime.now() + timedelta(minutes=1)
REGISTRATION_END = datetime.now() + timedelta(minutes=2)
EVENT_START = datetime.now() + timedelta(minutes=3)
EVENT_END = datetime.now() + timedelta(minutes=4)


def event_time_validator(event: mdl.Event) -> mdl.Event:
    event.registration_start_timestamp = datetime.now() + timedelta(minutes=1)
    event.registration_end_timestamp = datetime.now() + timedelta(minutes=2)
    event.event_start_timestamp = datetime.now() + timedelta(minutes=3)
    event.event_end_timestamp = datetime.now() + timedelta(minutes=4)

    return event


def test_publish(seed_event):
    event: mdl.Event = seed_event(status=mdl.EventStatus.APPROVED)

    with pytest.raises(ex.EventNotDrafted, match="Only events in draft may be published."):
        event.publish()

    event.registration_start_timestamp = datetime.now() + timedelta(minutes=3)
    event.status = mdl.EventStatus.DRAFT

    with pytest.raises(
        ex.EventRegistrationEndsAfterStart,
        match="Event registration end timestamp must be after event registration start timestamp.",
    ):
        event.publish()

    event_time_validator(event)
    event.event_end_timestamp = datetime.now() + timedelta(minutes=2)

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
    event.registration_end_timestamp = datetime.now() + timedelta(minutes=5)

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

    with pytest.raises(ex.EventCapacityExceeded, match="Event capacity cannot be less than 1."):
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
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
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
            current_time=REGISTRATION_START - timedelta(minutes=1),
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
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
            registration_fee=1,
            current_time=REGISTRATION_START + timedelta(minutes=1),
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
            event_start_timestamp=REGISTRATION_START - timedelta(minutes=1),
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
            event_end_timestamp=REGISTRATION_END - timedelta(minutes=1),
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

    with pytest.raises(ex.EventCapacityNonInteger, match="Event capacity must be an integer."):
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
        registration_start_timestamp=REGISTRATION_START,
        registration_end_timestamp=REGISTRATION_END,
        event_start_timestamp=EVENT_START,
        event_end_timestamp=EVENT_END,
        registration_fee=10000,
        current_time=REGISTRATION_START - timedelta(minutes=2),
    )

    assert event.name == "MOAZ FAIR"
    assert event.venue == "HOCKEY GROUND"
    assert event.capacity == 2
    assert event.description == "The ultimate ahhm."
    assert event.registration_start_timestamp == REGISTRATION_START
    assert event.registration_end_timestamp == REGISTRATION_END
    assert event.event_start_timestamp == EVENT_START
    assert event.event_end_timestamp == EVENT_END
    assert event.registration_fee == 10000


def test_register_closed_loop(seed_event):
    event: mdl.Event = seed_event()

    user_id = str(uuid4())

    with pytest.raises(
        ex.EventNotApproved,
        match="Cannot register to an event that is not approved.",
    ):
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=datetime.now(),
            event_form_data={},
            paid_registrations_count=0,
        )

    event.status = mdl.EventStatus.APPROVED

    with pytest.raises(
        ex.EventNotApproved,
        match="Registration has not started yet.",
    ):
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=REGISTRATION_START - timedelta(minutes=1),
            event_form_data={},
            paid_registrations_count=0,
        )

    with pytest.raises(ex.RegistrationEnded, match="Registration time has passed."):
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=REGISTRATION_END + timedelta(minutes=1),
            event_form_data={},
            paid_registrations_count=0,
        )

    with pytest.raises(
        ex.UserInvalidClosedLoop,
        match="User is not allowed to register for this event.",
    ):
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=[],
            current_time=REGISTRATION_START,
            event_form_data={},
            paid_registrations_count=0,
        )

    qr_id = str(uuid4())
    user_id = str(uuid4())
    closed_loop_id = str(uuid4())
    users_closed_loop_ids = [closed_loop_id]

    event.closed_loop_id = closed_loop_id

    event.register_user_closed_loop(
        qr_id=qr_id,
        user_id=user_id,
        users_closed_loop_ids=users_closed_loop_ids,
        current_time=REGISTRATION_START + timedelta(minutes=0.5),
        event_form_data={},
        paid_registrations_count=0,
    )

    assert event.registrations[user_id].qr_id == qr_id
    assert event.registrations[user_id].user_id == user_id
    assert event.registrations[user_id].attendance_status == mdl.EventAttendanceStatus.UN_ATTENDED

    with pytest.raises(
        ex.EventCapacityExceeded,
        match="This event is already at capacity.",
    ):
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=users_closed_loop_ids,
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
            event_form_data={},
            paid_registrations_count=1,
        )

    event.capacity = 2

    with pytest.raises(
        ex.RegistrationAlreadyExists,
        match="User has already registered with the event.",
    ):
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=user_id,
            users_closed_loop_ids=users_closed_loop_ids,
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
            event_form_data={},
            paid_registrations_count=0,
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
            registration_id=registration.user_id,
            current_time=datetime.now(),
        )

    event.status = mdl.EventStatus.APPROVED

    with pytest.raises(ex.AttendancePostEventException, match="Event has ended."):
        event.mark_attendance(
            registration_id=registration.user_id,
            current_time=EVENT_END + timedelta(minutes=1),
        )

    with pytest.raises(ex.EventRegistrationNotStarted, match="Attendance has not started yet."):
        event.mark_attendance(
            registration_id=registration.user_id,
            current_time=REGISTRATION_START - timedelta(minutes=1),
        )

    with pytest.raises(
        ex.RegistrationDoesNotExist,
        match="User has not registered for this event.",
    ):
        event.mark_attendance(
            registration_id=registration.user_id,
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
        )

    event.registrations[registration.user_id] = registration
    event.mark_attendance(
        registration_id=registration.user_id,
        current_time=REGISTRATION_START + timedelta(minutes=0.5),
    )

    with pytest.raises(
        ex.UserIsAlreadyMarkedPresent,
        match="User has already marked attendance for this event.",
    ):
        event.mark_attendance(
            registration_id=registration.user_id,
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
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
            current_time=EVENT_END + timedelta(minutes=1),
        )

    event.cancel(
        cancellation_reason="aisay he, dil kr rha tha",
        current_time=REGISTRATION_END,
    )

    assert event.status == mdl.EventStatus.CANCELLED
    assert event.cancellation_reason == "aisay he, dil kr rha tha"


def test_add_update_form_schema(seed_event):
    event: mdl.Event = seed_event()

    event_form_schema: Dict[str, List[mdl.EventFormSchemaItem]] = {
        "fields": [
            mdl.EventFormSchemaItem(
                question="What is your name?",
                type=mdl.QuestionType.INPUT_STR,
                validation=[
                    mdl.ValidationRule(type=mdl.ValidationEnum.REQUIRED, value=True),
                    mdl.ValidationRule(type=mdl.ValidationEnum.MIN_LENGTH, value=10),
                    mdl.ValidationRule(type=mdl.ValidationEnum.MAX_LENGTH, value=25),
                ],
                options=[],
            ),
            mdl.EventFormSchemaItem(
                question="What is your university name?",
                type=mdl.QuestionType.DROPDOWN,
                validation=[mdl.ValidationRule(type=mdl.ValidationEnum.REQUIRED, value=True)],
                options=["LUMS", "NUST", "FAST"],
            ),
        ]
    }

    event.upsert_form_schema(
        event_form_schema=event_form_schema,
        current_time=REGISTRATION_START - timedelta(minutes=0.5),
    )

    assert event.event_form_schema is not None
    assert event.event_form_schema == event_form_schema

    event_form_schema = {
        "fields": [
            mdl.EventFormSchemaItem(
                question="What is your name?",
                type=mdl.QuestionType.INPUT_STR,
                validation=[
                    mdl.ValidationRule(type=mdl.ValidationEnum.REQUIRED, value=True),
                    mdl.ValidationRule(type=mdl.ValidationEnum.MIN_LENGTH, value=10),
                    mdl.ValidationRule(type=mdl.ValidationEnum.MAX_LENGTH, value=25),
                ],
                options=[],
            )
        ]
    }

    event.upsert_form_schema(
        event_form_schema=event_form_schema,
        current_time=REGISTRATION_START - timedelta(minutes=0.5),
    )

    assert event.event_form_schema is not None
    assert event.event_form_schema == event_form_schema
    assert len(event.event_form_schema) == 1

    with pytest.raises(ex.RegistrationStarted):
        event.upsert_form_schema(
            event_form_schema=event_form_schema,
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
        )


def test_convert_json_to_model(seed_event):
    event: mdl.Event = seed_event()
    json = {
        "fields": [
            {
                "question": "What is your name?",
                "type": "INPUT_STR",
                "validation": [
                    {"type": "MIN_LENGTH", "value": 1},
                    {"type": "MAX_LENGTH", "value": 25},
                    {"type": "REQUIRED", "value": True},
                ],
                "options": [""],
            },
            {
                "question": "What is your batch?",
                "type": "MULTIPLE_CHOICE",
                "validation": [{"type": "REQUIRED", "value": True}],
                "options": ["2021", "2022", "2023", "2024"],
            },
        ]
    }
    model_event_schema = event.from_json_to_event_schema(event_schema_json=json)
    assert type(model_event_schema) == dict


def test_register_open_loop(seed_event):
    event: mdl.Event = seed_event()
    qr_id = str(uuid4())

    event.status = mdl.EventStatus.APPROVED

    event.register_user_open_loop(
        qr_id=qr_id,
        current_time=REGISTRATION_START + timedelta(minutes=0.5),
        event_form_data={},
        tx_id="",
        paid_registrations_count=0,
    )

    assert event.registrations[qr_id].qr_id == qr_id
    assert event.registrations[qr_id].user_id == qr_id
    assert event.registrations[qr_id].attendance_status == mdl.EventAttendanceStatus.UN_ATTENDED
