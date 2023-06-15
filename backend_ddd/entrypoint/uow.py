from abc import ABC, abstractmethod
from ..payment.adapters.repository import (
    TransactionAbstractRepository,
    FakeTransactionRepository,
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
