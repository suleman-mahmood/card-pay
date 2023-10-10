from uuid import uuid4
from datetime import datetime, timedelta
from core.event.domain import model as mdl
from core.entrypoint.uow import UnitOfWork, FakeUnitOfWork

REGISTRATION_START = datetime.now() + timedelta(minutes=1)
REGISTRATION_END = datetime.now() + timedelta(minutes=2)
EVENT_START = datetime.now() + timedelta(minutes=3)
EVENT_END = datetime.now() + timedelta(minutes=4)


def test_events_repository_add_get(seed_event):
    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        if uow.__class__.__name__ == "UnitOfWork":
            uow.cursor.execute(
                "alter table events drop constraint events_organizer_id_fkey cascade;"
            )
        event: mdl.Event = seed_event(
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
        )
        event.status = mdl.EventStatus.APPROVED
        event.register_user(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
        )

        uow.events.add(event=event)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        uow.close_connection()


def test_events_repository_add_get_save(seed_event):
    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        if uow.__class__.__name__ == "UnitOfWork":
            uow.cursor.execute(
                "alter table events drop constraint events_organizer_id_fkey cascade;"
            )
        event: mdl.Event = seed_event(
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
        )

        uow.events.add(event=event)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        event.status = mdl.EventStatus.APPROVED
        event.register_user(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
        )

        uow.events.save(event=event)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        uow.close_connection()
