"""commands for event micro-service"""
from datetime import datetime
from typing import Dict, List

from core.entrypoint.uow import AbstractUnitOfWork
from core.event.domain import model as mdl
from core.event.entrypoint import anti_corruption as acl
from core.event.entrypoint import anti_corruption as event_acl
from core.event.entrypoint import exceptions as exc
from core.event.entrypoint import services as svc


def create(
    id: str,
    status: mdl.EventStatus,
    registrations: Dict[str, mdl.Registration],
    cancellation_reason: str,
    name: str,
    organizer_id: str,
    venue: str,
    capacity: int,
    description: str,
    image_url: str,
    closed_loop_id: str,
    event_type: str,
    registration_fee: int,
    event_start_timestamp: datetime,
    event_end_timestamp: datetime,
    registration_start_timestamp: datetime,
    registration_end_timestamp: datetime,
    uow: AbstractUnitOfWork,
    auth_acl: acl.AbstractAuthenticationService,
):
    """Create event command"""
    if not auth_acl.is_organizer(id=organizer_id, uow=uow):
        raise exc.EventNotCreatedByOrganizer("Only organizers can create an event")

    if not auth_acl.is_valid_closed_loop(id=closed_loop_id, uow=uow):
        raise exc.ClosedLoopDoesNotExist("The closed loop doesn't exist")

    event = mdl.Event(
        id=id,
        status=status,
        registrations=registrations,
        cancellation_reason=cancellation_reason,
        name=name,
        organizer_id=organizer_id,
        venue=venue,
        capacity=capacity,
        description=description,
        image_url=image_url,
        closed_loop_id=closed_loop_id,
        event_start_timestamp=event_start_timestamp,
        event_end_timestamp=event_end_timestamp,
        registration_start_timestamp=registration_start_timestamp,
        registration_end_timestamp=registration_end_timestamp,
        registration_fee=registration_fee,
        event_form_schema={"fields": []},
        event_type=mdl.EventType[event_type],
    )
    uow.events.add(event)


def publish(event_id: str, uow: AbstractUnitOfWork):
    """Publish event command"""
    event = uow.events.get(event_id=event_id)
    event.publish()
    uow.events.save(event=event)


def update(
    event_id: str,
    name: str,
    venue: str,
    capacity: int,
    description: str,
    image_url: str,
    registration_start_timestamp: datetime,
    registration_end_timestamp: datetime,
    event_start_timestamp: datetime,
    event_end_timestamp: datetime,
    registration_fee: int,
    current_time: datetime,
    uow: AbstractUnitOfWork,
):
    event = uow.events.get(event_id=event_id)
    event.update(
        name=name,
        venue=venue,
        capacity=capacity,
        description=description,
        image_url=image_url,
        registration_start_timestamp=registration_start_timestamp,
        registration_end_timestamp=registration_end_timestamp,
        event_start_timestamp=event_start_timestamp,
        event_end_timestamp=event_end_timestamp,
        registration_fee=registration_fee,
        current_time=current_time,
    )
    uow.events.save(event=event)


def register_user_closed_loop(
    event_id: str,
    qr_id: str,
    user_id,
    users_closed_loop_ids: List[str],
    current_time: datetime,
    event_form_data: Dict[str, List[mdl.EventFormDataItem]],
    paid_registrations_count: int,
    uow: AbstractUnitOfWork,
):
    event = uow.events.get(event_id=event_id)
    event.register_user_closed_loop(
        qr_id=qr_id,
        user_id=user_id,
        users_closed_loop_ids=users_closed_loop_ids,
        current_time=current_time,
        event_form_data=event_form_data,
        paid_registrations_count=paid_registrations_count,
    )
    uow.events.save(event=event)


def register_user_open_loop(
    event_id: str,
    qr_id: str,
    current_time: datetime,
    event_form_data: Dict[str, List[mdl.EventFormDataItem]],
    tx_id: str,
    paid_registrations_count: int,
    uow: AbstractUnitOfWork,
):
    event = uow.events.get(event_id=event_id)
    event.register_user_open_loop(
        qr_id=qr_id,
        current_time=current_time,
        event_form_data=event_form_data,
        tx_id=tx_id,
        paid_registrations_count=paid_registrations_count,
    )
    uow.events.save(event=event)


def mark_attendance(
    qr_id: str,
    current_time: datetime,
    uow: AbstractUnitOfWork,
    event_service_acl: event_acl.AbstractEventsService,
):
    event_dto = event_service_acl.get_event_from_registration(registration_id=qr_id, uow=uow)
    event = uow.events.get(event_id=event_dto.event_id)

    registration_id = event_dto.user_id
    if qr_id == event_dto.user_id:
        registration_id = qr_id

    event.mark_attendance(
        registration_id=registration_id,
        current_time=current_time,
    )
    uow.events.save(event=event)


def cancel(
    event_id: str,
    cancellation_reason: str,
    current_time: datetime,
    uow: AbstractUnitOfWork,
):
    event = uow.events.get(event_id=event_id)
    event.cancel(
        cancellation_reason=cancellation_reason,
        current_time=current_time,
    )
    uow.events.save(event=event)


def add_form_schema(
    event_id: str,
    event_form_schema: Dict[str, List[mdl.EventFormSchemaItem]],
    current_time: datetime,
    uow: AbstractUnitOfWork,
):
    event = uow.events.get(event_id=event_id)
    event.upsert_form_schema(event_form_schema=event_form_schema, current_time=current_time)
    uow.events.save(event=event)


def increment_voucher_count(
    tx_id: str, uow: AbstractUnitOfWork, event_acl: event_acl.EventsService
):
    form_data = event_acl.get_form_data_from_transaction_id(tx_id=tx_id, uow=uow)

    sql_voucher = """
                update vouchers
                set redeemed = redeemed + 1
                where voucher.code = %(voucher_code)s    
            """

    answer = str(next(item for item in form_data if item.question == svc.VOUCHER_QUESTION).answer)
    uow.dict_cursor.execute(sql_voucher, {"voucher_code": answer})
