"""
1. Get all closed loops
2. Get closed loop from closed loop id

2. Get user from user id
4. Get user from email
3. Get user from phone number

6. Get all active users
7. Get all inactive users
8. Get all users of a user type
4. Get all closed loops of a user


2. Get all users of a closed loop
6. Get all unique identifiers of a closed loop (all roll numbers of LUMS)
user.closed_loops[closed_loop_id].unique_identifier


"""
from ..domain import model as authentication_model
# from ..adapters import repository as authentication_repository
from ...entrypoint.uow import AbstractUnitOfWork


def get_all_closed_loops(uow: AbstractUnitOfWork):
    """Get all closed loops"""
    with uow:
        sql = """
            select id, name, logo_url, description, regex, verification_type, created_at
            from closed_loops
            """
        uow.cursor.execute(sql)
        rows = uow.cursor.fetchall()
        closed_loops = [
            authentication_model.ClosedLoop(
                id=row[0],
                name=row[1],
                logo_url=row[2],
                description=row[3],
                regex=row[4],
                verification_type=row[5],
                created_at=row[6],
            )
            for row in rows
        ]

        return closed_loops


def get_closed_loop_from_closed_loop_id(closed_loop_id: str, uow: AbstractUnitOfWork):
    """Get closed loop from closed loop id"""
    with uow:
        closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop_id)
    return closed_loop


def get_user_from_user_id(user_id: str, uow: AbstractUnitOfWork):
    """Get user from user id"""
    with uow:
        user = uow.users.get(user_id=user_id)
    return user


