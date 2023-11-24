import json
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Dict

from core.event.adapters import exceptions as ex
from core.event.domain import model as mdl
from psycopg2.extras import DictCursor


class EventAbstractRepository(ABC):
    """Event model abstract repository."""

    @abstractmethod
    def add(self, event: mdl.Event) -> None:
        """Add event to repository."""
        pass

    @abstractmethod
    def get(self, event_id: str) -> mdl.Event:
        """Get event from repository."""
        pass

    @abstractmethod
    def save(self, event: mdl.Event) -> None:
        """Save event to repository."""
        pass


class FakeEventRepository(EventAbstractRepository):
    """Fake event repository."""

    def __init__(self):
        """Initialize."""
        self.events: Dict[str, mdl.Event] = {}

    def add(self, event: mdl.Event) -> None:
        """Add event to repository."""
        self.events[event.id] = event

    def get(self, event_id: str) -> mdl.Event:
        """Get event from repository."""
        return self.events[event_id]

    def save(self, event: mdl.Event) -> None:
        """Save event to repository."""
        self.events[event.id] = event


class EventRepository(EventAbstractRepository):
    """Event repository."""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor(cursor_factory=DictCursor)

    def add(self, event: mdl.Event) -> None:
        sql = """
            insert into events (
                id, 
                status, 
                cancellation_reason, 
                name, 
                organizer_id, 
                venue, 
                capacity, 
                description, 
                image_url, 
                closed_loop_id, 
                event_start_timestamp, 
                event_end_timestamp, 
                registration_start_timestamp, 
                registration_end_timestamp, 
                registration_fee,
                event_form_schema,
                event_type
            )
            values (
                %(id)s, 
                %(status)s, 
                %(cancellation_reason)s, 
                %(name)s, 
                %(organizer_id)s, 
                %(venue)s, 
                %(capacity)s, 
                %(description)s,
                %(image_url)s, 
                %(closed_loop_id)s, 
                %(event_start_timestamp)s, 
                %(event_end_timestamp)s, 
                %(registration_start_timestamp)s, 
                %(registration_end_timestamp)s, 
                %(registration_fee)s,
                %(event_form_schema)s,
                %(event_type)s
            )
        """
        for each in event.event_form_schema["fields"]:
            each.type = each.type.name
            for validation in each.validation:
                validation.type = validation.type.name

        event_schema = {"fields": [asdict(l) for l in event.event_form_schema["fields"]]}

        self.cursor.execute(
            sql,
            {
                "id": event.id,
                "status": event.status.name,
                "cancellation_reason": event.cancellation_reason,
                "name": event.name,
                "organizer_id": event.organizer_id,
                "venue": event.venue,
                "capacity": event.capacity,
                "description": event.description,
                "image_url": event.image_url,
                "closed_loop_id": event.closed_loop_id,
                "event_start_timestamp": event.event_start_timestamp,
                "event_end_timestamp": event.event_end_timestamp,
                "registration_start_timestamp": event.registration_start_timestamp,
                "registration_end_timestamp": event.registration_end_timestamp,
                "registration_fee": event.registration_fee,
                "event_form_schema": event_schema,
                "event_type": event.event_type.name,
            },
        )

        if len(event.registrations) == 0:
            return

        sql = """
            insert into registrations (
                qr_id, 
                user_id, 
                attendance_status, 
                event_id,
                event_form_data,
                tx_id
            )
            values
        """

        args = [
            {
                "qr_id": registration.qr_id,
                "user_id": registration.user_id,
                "attendance_status": registration.attendance_status.name,
                "event_id": event.id,
                "event_form_data": {
                    "fields": [asdict(l) for l in registration.event_form_data["fields"]]
                },
                "tx_id": registration.tx_id,
            }
            for _, registration in event.registrations.items()
        ]

        args_str = ",".join(
            self.cursor.mogrify(
                "(%(qr_id)s, %(user_id)s, %(attendance_status)s, %(event_id)s, %(event_form_data)s, %(tx_id)s)",
                x,
            ).decode("utf-8")
            for x in args
        )

        self.cursor.execute(sql + args_str)

    def get(self, event_id: str) -> mdl.Event:
        sql = """
            select
                id, 
                status, 
                cancellation_reason, 
                name, organizer_id, 
                venue, 
                capacity, 
                description, 
                image_url, 
                closed_loop_id, 
                event_start_timestamp, 
                event_end_timestamp, 
                registration_start_timestamp, 
                registration_end_timestamp, 
                registration_fee,
                event_form_schema,
                event_type
            from 
                events
            where 
                id = %(event_id)s
            for update
        """
        self.cursor.execute(sql, {"event_id": event_id})
        event_row = self.cursor.fetchone()

        if event_row is None:
            raise ex.EventNotFound(f"Event not found with id {event_id}")

        sql = """
            select 
                qr_id,
                user_id,
                attendance_status,
                event_id,
                event_form_data,
                tx_id
            from 
                registrations
            where 
                event_id = %s
         """

        self.cursor.execute(sql, [event_id])
        registration_rows = self.cursor.fetchall()

        registrations = {}
        for registration_row in registration_rows:
            event_form_data = []
            for v in registration_row["event_form_data"]["fields"]:
                event_form_data.append(
                    mdl.EventFormDataItem(question=v["question"], answer=v["answer"])
                )
            registration_key = (
                registration_row["user_id"]
                if registration_row["tx_id"] is None
                else registration_row["qr_id"]
            )
            registrations[registration_key] = mdl.Registration(
                qr_id=registration_row["qr_id"],
                user_id=registration_row["user_id"],
                attendance_status=mdl.EventAttendanceStatus[registration_row["attendance_status"]],
                event_form_data={"fields": event_form_data},
                tx_id=registration_row["tx_id"],
            )

        event_form_schema = []
        for each in event_row["event_form_schema"].get("fields", []):
            validation_rules = []
            for val in each["validation"]:
                val["type"] = mdl.ValidationEnum[val["type"]]
                val = mdl.ValidationRule(type=val["type"], value=val["value"])
                validation_rules.append(val)
            each = mdl.EventFormSchemaItem(
                question=each["question"],
                type=mdl.QuestionType[each["type"]],
                validation=validation_rules,
                options=each["options"],
            )
            event_form_schema.append(each)

        event_form_schema = {"fields": event_form_schema}

        return mdl.Event(
            id=event_row["id"],
            status=mdl.EventStatus[event_row["status"]],
            registrations=registrations,
            cancellation_reason=event_row["cancellation_reason"],
            name=event_row["name"],
            organizer_id=event_row["organizer_id"],
            venue=event_row["venue"],
            capacity=event_row["capacity"],
            description=event_row["description"],
            image_url=event_row["image_url"],
            closed_loop_id=event_row["closed_loop_id"],
            event_start_timestamp=event_row["event_start_timestamp"],
            event_end_timestamp=event_row["event_end_timestamp"],
            registration_start_timestamp=event_row["registration_start_timestamp"],
            registration_end_timestamp=event_row["registration_end_timestamp"],
            registration_fee=event_row["registration_fee"],
            event_form_schema=event_form_schema,
            event_type=mdl.EventType[event_row["event_type"]],
        )

    def save(self, event: mdl.Event) -> None:
        sql = """
            insert into events (
                id, 
                status, 
                cancellation_reason, 
                name, 
                organizer_id, 
                venue, 
                capacity, 
                description, 
                image_url, 
                closed_loop_id, 
                event_start_timestamp, 
                event_end_timestamp, 
                registration_start_timestamp, 
                registration_end_timestamp, 
                registration_fee,
                event_form_schema,
                event_type
            )
            values (
                %(id)s, 
                %(status)s, 
                %(cancellation_reason)s, 
                %(name)s, 
                %(organizer_id)s, 
                %(venue)s, 
                %(capacity)s, 
                %(description)s,
                %(image_url)s, 
                %(closed_loop_id)s, 
                %(event_start_timestamp)s, 
                %(event_end_timestamp)s, 
                %(registration_start_timestamp)s, 
                %(registration_end_timestamp)s, 
                %(registration_fee)s,
                %(event_form_schema)s,
                %(event_type)s
            )
            on conflict (id) do update set
                status = excluded.status,
                cancellation_reason = excluded.cancellation_reason,
                name = excluded.name,
                organizer_id = excluded.organizer_id,
                venue = excluded.venue,
                capacity = excluded.capacity,
                description = excluded.description,
                image_url = excluded.image_url,
                closed_loop_id = excluded.closed_loop_id,
                event_start_timestamp = excluded.event_start_timestamp,
                event_end_timestamp = excluded.event_end_timestamp,
                registration_start_timestamp = excluded.registration_start_timestamp,
                registration_end_timestamp = excluded.registration_end_timestamp,
                registration_fee = excluded.registration_fee,
                event_form_schema = excluded.event_form_schema,
                event_type = excluded.event_type
        """

        for each in event.event_form_schema["fields"]:
            each.type = each.type.name
            for validation in each.validation:
                validation.type = validation.type.name

        event_schema = {"fields": [asdict(l) for l in event.event_form_schema["fields"]]}

        self.cursor.execute(
            sql,
            {
                "id": event.id,
                "status": event.status.name,
                "cancellation_reason": event.cancellation_reason,
                "name": event.name,
                "organizer_id": event.organizer_id,
                "venue": event.venue,
                "capacity": event.capacity,
                "description": event.description,
                "image_url": event.image_url,
                "closed_loop_id": event.closed_loop_id,
                "event_start_timestamp": event.event_start_timestamp,
                "event_end_timestamp": event.event_end_timestamp,
                "registration_start_timestamp": event.registration_start_timestamp,
                "registration_end_timestamp": event.registration_end_timestamp,
                "registration_fee": event.registration_fee,
                "event_form_schema": event_schema,
                "event_type": event.event_type.name,
            },
        )

        if len(event.registrations) == 0:
            return

        sql = """
            insert into registrations (
                qr_id, 
                user_id, 
                attendance_status, 
                event_id,
                event_form_data,
                tx_id
            )
            values
        """

        conflict_sql = """
            on conflict (qr_id) do update set
                user_id = excluded.user_id,
                attendance_status = excluded.attendance_status,
                event_id = excluded.event_id,
                event_form_data = excluded.event_form_data,
                tx_id = excluded.tx_id
        """

        args = [
            {
                "qr_id": registration.qr_id,
                "user_id": registration.user_id,
                "attendance_status": registration.attendance_status.name,
                "event_id": event.id,
                "event_form_data": {
                    "fields": [asdict(l) for l in registration.event_form_data["fields"]]
                },
                "tx_id": registration.tx_id,
            }
            for _, registration in event.registrations.items()
        ]

        args_str = ",".join(
            self.cursor.mogrify(
                "(%(qr_id)s, %(user_id)s, %(attendance_status)s, %(event_id)s, %(event_form_data)s, %(tx_id)s)",
                x,
            ).decode("utf-8")
            for x in args
        )

        self.cursor.execute(sql + args_str + conflict_sql)
