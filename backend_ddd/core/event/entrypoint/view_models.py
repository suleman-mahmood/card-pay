from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.event.domain import model as event_mdl
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