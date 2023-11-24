class EventNotCreatedByOrganizer(Exception):
    """A non-organizer user type cannot create an event"""


class ClosedLoopDoesNotExist(Exception):
    """The closed loop doesn't exist"""


class TxIdDoesNotExist(Exception):
    """The TxId doesn't exist"""


class InvalidAttendanceQrId(Exception):
    """The qr_id passed does not exist"""


class InvalidPaidRegistration(Exception):
    """Could not get paid registrations"""


class EventNotFound(Exception):
    """Could not find event through registration"""
