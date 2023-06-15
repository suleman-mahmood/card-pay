"""unit of work"""
import os
from abc import ABC, abstractmethod
import psycopg2
from ..payment.adapters.repository import (
    TransactionAbstractRepository,
    FakeTransactionRepository,
    TransactionRepository,
)
from ..authentication.adapters.repository import (
    ClosedLoopAbstractRepository,
    UserAbstractRepository,
    FakeClosedLoopAbstractRepository,
    FakeUserAbstractRepository,
)


class AbstractUnitOfWork(ABC):
    users: UserAbstractRepository
    closed_loops: ClosedLoopAbstractRepository
    transactions: TransactionAbstractRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.commit()
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.users = FakeUserAbstractRepository()
        self.closed_loops = FakeClosedLoopAbstractRepository()
        self.transactions = FakeTransactionRepository()

    def commit(self):
        pass

    def rollback(self):
        pass


class UnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.connection = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT"),
        )

        self.cursor = self.connection.cursor()

        # fix this asap
        self.transactions = TransactionRepository(self.connection)

        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
