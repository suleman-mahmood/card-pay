from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.event.domain import model as event_mdl
from core.payment.domain import model as pmt_mdl
from psycopg2.extras import DictRow


@dataclass(frozen=True)
class EventDTO:
    id: str
    status: event_mdl.EventStatus
    cancellation_reason: str
    name: str
    organizer_name: str
    venue: str
    capacity: int
    description: str
    image_url: str
    closed_loop_id: str
    event_start_timestamp: datetime
    event_end_timestamp: datetime
    registration_start_timestamp: datetime
    registration_end_timestamp: datetime
    registration_fee: int
    event_form_schema: dict
    qr_id: Optional[str]

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "EventDTO":
        return EventDTO(
            id=row["id"],
            status=event_mdl.EventStatus[row["status"]],
            cancellation_reason=row["cancellation_reason"],
            name=row["name"],
            organizer_name=row["organizer_name"],
            venue=row["venue"],
            capacity=row["capacity"],
            description=row["description"],
            image_url=row["image_url"],
            closed_loop_id=row["closed_loop_id"],
            event_start_timestamp=row["event_start_timestamp"],
            event_end_timestamp=row["event_end_timestamp"],
            registration_start_timestamp=row["registration_start_timestamp"],
            registration_end_timestamp=row["registration_end_timestamp"],
            registration_fee=row["registration_fee"],
            event_form_schema=row["event_form_schema"],
            qr_id=row["qr_id"] if "qr_id" in row else None,
        )


@dataclass(frozen=True)
class OrganizerDTO:
    id: str
    full_name: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "OrganizerDTO":
        return OrganizerDTO(
            id=row["id"],
            full_name=row["full_name"],
        )


@dataclass(frozen=True)
class DraftEventDTO:
    id: str
    name: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "DraftEventDTO":
        return DraftEventDTO(
            id=row["id"],
            name=row["name"],
        )


@dataclass(frozen=True)
class AttendanceQrDTO:
    qr_id: str
    event_id: str
    email: str
    full_name: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "AttendanceQrDTO":
        email_field = row["event_form_data"].get("fields", [])[2]
        email = email_field.get("answer")

        name_field = row["event_form_data"].get("fields", [])[0]
        full_name = name_field.get("answer")

        return AttendanceQrDTO(
            qr_id=row["qr_id"],
            event_id=row["event_id"],
            email=email,
            full_name=full_name,
        )


@dataclass(frozen=True)
class RegistrationsDTO:
    form_data: str
    attendance_status: str
    event_name: str
    created_at: str
    amount: int
    status: pmt_mdl.TransactionStatus

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "RegistrationsDTO":
        return RegistrationsDTO(
            form_data=row["form_data"],
            attendance_status=row["attendance_status"],
            event_name=row["event_name"],
            amount=row["amount"],
            status=row["status"],
            created_at=row["created_at"],
        )


@dataclass(frozen=True)
class AttendanceDTO:
    form_data: str
    attendance_status: str
    event_name: str
    registration_fee: int

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "AttendanceDTO":
        return AttendanceDTO(
            form_data=row["form_data"],
            attendance_status=row["attendance_status"],
            event_name=row["event_name"],
            registration_fee=row["registration_fee"],
        )
