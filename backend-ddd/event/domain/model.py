# @dataclass
# class ClosedLoop:
#     """Closed loop entity - Aggregate root"""

#     id: str
#     name: str
#     logo_url: str
#     description: str


# class ClosedLoopUserState(str, Enum):
#     """Closed loop enum"""

#     UN_VERIFIED = 1
#     PENDING = 2
#     VERIFIED = 3


# @dataclass
# class ClosedLoopUser:
#     """Closed loop entity - Aggregate root"""

#     id: str
#     user_id: str
#     closed_loop_id: str
#     email: str = ""
#     status: ClosedLoopUserState = ClosedLoopUserState.UN_VERIFIED
#     unique_identifier: Optional[str] = None  # Roll number etc