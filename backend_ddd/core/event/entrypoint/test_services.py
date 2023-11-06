from uuid import uuid4

from core.entrypoint.uow import FakeUnitOfWork
from core.event.domain import model as mdl
from core.event.entrypoint import commands as event_cmd
from core.event.entrypoint import services as svc
from core.event.tests.unit import test_commands as tst_cmd


def test_calculate_ticket_price(seed_event):
    uow = FakeUnitOfWork()
    qr_id = str(uuid4())

    event = tst_cmd.seed_event_cmd(seed_event=seed_event, closed_loop_id="", uow=uow)

    event_form_data = [
        mdl.EventFormDataItem(question="What is your name?", answer="Khuzaima"),
        mdl.EventFormDataItem(question="What is your age?", answer=21),
    ]

    event_cmd.publish(event_id=event.id, uow=uow)
    event_cmd.register_user_open_loop(
        event_id=event.id,
        qr_id=qr_id,
        event_form_data={"fields": event_form_data},
        current_time=tst_cmd.REGISTRATION_START,
        uow=uow,
        paypro_id="",
    )
    fetched_event = uow.events.get(event_id=event.id)

    assert fetched_event.registrations == {
        qr_id: mdl.Registration(
            qr_id=qr_id,
            user_id=qr_id,
            attendance_status=mdl.EventAttendanceStatus.UN_ATTENDED,
            event_form_data={"fields": event_form_data},
            paypro_id="",
        )
    }

    ticket_price = svc.calculate_ticket_price(
        event_id=event.id, form_data={"fields": event_form_data}, uow=uow
    )

    assert ticket_price == event.registration_fee
