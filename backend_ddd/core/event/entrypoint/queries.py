import json
from typing import List, Optional

from core.entrypoint.uow import AbstractUnitOfWork
from core.event.domain import model as event_mdl
from core.event.entrypoint import exceptions as event_ex
from core.event.entrypoint import view_models as event_vm


def get_live_events(
    closed_loop_id: str,
    uow: AbstractUnitOfWork,
    event_type: Optional[event_mdl.EventType] = None,
) -> List[event_vm.EventDTO]:
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
            e.event_form_schema
        from
            events e
            inner join users u on u.id = e.organizer_id
        where
            e.status = 'APPROVED'
            and e.closed_loop_id = %(closed_loop_id)s
            and e.registration_end_timestamp > (current_timestamp at time zone '-5')
    """

    # Add the filter for event type
    if event_type is not None:
        sql += f" and (e.event_type = '{event_type.name}' or e.event_type = 'INCLUSIVE') "

    uow.dict_cursor.execute(sql, {"closed_loop_id": closed_loop_id})
    events = uow.dict_cursor.fetchall()

    return [event_vm.EventDTO.from_db_dict_row(event) for event in events]


def get_registered_events(
    user_id: str,
    uow: AbstractUnitOfWork,
) -> List[event_vm.EventDTO]:
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
            e.event_form_schema,
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


def get_all_organizers(uow: AbstractUnitOfWork) -> List[event_vm.OrganizerDTO]:
    sql = """
        select
            id,
            full_name
        from
            users
        where
            user_type = 'EVENT_ORGANIZER'::user_type_enum
        """

    uow.dict_cursor.execute(sql)
    rows = uow.dict_cursor.fetchall()

    return [event_vm.OrganizerDTO.from_db_dict_row(row) for row in rows]


def get_draft_events(uow: AbstractUnitOfWork) -> List[event_vm.DraftEventDTO]:
    sql = """
        select
            id,
            name
        from
            events
        where
            status = 'DRAFT'::event_status_enum
        """

    uow.dict_cursor.execute(sql)
    rows = uow.dict_cursor.fetchall()

    return [event_vm.DraftEventDTO.from_db_dict_row(row) for row in rows]


def get_attendance_details(paypro_id: str, uow: AbstractUnitOfWork) -> event_vm.AttendanceQrDTO:
    sql = """
        select
            qr_id,
            event_id,
            event_form_data
        from
            registrations
        where
            paypro_id = %(paypro_id)s
        """

    uow.dict_cursor.execute(sql, {"paypro_id": paypro_id})
    row = uow.dict_cursor.fetchone()

    if row is None:
        raise event_ex.PayproIdDoesNotExist

    return event_vm.AttendanceQrDTO.from_db_dict_row(row=row)


def get_registrations(
    paypro_ids: List[str], uow: AbstractUnitOfWork
) -> List[event_vm.RegistrationsDTO]:
    sql = """
        select
            r.event_form_data::json->'fields' as form_data,
            r.attendance_status,
            e.name as event_name,
            tx.amount,
            tx.status,
            r.created_at at time zone '+5' as created_at
        from
            registrations r
            join events e on e.id = r.event_id
            join transactions tx on tx.paypro_id = r.paypro_id
        where
            r.paypro_id in (select unnest(%(paypro_ids)s::text[]))
        order by r.created_at desc;
    """

    uow.dict_cursor.execute(sql, {"paypro_ids": paypro_ids})
    rows = uow.dict_cursor.fetchall()

    return [event_vm.RegistrationsDTO.from_db_dict_row(row) for row in rows]


def get_internal_registrations(
    organizer_id: str, uow: AbstractUnitOfWork
) -> List[event_vm.InternalRegistrationDTO]:
    sql = """
        select 
            u.id, 
            u.full_name, 
            u.personal_email, 
            e.name as event_name,
            u.phone_number,
            r.created_at at time zone '+5' as created_at
        from 
            users u
        inner join 
            registrations r on u.id = r.user_id
        inner join 
            events e on r.event_id = e.id
        where 
            e.organizer_id = %(organizer_id)s and r.paypro_id is null
        order by r.created_at desc;
    """
    uow.dict_cursor.execute(sql, {"organizer_id": organizer_id})
    rows = uow.dict_cursor.fetchall()

    return [event_vm.InternalRegistrationDTO.from_db_dict_row(row) for row in rows]


def get_attendance_data(qr_id: str, uow: AbstractUnitOfWork) -> event_vm.AttendanceDTO:
    sql = """
        select
            r.event_form_data::json->'fields' as form_data,
            r.attendance_status,
            e.name as event_name,
            e.registration_fee,
            u.full_name,
            ucl.unique_identifier
        from
            registrations r
            join events e on e.id = r.event_id
            left join users u on u.id = r.user_id
            left join user_closed_loops ucl on ucl.user_id = r.user_id
        where
            r.qr_id = %(qr_id)s
    """

    uow.dict_cursor.execute(sql, {"qr_id": qr_id})
    row = uow.dict_cursor.fetchone()

    if row is None:
        raise event_ex.InvalidAttendanceQrId("The qr_id passed does not exist")

    return event_vm.AttendanceDTO.from_db_dict_row(row)


def get_paid_registrations_count(event_id: str, uow: AbstractUnitOfWork) -> int:
    sql = """
        select
            count(case
                when registrations.paypro_id is null then 1
                when transactions.status = 'SUCCESSFUL' then 1
                else null
            end) as paid_registrations_count
        from
            registrations
        left join
            transactions on registrations.paypro_id = transactions.paypro_id
        where
            registrations.event_id = %(event_id)s;
    """

    uow.dict_cursor.execute(sql, {"event_id": event_id})
    row = uow.dict_cursor.fetchone()

    if row is None:
        raise event_ex.InvalidPaidRegistration("Could not get paid registrations")

    return row["paid_registrations_count"]


def get_unpaid_registrations(
    organizer_id: str, uow: AbstractUnitOfWork
) -> List[event_vm.UnpaidRegistrationsDTO]:
    sql = """
        select
            r.event_form_data::json->'fields' as form_data,
            r.attendance_status,
            e.name as event_name,
            tx.amount,
            r.created_at at time zone '+5' as created_at 
        from
            registrations r
            join events e on e.id = r.event_id
            join transactions tx on tx.paypro_id = r.paypro_id
        where
            tx.status = 'PENDING'
            and organizer_id = %(organizer_id)s
        order by r.created_at desc;
    """

    uow.dict_cursor.execute(sql, {"organizer_id": organizer_id})
    rows = uow.dict_cursor.fetchall()

    return [event_vm.UnpaidRegistrationsDTO.from_db_dict_row(row) for row in rows]


def get_event_from_registration(
    registration_id: str, uow: AbstractUnitOfWork
) -> event_vm.AttendanceEventDTO:
    sql = """
        select 
            r.event_id,
            r.user_id
        from
            registrations r
        where r.qr_id = %(registration_id)s
    """

    uow.dict_cursor.execute(sql, {"registration_id": registration_id})
    row = uow.dict_cursor.fetchone()

    if row is None:
        raise event_ex.EventNotFound("Could not find event through registration")

    return event_vm.AttendanceEventDTO.from_db_dict_row(row)
