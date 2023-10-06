from uuid import uuid4
from datetime import datetime, timedelta
from core.event.domain import model as mdl
from core.entrypoint.uow import UnitOfWork, FakeUnitOfWork


def test_events_repository_add_get(seed_event):
    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        event: mdl.Event = seed_event()
        event.status = mdl.EventStatus.APPROVED
        event.register_user(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=datetime.now() + timedelta(seconds=1.5),
        )

        uow.events.add(event=event)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        uow.close_connection()


def test_events_repository_add_get_save(seed_event):
    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        event: mdl.Event = seed_event()

        uow.events.add(event=event)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        event.status = mdl.EventStatus.APPROVED
        event.register_user(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=datetime.now() + timedelta(seconds=1.5),
        )

        uow.events.save(event=event)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        uow.close_connection()
