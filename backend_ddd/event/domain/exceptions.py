class RegistrationNotAllowedException(Exception):
    """exception raised for when a user tries to initiate an illogical registration request"""


class EventConstraintException(Exception):
    """exception for when the system tries to violate event constraints"""
