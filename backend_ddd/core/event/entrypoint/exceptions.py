class EventNotCreatedByOrganizer(Exception):
    """A non-organizer user type cannot create an event"""


class ClosedLoopDoesNotExist(Exception):
    """The closed loop doesn't exist"""
class EventDoesNotExist(Exception):
    """Event does not exist"""
