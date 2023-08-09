"""unit of work"""
import os
from abc import ABC, abstractmethod
from google.cloud.sql.connector import Connector, IPTypes
import psycopg2

from psycopg2.extensions import adapt, register_adapter, AsIs
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
from dotenv import load_dotenv

load_dotenv()


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
        connection: psycopg2.connection
        cursor: psycopg2.cursor

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        pass

    def commit_close_connection(self):
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

        # TODO: un-comment this when deploying to app engine (Production)
        # instance_connection_name = os.environ.get("INSTANCE_CONNECTION_NAME")
        # db_name = os.environ.get("DB_NAME")
        # db_user = os.environ.get("DB_USER")
        # db_pass = os.environ.get("DB_PASS")

        # connector = Connector()
        # self.connection = connector.connect(
        #     instance_connection_name,
        #     "pg8000",
        #     db=db_name,
        #     user=db_user,
        #     password=db_pass,
        #     ip_type=IPTypes.PUBLIC,
        # )

        self.connection = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT"),
        )

        self.cursor = self.connection.cursor()

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
        self.connection.close()

    def close_connection(self):
        self.close_connection()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
