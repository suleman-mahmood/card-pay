import pytest
import os
from core.api.api import app as flask_app


@pytest.fixture(scope="session", autouse=True)
def initialize_pytest_config():
    os.environ["DB_HOST"] = os.environ["DB_HOST_LOCAL"]
    os.environ["DB_NAME"] = os.environ["DB_NAME_LOCAL"]
    os.environ["DB_USER"] = os.environ["DB_USER_LOCAL"]
    os.environ["DB_PASSWORD"] = os.environ["DB_PASSWORD_LOCAL"]
    os.environ["DB_PORT"] = os.environ["DB_PORT_LOCAL"]


@pytest.fixture()
def app():
    app = flask_app
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
