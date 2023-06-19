import pytest
from ..domain import model
from datetime import datetime
from uuid import uuid4


@pytest.fixture
def seed_event():
    def _seed_event() -> model.Event:
        return model.Event(
            name="CARD PAY FAIR",
            organizer="CARD PAY SOCIETY",
            venue="SDSB B2",
            capacity=1,
            event_type=model.EventType.STANDARD,
            description="The ultimate fintech hackathon.",
            image="https://media.licdn.com/dms/image/D4D16AQGJJTwwC6-6mA/profile-displaybackgroundimage-shrink_200_800/0/1686490135139?e=2147483647&v=beta&t=eJwseRkzlGuk3D8ImC5Ga1EajMf4kdgOkK3C0oHDHT4",
            start=datetime.now,
            end=datetime.now,
            closed_loop_id=uuid4(),
        )

    return _seed_event


@pytest.fixture
def seed_registration():
    def _seed_registration() -> model.Registration:
        return model.Registration(
            user_id=str(uuid4()),
        )

    return _seed_registration
