"""Repository interface for authentication module."""
from abc import ABC, abstractmethod
from typing import Dict
from ..domain.model import (
    ClosedLoop,
    User,
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


class FakeClosedLoopRepository(ClosedLoopAbstractRepository):
    """Fake Authentication Repository"""

    def __init__(self):
        self.closed_loops: Dict[str, ClosedLoop] = {}

    def add(self, closed_loop: ClosedLoop):
        self.closed_loops[closed_loop.id] = closed_loop

    def get(self, closed_loop_id: str) -> ClosedLoop:
        return self.closed_loops[closed_loop_id]

    def save(self, closed_loop: ClosedLoop):
        self.closed_loops[closed_loop.id] = closed_loop


class FakeUserRepository(UserAbstractRepository):
    """Fake Authentication Repository"""

    def __init__(self):
        self.users: Dict[str, User] = {}

    def add(self, user: User):
        self.users[user.id] = user

    def get(self, user_id: str) -> User:
        return self.users[user_id]

    def save(self, user: User):
        self.users[user.id] = user


class ClosedLoopRepository(ClosedLoopAbstractRepository):

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, closed_loop: ClosedLoop):

        sql = "INSERT INTO closed_loops (id, name, logo_url, description, regex, verification_type) VALUES (%s, %s, %s, %s, %s, %s)"

        self.cursor.execute(sql, (closed_loop.id, closed_loop.name, closed_loop.logo_url,
                            closed_loop.description, closed_loop.regex, closed_loop.verification_type))

    def get(self, closed_loop_id: str) -> ClosedLoop:

        sql = "SELECT * FROM closed_loops WHERE id = %s"

        self.cursor.execute(sql, (closed_loop_id,))

        row = self.cursor.fetchone()

        return ClosedLoop(id=row[0], name=row[1], logo_url=row[2], description=row[3], regex=row[4], verification_type=row[5], created_at=row[6])

    def save(self, closed_loop: ClosedLoop):
            
        sql = "UPDATE closed_loops SET name = %s, logo_url = %s, description = %s, regex = %s, verification_type = %s WHERE id = %s"

        self.cursor.execute(sql, (closed_loop.name, closed_loop.logo_url,closed_loop.description, closed_loop.regex, closed_loop.verification_type, closed_loop.id))


