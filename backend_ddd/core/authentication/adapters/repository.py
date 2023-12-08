"""Repository interface for authentication module."""
from abc import ABC, abstractmethod
from typing import Dict

from core.authentication.adapters import exceptions as ex
from core.authentication.domain import model as mdl
from psycopg2.extras import DictCursor


class ClosedLoopAbstractRepository(ABC):
    """ClosedLoop Abstract Repository"""

    @abstractmethod
    def add(self, closed_loop: mdl.ClosedLoop):
        pass

    @abstractmethod
    def get(self, closed_loop_id: str) -> mdl.ClosedLoop:
        pass

    @abstractmethod
    def save(self, closed_loop: mdl.ClosedLoop):
        pass


class UserAbstractRepository(ABC):
    """User Abstract Repository"""

    @abstractmethod
    def add(self, user: mdl.User):
        pass

    @abstractmethod
    def get(self, user_id: str) -> mdl.User:
        pass

    @abstractmethod
    def save(self, user: mdl.User):
        pass


class FakeClosedLoopRepository(ClosedLoopAbstractRepository):
    """Fake Authentication Repository"""

    def __init__(self):
        self.closed_loops: Dict[str, mdl.ClosedLoop] = {}

    def add(self, closed_loop: mdl.ClosedLoop):
        self.closed_loops[closed_loop.id] = closed_loop

    def get(self, closed_loop_id: str) -> mdl.ClosedLoop:
        if closed_loop_id not in self.closed_loops:
            raise ex.ClosedLoopNotFound("CLosed loop not found")
        return self.closed_loops[closed_loop_id]

    def save(self, closed_loop: mdl.ClosedLoop):
        self.closed_loops[closed_loop.id] = closed_loop


class FakeUserRepository(UserAbstractRepository):
    """Fake Authentication Repository"""

    def __init__(self):
        self.users: Dict[str, mdl.User] = {}

    def add(self, user: mdl.User):
        self.users[user.id] = user

    def get(self, user_id: str) -> mdl.User:
        if user_id not in self.users:
            raise ex.UserNotFoundException("User not found")
        return self.users[user_id]

    def save(self, user: mdl.User):
        self.users[user.id] = user


class ClosedLoopRepository(ClosedLoopAbstractRepository):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor(cursor_factory=DictCursor)

    def add(self, closed_loop: mdl.ClosedLoop):
        sql = """
            insert into closed_loops (id, name, logo_url, description, regex, verification_type, created_at)
            values (%(id)s, %(name)s, %(logo_url)s, %(description)s, %(regex)s, %(verification_type)s, %(created_at)s)
        """

        self.cursor.execute(
            sql,
            {
                "id": closed_loop.id,
                "name": closed_loop.name,
                "logo_url": closed_loop.logo_url,
                "description": closed_loop.description,
                "regex": closed_loop.regex,
                "verification_type": closed_loop.verification_type.name,
                "created_at": closed_loop.created_at,
            },
        )

    def get(self, closed_loop_id: str) -> mdl.ClosedLoop:
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

        if row is None:
            raise ex.ClosedLoopNotFound("Closed loop not found")

        return mdl.ClosedLoop(
            id=row["id"],
            name=row["name"],
            logo_url=row["logo_url"],
            description=row["description"],
            regex=row["regex"],
            verification_type=mdl.ClosedLoopVerificationType[row["verification_type"]],
            created_at=row["created_at"],
        )

    def save(self, closed_loop: mdl.ClosedLoop):
        sql = """
            insert into closed_loops (id, name, logo_url, description, regex, verification_type, created_at)
            values (%(id)s, %(name)s, %(logo_url)s, %(description)s, %(regex)s, %(verification_type)s, %(created_at)s)
            on conflict(id) do update set 
                id = excluded.id,
                name = excluded.name,
                logo_url = excluded.logo_url,
                description = excluded.description,
                regex = excluded.regex,
                verification_type = excluded.verification_type
        """

        self.cursor.execute(
            sql,
            {
                "id": closed_loop.id,
                "name": closed_loop.name,
                "logo_url": closed_loop.logo_url,
                "description": closed_loop.description,
                "regex": closed_loop.regex,
                "verification_type": closed_loop.verification_type.name,
                "created_at": closed_loop.created_at,
            },
        )


