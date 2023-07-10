"""events microservice domain model"""

from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from datetime import datetime
from .exceptions import RegistrationNotAllowedException, EventConstraintException
from typing import List


@dataclass(frozen=True)
class Registration:
    """registration value object"""

    user_id: str

    id: str = field(default_factory=lambda: str(uuid4()))

    @property
    def qr_code(self) -> str:
        """QR code"""
        return self.id


class EventType(str, Enum):
    """event type enum"""

    STANDARD = 1
    CONCERT = 2
    FUND_RAISER = 3


class EventStatus(str, Enum):
    """event approval statuses"""

    DRAFT = 1
    PENDING = 2
    APPROVED = 3
    CANCELLED = 4


@dataclass
class Event:
    name: str
    organizer: str
    venue: str
    capacity: int
    event_type: EventType
    description: str
    image_url: str
    closed_loop_id: str
    start: datetime
    end: datetime
    registrations: List[Registration] = field(default_factory=list)
    approval_status: EventStatus = EventStatus.DRAFT
    status_reason: str = field(default_factory=str)
    id: str = field(default_factory=lambda: str(uuid4()))

    def publish_draft(self):
        if self.approval_status != EventStatus.DRAFT:
            raise EventConstraintException(
                "Only events in draft may be published for approval."
            )
        self.approval_status = EventStatus.PENDING

    def approve(self):
        if self.approval_status != EventStatus.PENDING:
            raise EventConstraintException("Only pending events may be approved.")
        self.approval_status = EventStatus.APPROVED

    def decline(self):
        if self.approval_status != EventStatus.PENDING:
            raise EventConstraintException(
                "Only pending events may be declined approval."
            )
        self.approval_status = EventStatus.DRAFT

    def register(self, registration: Registration):
        if registration in self.registrations:
            raise RegistrationNotAllowedException(
                "User has already registered with the event."
            )
        if self.approval_status != EventStatus.APPROVED:
            raise EventConstraintException(
                "Cannot register to an event that is not approved."
            )
        if len(self.registrations) >= self.capacity:
            raise RegistrationNotAllowedException("This event is already at capacity.")
        self.registrations.append(registration)

    @property
    def get_start_time(self):
        pass
