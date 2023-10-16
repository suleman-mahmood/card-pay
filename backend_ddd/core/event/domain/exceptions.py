from datetime import datetime, timedelta
from typing import List

from ..domain import model as event_model


class EventNotDrafted(Exception):
    """exception for when event publish fails"""


class EventEndsBeforeStartTime(Exception):
    """exception for when event end is invalid"""


class EventStartsBeforeRegistrationTime(Exception):
    """exception for when event start is invalid"""


class EventEndsBeforeRegistrationStartTime(Exception):
    """exception for when event end is invalid"""


class EventTicketPriceNegative(Exception):
    """exception for when event fee is invalid"""


class EventCapacityExceeded(Exception):
    """exception for when event capacity is invalid upon update"""


class EventRegistrationTimeUpdateAfterStart(Exception):
    """exception for when event update is invalid"""


class EventClosedLoopIdException(Exception):
    """exception for when event closed loop id is not provided"""


class EventUpdatePastEventEnd(Exception):
    """exception for when event update is invalid as event has ended"""


class EventFeeUpdateAfterStart(Exception):
    """exception for when event fee update is invalid as registration has started"""


class EventRegistrationEndsAfterStart(Exception):
    """exception for when event end is invalid"""


class AttendanceFailedException(Exception):
    """exception for when attendance fails"""


class UnregisterationNotAllowedException(Exception):
    """exception raised for invalid unregisteration"""


class RegistrationAlreadyExists(Exception):
    """exception for when registration already exists"""


class UserInvalidClosedLoop(Exception):
    """exception for when closed loop registration is invalid"""


class RegistrationEnded(Exception):
    """exception for when registration has ended"""


class EventNotApproved(Exception):
    """exception for when attendance is attempted for non approved event"""


class EventRegistrationNotStarted(Exception):
    """exception for when attendance is attempted before registration start time"""


class RegistrationDoesNotExist(Exception):
    """exception for when attendance is attempted for invalid registrant"""


class UserIsAlreadyMarkedPresent(Exception):
    """exception for when attendance is attempted for invalid registrant"""


class AttendancePostEventException(Exception):
    """exception for when attendance is attempted after event end time"""


class EventEnded(Exception):
    """exception for when event is already ended"""


class EventCapacityNonInteger(Exception):
    """exception for when registration capacity is invalid"""


class RegistrationStarted(Exception):
    """exception for when event has already started and organizer tries to attach form"""


class DuplicateFormSchema(Exception):
    """exception for when the event already has a form"""