def get_user_from_email(user_email: str, uow: AbstractUnitOfWork):
    """Get user from email"""
    with uow:
        sql = """
            select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at
            from users
            where personal_email = %s
        """
        uow.cursor.execute(
            sql,
            [
                user_email
            ]
        )
        row = uow.cursor.fetchone()
        user = authentication_model.User(
            id=row[0],
            personal_email=authentication_model.PersonalEmail(row[1]),
            phone_number=authentication_model.PhoneNumber(row[2]),
            user_type=authentication_model.UserType[row[3]],
            pin=row[4],
            full_name=row[5],
            wallet_id=row[6],
            is_active=row[7],
            is_phone_number_verified=row[8],
            otp=row[9],
            otp_generated_at=row[10],
            location=authentication_model.Location(latitude=float(
                row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
            created_at=row[12]
        )
        return user


def get_user_from_phone_number(phone_number: str, uow: AbstractUnitOfWork):
    """ Get user from phone number"""
    with uow:
        sql = """
            select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at
            from users
            where phone_number = %s
        """
        uow.cursor.execute(
            sql,
            [
                phone_number
            ]
        )
        row = uow.cursor.fetchone()
        user = authentication_model.User(
            id=row[0],
            personal_email=authentication_model.PersonalEmail(row[1]),
            phone_number=authentication_model.PhoneNumber(row[2]),
            user_type=authentication_model.UserType[row[3]],
            pin=row[4],
            full_name=row[5],
            wallet_id=row[6],
            is_active=row[7],
            is_phone_number_verified=row[8],
            otp=row[9],
            otp_generated_at=row[10],
            location=authentication_model.Location(latitude=float(
                row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
            created_at=row[12]
        )
        return user


def get_all_active_users(uow: AbstractUnitOfWork):
    """Get all active users"""
    with uow:
        sql = """
            select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at 
            from users 
            where is_active = true
        """
        uow.cursor.execute(sql)
        rows = uow.cursor.fetchall()
        users = [
            authentication_model.User(
                id=row[0],
                personal_email=authentication_model.PersonalEmail(row[1]),
                phone_number=authentication_model.PhoneNumber(row[2]),
                user_type=authentication_model.UserType[row[3]],
                pin=row[4],
                full_name=row[5],
                wallet_id=row[6],
                is_active=row[7],
                is_phone_number_verified=row[8],
                otp=row[9],
                otp_generated_at=row[10],
                location=authentication_model.Location(latitude=float(
                    row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
                created_at=row[12]
            )
            for row in rows
        ]
        return users


def get_all_inactive_users(uow: AbstractUnitOfWork):
    """Get all inactive users"""
    with uow:
        sql = """
            select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at 
            from users 
            where is_active = false
        """
        uow.cursor.execute(sql)
        rows = uow.cursor.fetchall()
        users = [
            authentication_model.User(
                id=row[0],
                personal_email=authentication_model.PersonalEmail(row[1]),
                phone_number=authentication_model.PhoneNumber(row[2]),
                user_type=authentication_model.UserType[row[3]],
                pin=row[4],
                full_name=row[5],
                wallet_id=row[6],
                is_active=row[7],
                is_phone_number_verified=row[8],
                otp=row[9],
                otp_generated_at=row[10],
                location=authentication_model.Location(latitude=float(
                    row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
                created_at=row[12]
            )
            for row in rows
        ]
        return users


def get_all_users_of_a_user_type(uow: AbstractUnitOfWork, user_type: authentication_model.UserType):
    """Get all users of a user type"""
    with uow:
        sql = """
            select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at 
            from users 
            where user_type = %s
        """
        uow.cursor.execute(
            sql,
            [
                user_type.name
            ]
        )
        rows = uow.cursor.fetchall()
        users = [
            authentication_model.User(
                id=row[0],
                personal_email=authentication_model.PersonalEmail(row[1]),
                phone_number=authentication_model.PhoneNumber(row[2]),
                user_type=authentication_model.UserType[row[3]],
                pin=row[4],
                full_name=row[5],
                wallet_id=row[6],
                is_active=row[7],
                is_phone_number_verified=row[8],
                otp=row[9],
                otp_generated_at=row[10],
                location=authentication_model.Location(latitude=float(
                    row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
                created_at=row[12]
            )
            for row in rows
        ]
        return users


def get_all_closed_loops_of_a_user(user_id: str, uow: AbstractUnitOfWork):
    """Get all closed loops of a user"""
    with uow:
        sql = """
            SELECT cl.id, cl.name, cl.logo_url, cl.description, cl.regex, cl.verification_type, cl.created_at
            FROM closed_loops cl
            JOIN user_closed_loops ucl ON cl.id = ucl.closed_loop_id
            WHERE ucl.user_id = %s
        """
        uow.cursor.execute(sql, [user_id])
        rows = uow.cursor.fetchall()

        closed_loops = [
            authentication_model.ClosedLoop(
                id=row[0],
                name=row[1],
                logo_url=row[2],
                description=row[3],
                regex=row[4],
                verification_type=row[5],
                created_at=row[6],
            )
            for row in rows
        ]

        return closed_loops

    # # with uow:
    # #     sql = """
    # #         select closed_loop_id
    # #         from user_closed_loops
    # #         where user_id = %s
    # #     """
    # #     uow.cursor.execute(
    # #         sql,
    # #         [
    # #             user_id
    # #         ]
    # #     )
    # #     rows = uow.cursor.fetchall()

    # #     sql = """
    # #         select id, name, logo_url, description, regex, verification_type, created_at
    # #         from closed_loops
    # #         where id IN (
    # #     """
    # #     ids_str = ",".join([f"'{row[0]}'" for row in rows])
    # #     sql += ids_str + ")"
    # #     uow.cursor.execute(sql)

    # #     rows = uow.cursor.fetchall()
    # #     closed_loops = [
    # #         authentication_model.ClosedLoop(
    # #             id=row[0],
    # #             name=row[1],
    # #             logo_url=row[2],
    # #             description=row[3],
    # #             regex=row[4],
    # #             verification_type=row[5],
    # #             created_at=row[6],
    # #         )
    # #         for row in rows
    # #     ]

    # #     return closed_loops


def get_all_users_of_a_closed_loop(closed_loop_id: str, uow: AbstractUnitOfWork):
    """Get all users of a closed loop"""
    with uow:
        sql = """
            select u.id, u.personal_email, u.phone_number, u.user_type, u.pin, u.full_name, u.wallet_id, u.is_active, u.is_phone_number_verified, u.otp, u.otp_generated_at, u.location, u.created_at
            from users u
            join user_closed_loops ucl on u.id = ucl.user_id
            where ucl.closed_loop_id = %s
        """
        uow.cursor.execute(
            sql,
            [
                closed_loop_id
            ]
        )
        rows = uow.cursor.fetchall()
        users = [
            authentication_model.User(
                id=row[0],
                personal_email=authentication_model.PersonalEmail(row[1]),
                phone_number=authentication_model.PhoneNumber(row[2]),
                user_type=authentication_model.UserType[row[3]],
                pin=row[4],
                full_name=row[5],
                wallet_id=row[6],
                is_active=row[7],
                is_phone_number_verified=row[8],
                otp=row[9],
                otp_generated_at=row[10],
                location=authentication_model.Location(latitude=float(
                    row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
                created_at=row[12]
            )
            for row in rows
        ]
        return users


def get_all_unique_identifier_of_a_closed_loop(closed_loop_id: str, uow: AbstractUnitOfWork):
    """Get all unique identifiers of a closed loop (all roll numbers of LUMS)"""
    with uow:
        sql = """
            select unique_identifier
            from user_closed_loops
            where closed_loop_id = %s
        """
        uow.cursor.execute(
            sql,
            [
                closed_loop_id
            ]
        )
        rows = uow.cursor.fetchall()
        unique_identifiers = [row[0] for row in rows]
        return unique_identifiers


# def get_closed_loop_from_id(closed_loop_id:str, uow:AbstractUnitOfWork):

#     with uow:
#         closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop_id)

#     return closed_loop

# def get_user_from_user_id(user_id:str, uow:AbstractUnitOfWork):

#         with uow:
#             user = uow.users.get(user_id=user_id)

#         return user

# def get_user_from_phone_number(phone_number: str, uow:AbstractUnitOfWork):
#     with uow:
#         sql = """
#         select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at
#         from users
#         where phone_number = %s
#         """

#         self.cursor.execute(
#             sql,
#             [
#                 phone_number
#             ]
#         )

#         row = self.cursor.fetchone()

#         user = User(
#             id=row[0],
#             personal_email=PersonalEmail(row[1]),
#             phone_number=PhoneNumber(row[2]),
#             user_type=UserType[row[3]],
#             pin=row[4],
#             full_name=row[5],
#             wallet_id=row[6],
#             is_active=row[7],
#             is_phone_number_verified=row[8],
#             otp=row[9],
#             otp_generated_at=row[10],
#             location=Location(latitude=float(row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
#             created_at=row[12]
#             )

#         sql = """
#         select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at
#         from user_closed_loops
#         where user_id = %s
#         """

#         self.cursor.execute(
#             sql,
#             [
#                 user.id
#             ]
#         )

#         rows = self.cursor.fetchall()

#         for row in rows:
#             closed_loop_user = ClosedLoopUser(
#                 closed_loop_id=row[1],
#                 unique_identifier=row[2],
#                 id=row[3],
#                 unique_identifier_otp=row[4],
#                 status=row[5],
#                 created_at=row[6]
#             )

#             user.closed_loops[row[1]] = closed_loop_user

#         return user

# def get_user_from_email(email: str, uow: AbstractUnitOfWork):
#     with uow:
#         sql = """
#         select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at
#         from users
#         where personal_email = %s
#         """

#         self.cursor.execute(
#             sql,
#             [
#                 email
#             ]
#         )

#         row = self.cursor.fetchone()

#         user = User(
#             id=row[0],
#             personal_email=PersonalEmail(row[1]),
#             phone_number=PhoneNumber(row[2]),
#             user_type=UserType[row[3]],
#             pin=row[4],
#             full_name=row[5],
#             wallet_id=row[6],
#             is_active=row[7],
#             is_phone_number_verified=row[8],
#             otp=row[9],
#             otp_generated_at=row[10],
#             location=Location(latitude=float(row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
#             created_at=row[12]
#             )

#         sql = """
#         select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at
#         from user_closed_loops
#         where user_id = %s
#         """

#         self.cursor.execute(
#             sql,
#             [
#                 user.id
#             ]
#         )

#         rows = self.cursor.fetchall()

#         for row in rows:
#             closed_loop_user = ClosedLoopUser(
#                 closed_loop_id=row[1],
#                 unique_identifier=row[2],
#                 id=row[3],
#                 unique_identifier_otp=row[4],
#                 status=row[5],
#                 created_at=row[6]
#             )

#             user.closed_loops[row[1]] = closed_loop_user

#         return user

# def get_user_from_wallet_id(wallet_id: str, uow: AbstractUnitOfWork):
#     with uow:
#         sql = """
#         select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at
#         from users
#         where wallet_id = %s
#         """

#         self.cursor.execute(
#             sql,
#             [
#                 wallet_id
#             ]
#         )

#         row = self.cursor.fetchone()

#         user = User(
#             id=row[0],
#             personal_email=PersonalEmail(row[1]),
#             phone_number=PhoneNumber(row[2]),
#             user_type=UserType[row[3]],
#             pin=row[4],
#             full_name=row[5],
#             wallet_id=row[6],
#             is_active=row[7],
#             is_phone_number_verified=row[8],
#             otp=row[9],
#             otp_generated_at=row[10],
#             location=Location(latitude=float(row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
#             created_at=row[12]
#             )

#         sql = """
#         select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at
#         from user_closed_loops
#         where user_id = %s
#         """

#         self.cursor.execute(
#             sql,
#             [
#                 user.id
#             ]
#         )

#         rows = self.cursor.fetchall()

#         for row in rows:
#             closed_loop_user = ClosedLoopUser(
#                 closed_loop_id=row[1],
#                 unique_identifier=row[2],
#                 id=row[3],
#                 unique_identifier_otp=row[4],
#                 status=row[5],
#                 created_at=row[6]
#             )

#             user.closed_loops[row[1]] = closed_loop_user

#         return user

# def get_all_active_or_inactive_users(status: bool,uow: AbstractUnitOfWork):
    # with uow:
    #     sql = """
    #     select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at
    #     from users
    #     where is_actve = %s
    #     """
    #     uow.cursor.execute(
    #         sql,
    #         [
    #             status
    #         ]
    #     )

    #     rows = uow.cursor.fetchall()
    #     users = []

    #     for row in rows:
    #         user = User(
    #             id=row[0],
    #             personal_email=PersonalEmail(row[1]),
    #             phone_number=PhoneNumber(row[2]),
    #             user_type=UserType[row[3]],
    #             pin=row[4],
    #             full_name=row[5],
    #             wallet_id=row[6],
    #             is_active=row[7],
    #             is_phone_number_verified=row[8],
    #             otp=row[9],
    #             otp_generated_at=row[10],
    #             location=Location(latitude=float(
    #                 row[11][1:-1].split(",")[0]), longitude=float(row[11][1:-1].split(",")[0])),
    #             created_at=row[12]
    #         )

    #         sql = """
    #         select user_id, closed_loop_id, unique_identifier, closed_loop_user_id, unique_identifier_otp, status, created_at
    #         from user_closed_loops
    #         where user_id = %s
    #         """

    #         uow.cursor.execute(
    #             sql,
    #             [
    #                 user.id
    #             ]
    #         )

    #         rows = uow.cursor.fetchall()

    #         for row in rows:
    #             closed_loop_user = ClosedLoopUser(
    #                 closed_loop_id=row[1],
    #                 unique_identifier=row[2],
    #                 id=row[3],
    #                 unique_identifier_otp=row[4],
    #                 status=row[5],
    #                 created_at=row[6]
    #             )

    #             user.closed_loops[row[1]] = closed_loop_user

    #         users.append(user)
