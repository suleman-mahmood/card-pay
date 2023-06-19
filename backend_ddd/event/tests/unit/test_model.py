from ...domain.model import Registration, EventType, EventApprovalStatus, Event
from uuid import uuid4
import pytest
from ...domain.exceptions import *


def test_create_event_draft(seed_event):
    event = seed_event()

    event.create_draft()

    assert event.approval_status == EventApprovalStatus.DRAFT


def test_publish_event_draft(seed_event):
    event = seed_event()
    event.create_draft()

    event.publish_draft()

    assert event.approval_status == EventApprovalStatus.PENDING


def test_approve_event(seed_event):
    event = seed_event()
    event.publish_draft()
    event.publish_draft()

    event.approve_draft()

    assert event.approval_status == EventApprovalStatus.APPROVED


def test_decline_event(seed_event):
    event = seed_event()
    event.publish_draft()
    event.publish_draft()

    event.decline_draft()

    assert event.approval_status == EventApprovalStatus.DRAFT


def test_register_for_event(seed_event, seed_registration):
    event = seed_event()  # event has one capacity
    registration = seed_registration()

    event.register(registration)

    assert self.event.registrations[0] == registration

    with pytest.raises(RegistrationException) as e_info:
        event.register(registration)

    assert str(e_info.value) == "registration already exists"

    with pytest.raises(RegistrationException) as e_info:
        new_registration = seed_registration()
        event.register(new_registration)  # post-cap reached registration

    assert str(e_info.value) == "registration limit reached"



