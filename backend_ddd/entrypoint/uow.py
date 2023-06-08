from abc import ABC, abstractmethod
from ..payment.adapters.repository import (
    TransactionAbstractRepository,
    FakeTransactionRepository,
)


class AbstractUnitOfWork(ABC):
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
        self.transactions = FakeTransactionRepository()

    def commit(self):
        pass

    def rollback(self):
        pass
