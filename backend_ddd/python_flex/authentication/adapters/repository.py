"""Repository interface for authentication module."""
from abc import ABC, abstractmethod
from typing import Dict
from ..domain.model import (
    ClosedLoop,
    User,
    ClosedLoopUser,
    UserType,
    ClosedLoopVerificationType,
    PersonalEmail,
    PhoneNumber,
    Location,
    ClosedLoopUserState,
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
        sql = """
            insert into closed_loops (id, name, logo_url, description, regex,verification_type, created_at)
            values (%s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.execute(
            sql,
            [
                closed_loop.id,
                closed_loop.name,
                closed_loop.logo_url,
                closed_loop.description,
                closed_loop.regex,
                closed_loop.verification_type.name,
                closed_loop.created_at,
            ],
        )

    def get(self, closed_loop_id: str) -> ClosedLoop:
        sql = """
        select id, name, logo_url, description, regex, verification_type, created_at
        from closed_loops
        where id = %s
        """

        self.cursor.execute(
            sql,
            [
                closed_loop_id,
            ],
        )

        row = self.cursor.fetchone()
        return ClosedLoop(
            id=row[0],
            name=row[1],
            logo_url=row[2],
            description=row[3],
            regex=row[4],
            verification_type=ClosedLoopVerificationType[row[5]],
            created_at=row[6],
        )

    def save(self, closed_loop: ClosedLoop):
        sql = """
            insert into closed_loops (id, name, logo_url, description, regex, verification_type, created_at)
            values (%s, %s, %s, %s, %s, %s, %s)
            on conflict(id) do update set 
                id = excluded.id,
                name = excluded.name,
                logo_url = excluded.logo_url,
                description = excluded.description,
                regex = excluded.regex,
                verification_type = excluded.verification_type,
                created_at = excluded.created_at
        """

        self.cursor.execute(
            sql,
            [
                closed_loop.id,
                closed_loop.name,
                closed_loop.logo_url,
                closed_loop.description,
                closed_loop.regex,
                closed_loop.verification_type.name,
                closed_loop.created_at,
            ],
        )


class UserRepository(UserAbstractRepository):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, user: User):
        sql = """
            insert into users (id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.cursor.execute(
            sql,
            [
                user.id,
                user.personal_email.value,
                user.phone_number.value,
                user.user_type.name,
                user.pin,
                user.full_name,
                user.wallet_id,
                user.is_active,
                user.is_phone_number_verified,
                user.otp,
                user.otp_generated_at,
                user.location,
                user.created_at,
            ],
        )

        if len(user.closed_loops) != 0:
            sql = """
            insert into user_closed_loops (user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at)
            values
            """

            args = [
                (
                    user.id,
                    key,  # closed_loop_id
                    closed_loop_user.unique_identifier,
                    closed_loop_user.id,
                    closed_loop_user.unique_identifier_otp,
                    closed_loop_user.status.name,
                    closed_loop_user.created_at,
                )
                for key, closed_loop_user in user.closed_loops.items()
            ]

            args_str = ",".join(
                self.cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x).decode("utf-8")
                for x in args
            )

            self.cursor.execute(sql + args_str)

    def get(self, user_id: str) -> User:
        sql = """
        select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at 
        from users 
        where id = %s
        """

        self.cursor.execute(sql, [user_id])

        row = self.cursor.fetchone()

        user = User(
            id=row[0],
            personal_email=PersonalEmail(row[1]),
            phone_number=PhoneNumber(row[2]),
            user_type=UserType[row[3]],
            pin=row[4],
            full_name=row[5],
            wallet_id=row[6],
            is_active=row[7],
            is_phone_number_verified=row[8],
            otp=row[9],
            otp_generated_at=row[10],
            location=Location(
                latitude=float(row[11][1:-1].split(",")[0]),
                longitude=float(row[11][1:-1].split(",")[0]),
            ),
            created_at=row[12],
        )

        sql = """
        select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at 
        from user_closed_loops 
        where user_id = %s
        """

        self.cursor.execute(sql, [user_id])

        rows = self.cursor.fetchall()

        for row in rows:
            closed_loop_user = ClosedLoopUser(
                closed_loop_id=row[1],
                unique_identifier=row[2],
                id=row[3],
                unique_identifier_otp=row[4],
                status=ClosedLoopUserState[row[5]],
                created_at=row[6],
            )

            user.closed_loops[row[1]] = closed_loop_user

        return user

    def save(self, user: User):
        sql = """
        insert into users (id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at)
        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        on conflict(id) do update set
            id = excluded.id,
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
            location = excluded.location,
            created_at = excluded.created_at
        """

        self.cursor.execute(
            sql,
            [
                user.id,
                user.personal_email.value,
                user.phone_number.value,
                user.user_type.name,
                user.pin,
                user.full_name,
                user.wallet_id,
                user.is_active,
                user.is_phone_number_verified,
                user.otp,
                user.otp_generated_at,
                user.location,
                user.created_at,
            ],
        )

        sql = """
            delete from user_closed_loops 
            where user_id = %s
        """

        self.cursor.execute(sql, [user.id])

        if len(user.closed_loops) != 0:
            sql = """
            insert into user_closed_loops (user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at)
            values
            """

            args = [
                (
                    user.id,
                    key,  # closed_loop_id
                    closed_loop_user.unique_identifier,
                    closed_loop_user.id,
                    closed_loop_user.unique_identifier_otp,
                    closed_loop_user.status.name,
                    closed_loop_user.created_at,
                )
                for key, closed_loop_user in user.closed_loops.items()
            ]

            args_str = ",".join(
                self.cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x).decode("utf-8")
                for x in args
            )

            self.cursor.execute(sql + args_str)