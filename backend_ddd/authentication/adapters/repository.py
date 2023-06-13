"""Repository interface for authentication module."""
from abc import ABC, abstractmethod
from typing import Dict
from ..domain.model import (
    ClosedLoopUser,
    ClosedLoopUserState,
    ClosedLoopVerificationType,
    ClosedLoop,
    User,
    UserType,
)


class ClosedLoopAbstractRepository(ABC):
    """ClosedLoop Abstract Repository"""

    @abstractmethod
    def add(self, closed_loop: ClosedLoop):
        pass

    @abstractmethod
    def get(self, closed_loop_id: str) -> ClosedLoop:
        pass

    @abstractmethod
    def save(self, closed_loop: ClosedLoop):
        pass


class UserAbstractRepository(ABC):
    """User Abstract Repository"""

    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def get(self, user_id: str) -> User:
        pass

    @abstractmethod
    def save(self, user: User):
        pass


class FakeClosedLoopAbstractRepository(ClosedLoopAbstractRepository):
    """Fake Authentication Repository"""

    def __init__(self):
        self.closed_loops: Dict[str, ClosedLoop] = {}

    def add(self, closed_loop: ClosedLoop):
        self.closed_loops[closed_loop.id] = closed_loop

    def get(self, closed_loop_id: str) -> ClosedLoop:
        return self.closed_loops[closed_loop_id]

    def save(self, closed_loop: ClosedLoop):
        self.closed_loops[closed_loop.id] = closed_loop


class FakeUserAbstractRepository(UserAbstractRepository):
    """Fake Authentication Repository"""

    def __init__(self):
        self.users: Dict[str, User] = {}

    def add(self, user: User):
        self.users[user.id] = user

    def get(self, user_id: str) -> User:
        return self.users[user_id]

    def save(self, user: User):
        self.users[user.id] = user
