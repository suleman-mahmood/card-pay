"""Repository interface for authentication module."""
from abc import ABC, abstractmethod
from typing import Dict
from ..domain.model import (
    ClosedLoop,
    User,
    ClosedLoopUser,
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

        sql = "SELECT id, name, logo_url, description, regex, verification_type, created_at FROM closed_loops WHERE id = %s"

        self.cursor.execute(sql, (closed_loop_id,))

        row = self.cursor.fetchone()

        return ClosedLoop(id=row[0], name=row[1], logo_url=row[2], description=row[3], regex=row[4], verification_type=row[5], created_at=row[6])

    def save(self, closed_loop: ClosedLoop):
            
        sql = '''INSERT into closed_loops SET name = %s, logo_url = %s, description = %s, regex = %s, verification_type = %s WHERE id = %s 
        on conflict(id) do update set 
        name = excluded.name,
        logo_url = excluded.logo_url,
        description = excluded.description,
        regex = excluded.regex,
        verification_type = excluded.verification_type)'''

        self.cursor.execute(sql, (closed_loop.name, closed_loop.logo_url,closed_loop.description, closed_loop.regex, closed_loop.verification_type, closed_loop.id))

class UserRepository(UserAbstractRepository):

    def __init__(self,connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, user: User):
        sql = "INSERT INTO users SET id = %s, personal_email = %s, phone_number = %s, user_type = %s, pin = %s, full_name = %s, wallet_id = %s, is_active = %s, is_phone_number_verified = %s, otp = %s, otp_generated_at = %s, location = %s, created_at)"

        self.cursor.execute(sql, (user.id, user.personal_email, user.phone_number, user.user_type, user.pin, user.full_name, user.wallet_id, user.is_active, user.is_phone_number_verified, user.otp, user.otp_generated_at, user.location, user.created_at))

        for key in user.closed_loops:
            sql = '''INSERT INTO user_closed_loops (user_id, closed_loop_id, unique_identifier, closed_loop_user_id,
            unique_identifier_otp, status, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            
            closed_loop_user = user.closed_loops[key]

            self.cursor.execute(sql, (user.id, key, closed_loop_user.unique_identifier, closed_loop_user.id, closed_loop_user.unique_identifier_otp, closed_loop_user.status, closed_loop_user.created_at))

    def get(self, user_id: str) -> User:
        sql = "SELECT id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, closed_loops, otp, otp_generated_at, location, created_at FROM users WHERE id = %s"

        self.cursor.execute(sql, (user_id,))

        row = self.cursor.fetchone()

        user = User(id=row[0], personal_email=row[1], phone_number=row[2], user_type=row[3], pin=row[4], full_name=row[5], wallet_id=row[6], is_active=row[7], is_phone_number_verified=row[8], closed_loops = {}, otp=row[9], otp_generated_at=row[10], location=row[11], created_at=row[12])
        
        sql = "SELECT user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at FROM user_closed_loops WHERE user_id = %s"

        self.cursor.execute(sql, (user_id,))

        rows = self.cursor.fetchall()

        for row in rows:
            closed_loop_user = ClosedLoopUser(closed_loop_id = row[1], unique_identifier = row[2], id = row[3], unique_identifier_otp = row[4], status = row[5], created_at = row[6])

            user.closed_loops[row[1]] = closed_loop_user

        return user

    def save(self, user: User):
        sql = '''INSERT into users SET personal_email = %s, phone_number = %s, user_type = %s, pin = %s, full_name = %s, wallet_id = %s, is_active = %s, is_phone_number_verified = %s, otp = %s, otp_generated_at = %s, location = %s WHERE id = %s on conflict(id) do update set
        personal_email = excluded.personal_email,
        phone_number = excluded.phone_number,
        user_type = excluded.user_type,
        pin = excluded.pin,
        full_name = excluded.full_name,
        wallet_id = excluded.wallet_id,
        is_active = excluded.is_active,
        is_phone_number_verified = excluded.is_phone_number_verified,
        otp = excluded.otp,
        otp_generated_at = excluded.otp_generated_at,
        location = excluded.location
        )'''

        self.cursor.execute(sql, (user.personal_email, user.phone_number, user.user_type, user.pin, user.full_name, user.wallet_id, user.is_active, user.is_phone_number_verified, user.otp, user.otp_generated_at, user.location, user.id))

        for key in user.closed_loops:
            sql = '''INSERT into user_closed_loops SET unique_identifier = %s, unique_identifier_otp = %s, status = %s WHERE user_id = %s AND closed_loop_id = %s
            on conflict(user_id, closed_loop_id) do update set
            unique_identifier = excluded.unique_identifier,
            unique_identifier_otp = excluded.unique_identifier_otp,
            status = excluded.status
            '''

            closed_loop_user = user.closed_loops[key]

            self.cursor.execute(sql, (closed_loop_user.unique_identifier, closed_loop_user.unique_identifier_otp, closed_loop_user.status, user.id, key))
    


