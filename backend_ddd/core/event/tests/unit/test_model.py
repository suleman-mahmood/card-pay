from ...domain.model import Registration, EventType, EventStatus, Event
from uuid import uuid4
import pytest
from ...domain.exceptions import (
    RegistrationNotAllowedException,
    EventConstraintException,
)


def test_create_event_draft(seed_event):
    event = seed_event()

    assert event.approval_status == EventStatus.DRAFT


def test_publish_event_draft(seed_event):
    event = seed_event()

    event.publish_draft()

    assert event.approval_status == EventStatus.PENDING


def test_approve_event(seed_event):
    event = seed_event()
    event.publish_draft()

    event.approve()

    assert event.approval_status == EventStatus.APPROVED


def test_decline_event(seed_event):
    event = seed_event()
    event.publish_draft()

    event.decline()

    assert event.approval_status == EventStatus.DRAFT


def test_register_for_event(seed_event, seed_registration):
    event = seed_event()  # event has one capacity
    registration_1 = seed_registration()

    with pytest.raises(EventConstraintException) as e_info:
        event.register(registration_1)  # registering without approving event

    assert str(e_info.value) == "Cannot register to an event that is not approved."

    event.publish_draft()
    event.approve()  # approving event
    event.register(registration_1)  # legal registration

    assert event.registrations[0] == registration_1

    with pytest.raises(RegistrationNotAllowedException) as e_info:
        event.register(registration_1)

    assert str(e_info.value) == "User has already registered with the event."
    assert len(event.registrations) == 1

    registration_2 = seed_registration()
    event.register(registration_2)

    assert len(event.registrations) == 2

    registration_3 = seed_registration()

    with pytest.raises(RegistrationNotAllowedException) as e_info:
        event.register(registration_3)  # post-cap registration

    assert str(e_info.value) == "This event is already at capacity."
