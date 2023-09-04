"""view models for application level and general purpose view models"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Version:
    """Version view model"""

    id: str
    latest_version: str
    force_update_version: str
    created_at: datetime = field(default_factory=datetime.now)
