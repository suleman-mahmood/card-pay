class EventNotCreatedByOrganizer(Exception):
    """A non-organizer user type cannot create an event"""


class ClosedLoopDoesNotExist(Exception):
    """The closed loop doesn't exist"""


class InvalidAttendanceQrId(Exception):
    """The qr_id passed does not exist"""