class UserRepository(UserAbstractRepository):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor(cursor_factory=DictCursor)

    def add(self, user: mdl.User):
        sql = """
            insert into users (id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at, public_key, private_key) 
            values (%(id)s, %(personal_email)s, %(phone_number)s, %(user_type)s, %(pin)s, %(full_name)s, %(wallet_id)s, %(is_active)s, %(is_phone_number_verified)s, %(otp)s, %(otp_generated_at)s, %(location)s, %(created_at)s, %(public_key)s,  %(private_key)s)
        """

        self.cursor.execute(
            sql,
            {
                "id": user.id,
                "personal_email": user.personal_email.value,
                "phone_number": user.phone_number.value,
                "user_type": user.user_type.name,
                "pin": user.pin,
                "full_name": user.full_name,
                "wallet_id": user.wallet_id,
                "is_active": user.is_active,
                "is_phone_number_verified": user.is_phone_number_verified,
                "otp": user.otp,
                "otp_generated_at": user.otp_generated_at,
                "location": user.location,
                "created_at": user.created_at,
                "public_key": str(user.public_key),
                "private_key": str(user.private_key)
            },
        )

        if len(user.closed_loops) != 0:
            sql = """
            insert into user_closed_loops (user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at)
            values
            """

            args = [
                {
                    "user_id": user.id,
                    "closed_loop_id": key,
                    "unique_identifier": closed_loop_user.unique_identifier,
                    "closed_loop_user_id": closed_loop_user.id,
                    "unique_identifier_otp": closed_loop_user.unique_identifier_otp,
                    "status": closed_loop_user.status.name,
                    "created_at": closed_loop_user.created_at,
                }
                for key, closed_loop_user in user.closed_loops.items()
            ]

            args_str = ",".join(
                self.cursor.mogrify(
                    "(%(user_id)s,%(closed_loop_id)s,%(unique_identifier)s,%(closed_loop_user_id)s,%(unique_identifier_otp)s,%(status)s,%(created_at)s)",
                    x,
                ).decode("utf-8")
                for x in args
            )

            self.cursor.execute(sql + args_str)

    def get(self, user_id: str) -> mdl.User:
        sql = """
        select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at, public_key, private_key 
        from users 
        where id = %s
        """

        self.cursor.execute(sql, [user_id])

        row = self.cursor.fetchone()

        if row is None:
            raise ex.UserNotFoundException("User does not exist in db")

        user = mdl.User(
            id=row["id"],
            personal_email=mdl.PersonalEmail(row["personal_email"]),
            phone_number=mdl.PhoneNumber(row["phone_number"]),
            user_type=mdl.UserType[row["user_type"]],
            pin=row["pin"],
            full_name=row["full_name"],
            wallet_id=row["wallet_id"],
            is_active=row["is_active"],
            is_phone_number_verified=row["is_phone_number_verified"],
            otp=row["otp"],
            otp_generated_at=row["otp_generated_at"],
            location=mdl.Location(
                latitude=float(row["location"][1:-1].split(",")[0]),
                longitude=float(row["location"][1:-1].split(",")[1]),
            ),
            created_at=row["created_at"],
            public_key=row["public_key"],
            private_key=row["private_key"]
        )

        sql = """
        select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at 
        from user_closed_loops 
        where user_id = %s
        """

        self.cursor.execute(sql, [user_id])

        rows = self.cursor.fetchall()

        for row in rows:
            closed_loop_user = mdl.ClosedLoopUser(
                closed_loop_id=row["closed_loop_id"],
                unique_identifier=row["unique_identifier"],
                id=row["closed_loop_user_id"],
                unique_identifier_otp=row["unique_identifier_otp"],
                status=mdl.ClosedLoopUserState[row["status"]],
                created_at=row["created_at"],
            )

            user.closed_loops[row[1]] = closed_loop_user

        return user

    def save(self, user: mdl.User):
        sql = """
        insert into users (id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at, public_key, private_key)
        values(%(id)s, %(personal_email)s, %(phone_number)s, %(user_type)s, %(pin)s, %(full_name)s, %(wallet_id)s, %(is_active)s, %(is_phone_number_verified)s, %(otp)s, %(otp_generated_at)s, %(location)s, %(created_at)s, %(public_key)s, %(private_key)s)
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
            public_key = excluded.public_key,
            private_key = excluded.private_key
        """

        self.cursor.execute(
            sql,
            {
                "id": user.id,
                "personal_email": user.personal_email.value,
                "phone_number": user.phone_number.value,
                "user_type": user.user_type.name,
                "pin": user.pin,
                "full_name": user.full_name,
                "wallet_id": user.wallet_id,
                "is_active": user.is_active,
                "is_phone_number_verified": user.is_phone_number_verified,
                "otp": user.otp,
                "otp_generated_at": user.otp_generated_at,
                "location": user.location,
                "created_at": user.created_at,
                "public_key": user.public_key,
                "private_key": user.private_key
            },
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
                {
                    "user_id": user.id,
                    "closed_loop_id": key,  # closed_loop_id
                    "unique_identifier": closed_loop_user.unique_identifier,
                    "closed_loop_user_id": closed_loop_user.id,
                    "unique_identifier_otp": closed_loop_user.unique_identifier_otp,
                    "status": closed_loop_user.status.name,
                    "created_at": closed_loop_user.created_at,
                }
                for key, closed_loop_user in user.closed_loops.items()
            ]

            args_str = ",".join(
                self.cursor.mogrify(
                    "(%(user_id)s,%(closed_loop_id)s,%(unique_identifier)s,%(closed_loop_user_id)s,%(unique_identifier_otp)s,%(status)s,%(created_at)s)",
                    x,
                ).decode("utf-8")
                for x in args
            )

            self.cursor.execute(sql + args_str)
