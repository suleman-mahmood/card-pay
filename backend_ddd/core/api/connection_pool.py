import os
from dataclasses import dataclass
from random import randint
from typing import Optional

import psycopg2.pool
from dotenv import load_dotenv

load_dotenv()

"""
    --- --- --- --- --- --- --- --- --- --- --- ---
    Connection Pooling Setup
    --- --- --- --- --- --- --- --- --- --- --- ---
"""


def singleton(cls):
    cls.__call__ = lambda self: self
    return cls()


@singleton
@dataclass
class ConnectionPool:
    pool: Optional[psycopg2.pool.ThreadedConnectionPool] = None

    def __post_init__(self):
        db_host = os.environ.get("DB_HOST")
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_pass = os.environ.get("DB_PASSWORD")
        db_port = os.environ.get("DB_PORT")
        db_connect_timeout = os.environ.get("DB_CONNECT_TIMEOUT")
        db_minimum_connections = os.environ.get("DB_MIN_CON")
        db_maximum_connections = os.environ.get("DB_MAX_CON")

        self.pool = psycopg2.pool.ThreadedConnectionPool(
            db_minimum_connections,
            db_maximum_connections,
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_pass,
            port=db_port,
            connect_timeout=db_connect_timeout,
        )
