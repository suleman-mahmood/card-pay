"""unit of work"""
import os
from abc import ABC, abstractmethod
import psycopg2

from psycopg2.extensions import adapt, register_adapter, AsIs
from psycopg2.extras import DictCursor
from ..authentication.domain.model import Location
from ..payment.adapters.repository import (
    TransactionAbstractRepository,
    FakeTransactionRepository,
    TransactionRepository,
)
from ..authentication.adapters.repository import (
    ClosedLoopAbstractRepository,
    UserAbstractRepository,
    FakeClosedLoopRepository,
    FakeUserRepository,
    ClosedLoopRepository,
    UserRepository,
)
from ..marketing.adapters.repository import (
    MarkteingUserAbstractRepository,
    MarketingUserRepository,
    CashbackSlabAbstractRepository,
    FakeCashbackSlabRepository,
    CashbackSlabRepository,
    WeightageAbstractRepository,
    FakeWeightageRepository,
    WeightageRepository,
)


def adapt_point(point: Location):
    lat = adapt(point.latitude)
    lng = adapt(point.longitude)
    return AsIs("'(%s, %s)'" % (lat, lng))


class AbstractUnitOfWork(ABC):
    users: UserAbstractRepository
    closed_loops: ClosedLoopAbstractRepository
    transactions: TransactionAbstractRepository
    marketing_users: MarkteingUserAbstractRepository
    cashback_slabs: CashbackSlabAbstractRepository
    weightages: WeightageAbstractRepository

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
        self.users = FakeUserRepository()
        self.closed_loops = FakeClosedLoopRepository()
        self.transactions = FakeTransactionRepository()
        self.cashback_slabs = FakeCashbackSlabRepository()
        self.weightages = FakeWeightageRepository()

    def commit(self):
        pass

    def rollback(self):
        pass


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        register_adapter(Location, adapt_point)

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

        self.transactions = TransactionRepository(self.connection)
        self.closed_loops = ClosedLoopRepository(self.connection)
        self.users = UserRepository(self.connection)
        self.marketing_users = MarketingUserRepository(self.connection)
        self.cashback_slabs = CashbackSlabRepository(self.connection)
        self.weightages = WeightageRepository(self.connection)

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
