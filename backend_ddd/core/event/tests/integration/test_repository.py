import copy
from datetime import datetime, timedelta
from uuid import uuid4

from core.entrypoint.uow import FakeUnitOfWork, UnitOfWork
from core.event.domain import model as mdl

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
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
            event_form_data={"fields": []},
            paid_registrations_count=0,
        )

        uow.events.add(event=event)
        repo_event = uow.events.get(event_id=event.id)

        assert repo_event.event_form_schema == {"fields": []}
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

        event.event_form_schema = {
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
                    question="What is your name?",
                    type=mdl.QuestionType.INPUT_STR,
                    validation=[
                        mdl.ValidationRule(type=mdl.ValidationEnum.REQUIRED, value=True),
                        mdl.ValidationRule(type=mdl.ValidationEnum.MIN_LENGTH, value=10),
                        mdl.ValidationRule(type=mdl.ValidationEnum.MAX_LENGTH, value=25),
                    ],
                    options=[],
                ),
            ]
        }

        event_copy = copy.deepcopy(event)

        uow.events.add(event=event_copy)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        event_form_data = [
            mdl.EventFormDataItem(question="What is your name?", answer="Khuzaima"),
            mdl.EventFormDataItem(question="What is your age?", answer=21),
        ]

        event.status = mdl.EventStatus.APPROVED
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
            event_form_data={"fields": event_form_data},
            paid_registrations_count=0,
        )

        event_copy_v2 = copy.deepcopy(event)
        uow.events.save(event=event_copy_v2)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        uow.close_connection()


def test_events_repository_add_get_save_form_schema(seed_event):
    # for uow in [UnitOfWork(), FakeUnitOfWork()]:
    for uow in [UnitOfWork()]:
        if uow.__class__.__name__ == "UnitOfWork":
            uow.cursor.execute(
                "alter table events drop constraint events_organizer_id_fkey cascade;"
            )
        event: mdl.Event = seed_event(
            registration_start_timestamp=REGISTRATION_START,
            registration_end_timestamp=REGISTRATION_END,
            event_start_timestamp=EVENT_START,
            event_end_timestamp=EVENT_END,
            capacity=2,
        )

        event.event_form_schema = {
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
                    question="What is your name?",
                    type=mdl.QuestionType.INPUT_STR,
                    validation=[
                        mdl.ValidationRule(type=mdl.ValidationEnum.REQUIRED, value=True),
                        mdl.ValidationRule(type=mdl.ValidationEnum.MIN_LENGTH, value=10),
                        mdl.ValidationRule(type=mdl.ValidationEnum.MAX_LENGTH, value=25),
                    ],
                    options=[],
                ),
            ]
        }

        event_copy = copy.deepcopy(event)

        uow.events.add(event=event_copy)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        event.status = mdl.EventStatus.APPROVED

        event_form_data_1 = [
            mdl.EventFormDataItem(question="What is your name?", answer="Khuzaima"),
            mdl.EventFormDataItem(question="What is your age?", answer=21),
        ]
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
            event_form_data={"fields": event_form_data_1},
            paid_registrations_count=0,
        )

        event_form_data_2 = [
            mdl.EventFormDataItem(question="What is your name?", answer="Suleman"),
            mdl.EventFormDataItem(question="What is your age?", answer=24),
        ]
        event.register_user_closed_loop(
            qr_id=str(uuid4()),
            user_id=str(uuid4()),
            users_closed_loop_ids=[event.closed_loop_id],
            current_time=REGISTRATION_START + timedelta(minutes=0.5),
            event_form_data={"fields": event_form_data_2},
            paid_registrations_count=0,
        )

        event_copy_v2 = copy.deepcopy(event)
        uow.events.save(event=event_copy_v2)
        repo_event = uow.events.get(event_id=event.id)

        assert event == repo_event

        uow.close_connection()
