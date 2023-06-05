import pytest
import psycopg2


@pytest.fixture
def connection():
    yield psycopg2.connect("dbname=autonomousbot")
