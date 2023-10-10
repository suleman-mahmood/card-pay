import pytest
from core.event.domain import model as mdl
from core.event.entrypoint import commands as cmd
from core.event.entrypoint import anti_corruption as acl
from core.entrypoint.uow import AbstractUnitOfWork
from datetime import datetime, timedelta
from uuid import uuid4

# valid event timestamps
REGISTRATION_START = datetime.now() + timedelta(minutes=1)
REGISTRATION_END = datetime.now() + timedelta(minutes=2)
EVENT_START = datetime.now() + timedelta(minutes=3)
EVENT_END = datetime.now() + timedelta(minutes=4)


@pytest.fixture
def seed_event():
    def _seed_event(
        organizer_id=str(uuid4()),
        capacity=1,
        registration_fee=1,
        status=mdl.EventStatus.DRAFT,
        registration_start_timestamp=REGISTRATION_START,
        registration_end_timestamp=REGISTRATION_END,
        event_start_timestamp=EVENT_START,
        event_end_timestamp=EVENT_END,
        closed_loop_id=str(uuid4()),
    ) -> mdl.Event:
        return mdl.Event(
            id=str(uuid4()),
            status=status,
            registrations={},
            cancellation_reason="",
            name="CARD PAY FAIR",
            organizer_id=organizer_id,
            venue="SDSB B2",
            capacity=capacity,
            description="The ultimate fintech hackathon.",
            image_url="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            closed_loop_id=closed_loop_id,
            registration_start_timestamp=registration_start_timestamp,
            registration_end_timestamp=registration_end_timestamp,
            event_start_timestamp=event_start_timestamp,
            event_end_timestamp=event_end_timestamp,
            registration_fee=registration_fee,
        )

    return _seed_event


@pytest.fixture
def seed_event_cmd(seed_event):
    def _seed_event_cmd(
        uow: AbstractUnitOfWork,
        closed_loop_id: str = str(uuid4()),
        organizer_id: str = str(uuid4()),
    ):
        event = seed_event(
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
            closed_loop_id=closed_loop_id,
            organizer_id=organizer_id,
        )

        cmd.create(
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

    return _seed_event_cmd


@pytest.fixture
def seed_registration():
    def _seed_registration() -> mdl.Registration:
        return mdl.Registration(
            user_id=str(uuid4()),
            qr_id=str(uuid4()),
            attendance_status=mdl.EventAttendanceStatus.UN_ATTENDED,
        )

    return _seed_registration
