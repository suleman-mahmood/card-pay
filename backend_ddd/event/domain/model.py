"""events microservice domain model"""

from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from datetime import datetime
from .exceptions import *
from typing import List


@dataclass
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


class EventApprovalStatus(str, Enum):
    """event approval statuses"""

    DRAFT = 1
    PENDING = 2
    APPROVED = 3


@dataclass
class Event:
    name: str
    organizer: str
    venue: str
    capacity: int
    event_type: EventType
    description: str
    image: str
    closed_loop_id: str
    start: datetime
    end: datetime
    registrations: List[Registration] = field(default=list)
    approval_status: EventApprovalStatus = EventApprovalStatus.DRAFT
    id: str = field(default_factory=lambda: str(uuid4()))

    def register_for_event(self, registration: Registration):
        # registration = Registration()
        pass

    @property
    def get_start_time():
        pass
