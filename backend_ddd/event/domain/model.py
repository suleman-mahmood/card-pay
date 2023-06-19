"""events microservice domain model"""

from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from datetime import datetime
from .exceptions import TransactionNotAllowedException


@dataclass
class Registration:
    """registration value object"""

    created_at: datetime = datetime.now()

    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class EventType:
    """event type enum"""

    STANDARD = 1
    CONCERT = 2
    DONATION = 3


    
