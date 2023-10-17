"""unit of work"""
import os
from abc import ABC, abstractmethod

import psycopg2
from core.authentication.adapters import repository as auth_repo
from core.authentication.domain import model as auth_mdl
from core.event.adapters import repository as event_repo
from core.marketing.adapters import repository as mktg_repo
from core.payment.adapters import repository as pmt_repo
from psycopg2.extensions import AsIs, adapt, register_adapter
from psycopg2.extras import DictCursor, Json


def adapt_point(point: auth_mdl.Location):
    lat = adapt(point.latitude)
    lng = adapt(point.longitude)
    return AsIs("'(%s, %s)'" % (lat, lng))


class AbstractUnitOfWork(ABC):
    users: auth_repo.UserAbstractRepository
    closed_loops: auth_repo.ClosedLoopAbstractRepository
    transactions: pmt_repo.TransactionAbstractRepository
    marketing_users: mktg_repo.MarketingUserAbstractRepository
    cashback_slabs: mktg_repo.CashbackSlabAbstractRepository
    weightages: mktg_repo.WeightageAbstractRepository
    events: event_repo.EventAbstractRepository

    def __init__(self) -> None:
        self.connection: psycopg2.connection
        self.cursor: psycopg2.cursor
        self.dict_cursor: DictCursor

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        pass

    def commit_close_connection(self):
        pass

    def close_connection(self):
        pass

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users = auth_repo.FakeUserRepository()
        self.marketing_users = mktg_repo.FakeMarketingUserRepository()
        self.closed_loops = auth_repo.FakeClosedLoopRepository()
        self.transactions = pmt_repo.FakeTransactionRepository()
        self.cashback_slabs = mktg_repo.FakeCashbackSlabRepository()
        self.weightages = mktg_repo.FakeWeightageRepository()
        self.events = event_repo.FakeEventRepository()

    def commit(self):
        pass

    def rollback(self):
        pass


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        register_adapter(auth_mdl.Location, adapt_point)
        register_adapter(dict, Json)

        db_host = os.environ.get("DB_HOST")
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_pass = os.environ.get("DB_PASSWORD")
        db_port = os.environ.get("DB_PORT")
        db_connect_timeout = os.environ.get("DB_CONNECT_TIMEOUT")

        self.connection = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_pass,
            port=db_port,
            connect_timeout=db_connect_timeout,
        )

        self.cursor = self.connection.cursor()
        self.dict_cursor = self.connection.cursor(cursor_factory=DictCursor)

        self.transactions = pmt_repo.TransactionRepository(self.connection)
        self.closed_loops = auth_repo.ClosedLoopRepository(self.connection)
        self.users = auth_repo.UserRepository(self.connection)
        self.marketing_users = mktg_repo.MarketingUserRepository(self.connection)
        self.cashback_slabs = mktg_repo.CashbackSlabRepository(self.connection)
        self.weightages = mktg_repo.WeightageRepository(self.connection)
        self.events = event_repo.EventRepository(self.connection)

    def __enter__(self, *args):
        super().__enter__(*args)

    def __exit__(self, *args):
        super().__exit__(*args)

    def commit_close_connection(self):
        self.commit()
        self.close_connection()

    def close_connection(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
