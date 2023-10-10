from core.entrypoint.uow import AbstractUnitOfWork
from core.event.entrypoint import exceptions as event_ex
from core.event.entrypoint import view_models as event_vm


def get_live_events(
    closed_loop_id: str,
    uow: AbstractUnitOfWork,
):
    sql = """
        select
            e.id,
            e.status,
            e.cancellation_reason,
            e.name,
            u.full_name as organizer_name,
            e.venue,
            e.capacity,
            e.description,
            e.image_url,
            e.closed_loop_id,
            e.event_start_timestamp,
            e.event_end_timestamp,
            e.registration_start_timestamp,
            e.registration_end_timestamp,
            e.registration_fee
        from
            events e
            inner join users u on u.id = e.organizer_id
        where
            e.status = 'APPROVED'
            and e.closed_loop_id = %(closed_loop_id)s
            and e.event_end_timestamp > NOW()
    """
    uow.dict_cursor.execute(sql, {"closed_loop_id": closed_loop_id})
    events = uow.dict_cursor.fetchall()

    return [event_vm.EventDTO.from_db_dict_row(event) for event in events]


def get_registered_events(
    user_id: str,
    uow: AbstractUnitOfWork,
):
    sql = """
        select
            e.id,
            e.status,
            e.cancellation_reason,
            e.name,
            u.full_name as organizer_name,
            e.venue,
            e.capacity,
            e.description,
            e.image_url,
            e.closed_loop_id,
            e.event_start_timestamp,
            e.event_end_timestamp,
            e.registration_start_timestamp,
            e.registration_end_timestamp,
            e.registration_fee,
            r.qr_id
        from 
            events e
            inner join users u on u.id = e.organizer_id
            inner join registrations r on r.event_id = e.id
        where
            r.user_id = %(user_id)s
    """
    uow.dict_cursor.execute(sql, {"user_id": user_id})
    events = uow.dict_cursor.fetchall()

    return [event_vm.EventDTO.from_db_dict_row(event) for event in events]
