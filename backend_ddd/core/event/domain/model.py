"""events microservice domain model"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from core.event.domain import exceptions as ex


class EventAttendanceStatus(str, Enum):
    """Event attendance status enum"""

    UN_ATTENDED = 1
    ATTENDED = 2


@dataclass
class EventFormDataItem:
    question: str
    answer: str | int | float


@dataclass
class Registration:
    """
    Entity representing a registration for an event.

    Note: Only created when a valid registration takes place.
    """

    qr_id: str
    user_id: str
    attendance_status: EventAttendanceStatus
    event_form_data: Dict[str, List[EventFormDataItem]]
    paypro_id: Optional[str]

    @property
    def qr_code(self) -> str:
        """QR code"""
        return self.qr_id

    @classmethod
    def from_json_to_form_data(cls, event_data_json: dict) -> Dict[str, List[EventFormDataItem]]:
        return {
            "fields": [
                EventFormDataItem(question=each["question"], answer=each["answer"])
                for each in event_data_json["fields"]
            ]
        }


class EventStatus(str, Enum):
    """
    Event approval statuses.

    Events may only be in draft or approve status.
    Statuses are currectly being made with the assumption that there is no approval stage.
    """

    DRAFT = 1
    APPROVED = 2
    CANCELLED = 3


class ValidationEnum(str, Enum):
    """
    This is for form schema validation on a single item
    """

    REQUIRED = 1
    MIN_LENGTH = 2
    MAX_LENGTH = 3


class QuestionType(str, Enum):
    INPUT_STR = 1
    INPUT_INT = 2
    INPUT_FLOAT = 3
    MULTIPLE_CHOICE = 4
    DROPDOWN = 5


@dataclass
class ValidationRule:
    type: ValidationEnum
    value: int | bool


@dataclass
class EventFormSchemaItem:
    question: str
    type: QuestionType
    validation: List[ValidationRule]
    options: List[str]


@dataclass
class Event:
    """
    This is our aggregate root.

    Events require some form of registration and attending mechanism. (fund raisers do not)
    Once published, events are live for users to register to. (given registration has begun)
    """

    id: str
    status: EventStatus
    registrations: Dict[str, Registration]
    cancellation_reason: str

    name: str
    organizer_id: str
    venue: str
    capacity: int
    description: str
    image_url: str
    closed_loop_id: str
    event_start_timestamp: datetime
    event_end_timestamp: datetime
    registration_start_timestamp: datetime
    registration_end_timestamp: datetime
    registration_fee: int

    event_form_schema: Dict[str, List[EventFormSchemaItem]]

    def publish(self):
        """organiser publishes draft for approval, once published (in pending state) only admin can approve or decline"""

        if self.status != EventStatus.DRAFT:
            raise ex.EventNotDrafted("Only events in draft may be published.")

        if self.registration_end_timestamp <= self.registration_start_timestamp:
            raise ex.EventRegistrationEndsAfterStart(
                "Event registration end timestamp must be after event registration start timestamp."
            )

        if self.event_end_timestamp <= self.event_start_timestamp:
            raise ex.EventEndsBeforeStartTime(
                "Event end timestamp must be after event start timestamp."
            )

        if self.registration_start_timestamp > self.event_start_timestamp:
            raise ex.EventStartsBeforeRegistrationTime(
                "Event start timestamp cannot be before event registration start timestamp."
            )

        if self.event_end_timestamp < self.registration_end_timestamp:
            raise ex.EventEndsBeforeRegistrationStartTime(
                "Event end timestamp cannot be before event registration end timestamp."
            )

        if self.registration_fee <= 0:
            raise ex.EventTicketPriceNegative("Event registration charges cannot be negative.")

        if self.capacity < 1:
            raise ex.EventCapacityExceeded("Event capacity cannot be less than 1.")

        self.status = EventStatus.APPROVED

    def update(
        self,
        name: str,
        venue: str,
        capacity: int,
        description: str,
        image_url: str,
        registration_start_timestamp: datetime,
        registration_end_timestamp: datetime,
        event_start_timestamp: datetime,
        event_end_timestamp: datetime,
        registration_fee: int,
        current_time: datetime,
    ):
        """ """

        if current_time >= self.event_end_timestamp:
            raise ex.EventUpdatePastEventEnd("Cannot update event after it has ended.")

        if (
            registration_fee != self.registration_fee
            and current_time >= self.registration_start_timestamp
        ):
            raise ex.EventFeeUpdateAfterStart(
                "Cannot update event registration fee if registration has begun."
            )

        if registration_fee <= 0:
            raise ex.EventTicketPriceNegative("Event registration charges cannot be negative.")

        if (
            registration_start_timestamp < self.registration_start_timestamp
            and current_time >= self.registration_start_timestamp
        ):
            raise ex.EventRegistrationTimeUpdateAfterStart(
                "Cannot update event registration start timestamp to an earlier date if registration has begun."
            )

        if registration_end_timestamp <= registration_start_timestamp:
            raise ex.EventRegistrationEndsAfterStart(
                "Event registration end timestamp must be after event registration start timestamp."
            )

        if event_end_timestamp <= event_start_timestamp:
            raise ex.EventEndsBeforeStartTime(
                "Event end timestamp must be after event start timestamp."
            )

        if registration_start_timestamp > event_start_timestamp:
            raise ex.EventStartsBeforeRegistrationTime(
                "Event start timestamp cannot be before event registration start timestamp."
            )

        if event_end_timestamp < registration_end_timestamp:
            raise ex.EventEndsBeforeRegistrationStartTime(
                "Event end timestamp cannot be before event registration end timestamp."
            )

        if not isinstance(capacity, int):
            raise ex.EventCapacityNonInteger("Event capacity must be an integer.")

        if capacity < self.capacity:
            raise ex.EventCapacityExceeded(
                "Event capacity cannot be lesser than original capacity."
            )

        self.name = name
        self.venue = venue
        self.capacity = capacity
        self.description = description
        self.image_url = image_url
        self.event_start_timestamp = event_start_timestamp
        self.event_end_timestamp = event_end_timestamp
        self.registration_start_timestamp = registration_start_timestamp
        self.registration_end_timestamp = registration_end_timestamp
        self.registration_fee = registration_fee

    def _register_user(
        self,
        current_time: datetime,
        registration: Registration,
        registration_key: str,
    ):
        """
        need to carry out transaction after registering at command layer.
        only register if registration constraints are met.
        """

        if self.status != EventStatus.APPROVED:
            raise ex.EventNotApproved("Cannot register to an event that is not approved.")

        if current_time < self.registration_start_timestamp:
            raise ex.EventNotApproved("Registration has not started yet.")

        if current_time >= self.registration_end_timestamp:
            raise ex.RegistrationEnded("Registration time has passed.")

        if len(self.registrations) >= self.capacity:
            raise ex.EventCapacityExceeded("This event is already at capacity.")

        self.registrations[registration_key] = registration

    def register_user_closed_loop(
        self,
        qr_id: str,
        user_id: str,
        users_closed_loop_ids: List[str],
        current_time: datetime,
        event_form_data: Dict[str, List[EventFormDataItem]],
    ):
        if self.closed_loop_id not in users_closed_loop_ids:
            raise ex.UserInvalidClosedLoop("User is not allowed to register for this event.")

        if user_id in self.registrations:
            raise ex.RegistrationAlreadyExists("User has already registered with the event.")

        self._register_user(
            current_time=current_time,
            registration_key=user_id,
            registration=Registration(
                qr_id=qr_id,
                user_id=user_id,
                attendance_status=EventAttendanceStatus.UN_ATTENDED,
                event_form_data=event_form_data,
                paypro_id=None,
            ),
        )

    def register_user_open_loop(
        self,
        qr_id: str,
        current_time: datetime,
        event_form_data: Dict[str, List[EventFormDataItem]],
        paypro_id: str,
    ):
        self._register_user(
            current_time=current_time,
            registration_key=qr_id,
            registration=Registration(
                qr_id=qr_id,
                user_id=qr_id,
                attendance_status=EventAttendanceStatus.UN_ATTENDED,
                event_form_data=event_form_data,
                paypro_id=paypro_id,
            ),
        )

    def mark_attendance(self, user_id: str, current_time: datetime):
        if self.status != EventStatus.APPROVED:
            raise ex.EventNotApproved("Cannot mark attendance for an event that is not approved.")

        if current_time >= self.event_end_timestamp:
            raise ex.AttendancePostEventException("Event has ended.")

        if current_time < self.registration_start_timestamp:
            raise ex.EventRegistrationNotStarted("Attendance has not started yet.")

        registration = self.registrations.get(user_id)

        if registration is None:
            raise ex.RegistrationDoesNotExist("User has not registered for this event.")

        if registration.attendance_status == EventAttendanceStatus.ATTENDED:
            raise ex.UserIsAlreadyMarkedPresent(
                "User has already marked attendance for this event."
            )

        registration.attendance_status = EventAttendanceStatus.ATTENDED

    def cancel(self, cancellation_reason: str, current_time: datetime):
        """
        only admin can cancel approved events
        need to carry out a return transaction with registered amount to registered users on command layer (only if registered amount is > 0)
        """

        if self.status != EventStatus.APPROVED:
            raise ex.EventNotApproved("Only approved events may be cancelled.")

        if current_time >= self.event_end_timestamp:
            raise ex.EventEnded("Event has already ended. Cannot cancel event after it has ended.")

        self.status = EventStatus.CANCELLED
        self.cancellation_reason = cancellation_reason

    def upsert_form_schema(
        self,
        event_form_schema: Dict[str, List[EventFormSchemaItem]],
        current_time: datetime,
    ):
        if current_time < self.registration_start_timestamp:
            self.event_form_schema = event_form_schema
        else:
            raise ex.RegistrationStarted

    @classmethod
    def from_json_to_event_schema(
        cls, event_schema_json: dict
    ) -> Dict[str, List[EventFormSchemaItem]]:
        return {
            "fields": [
                EventFormSchemaItem(
                    question=each["question"],
                    type=QuestionType[each["type"]],
                    validation=[
                        ValidationRule(type=ValidationEnum[val["type"]], value=val["value"])
                        for val in each["validation"]
                    ],
                    options=each["options"],
                )
                for each in event_schema_json["fields"]
            ]
        }
