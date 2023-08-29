"""
1. Get all closed loops
2. Get closed loop from closed loop id

3. Get user from user id
4. Get user from email
5. Get user from phone number
6. Get user from closed_loop_id and unique_identifier

7. Get all active users
8. Get all inactive users
9. Get all users of a user type
10. Get all closed loops of a user

11. Get all users of a closed loop
12. Get all unique identifiers of a closed loop (ie all roll numbers of LUMS)


13. update closed loop
14. get information of all users of a closed loop
"""
from core.authentication.entrypoint import exceptions as ex
from ..domain import model as authentication_model

# from ..adapters import repository as authentication_repository
from ...entrypoint.uow import AbstractUnitOfWork


def get_all_closed_loops(uow: AbstractUnitOfWork):
    """Get all closed loops"""

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


def get_all_closed_loops_with_user_counts(uow: AbstractUnitOfWork):
    sql = """
        select cl.id, cl.name, cl.logo_url, cl.description, cl.regex, cl.verification_type, cl.created_at, count(ucl.user_id)
        from closed_loops cl
        left join user_closed_loops ucl on cl.id = ucl.closed_loop_id
        group by cl.id, cl.name, cl.logo_url, cl.description, cl.regex, cl.verification_type, cl.created_at
    """
    uow.cursor.execute(sql)
    rows = uow.cursor.fetchall()
    closed_loops = [
        {
            "id": row[0],
            "name": row[1],
            "logo_url": row[2],
            "description": row[3],
            "regex": row[4],
            "verification_type": row[5],
            "created_at": row[6],
            "user_count": row[7],
        }
        for row in rows
    ]

    return closed_loops


def get_closed_loop_from_closed_loop_id(closed_loop_id: str, uow: AbstractUnitOfWork):
    """Get closed loop from closed loop id"""

    closed_loop = uow.closed_loops.get(closed_loop_id=closed_loop_id)

    return closed_loop


def get_user_from_user_id(user_id: str, uow: AbstractUnitOfWork):
    """Get user from user id"""
    user = uow.users.get(user_id=user_id)
    return user


def get_user_type_from_user_id(user_id: str, uow: AbstractUnitOfWork):
    """Get user type from user id"""
    sql = """
        select user_type
        from users
        where id = %s
    """
    uow.cursor.execute(sql, [user_id])
    row = uow.cursor.fetchone()
    user_type = authentication_model.UserType[row[0]]
    return user_type


def get_user_from_email(user_email: str, uow: AbstractUnitOfWork):
    """Get user from email"""

    sql = """
        select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at
        from users
        where personal_email = %s
    """
    uow.cursor.execute(sql, [user_email])
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
        location=authentication_model.Location(
            latitude=float(row[11][1:-1].split(",")[0]),
            longitude=float(row[11][1:-1].split(",")[0]),
        ),
        created_at=row[12],
    )
    return user


def get_user_from_phone_number(phone_number: str, uow: AbstractUnitOfWork):
    """Get user from phone number"""

    sql = """
        select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at
        from users
        where phone_number = %s
    """
    uow.cursor.execute(sql, [phone_number])
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
        location=authentication_model.Location(
            latitude=float(row[11][1:-1].split(",")[0]),
            longitude=float(row[11][1:-1].split(",")[0]),
        ),
        created_at=row[12],
    )
    return user


def get_user_from_closed_loop_id_and_unique_identifier(
    closed_loop_id: str, unique_identifier: str, uow: AbstractUnitOfWork
):
    """Get user from closed_loop_id and unique_identifier"""

    sql = """
        select u.id, u.personal_email, u.phone_number, u.user_type, u.pin, u.full_name, u.wallet_id, u.is_active, u.is_phone_number_verified, u.otp, u.otp_generated_at, u.location, u.created_at
        from users u
        join user_closed_loops ucl on u.id = ucl.user_id
        where ucl.closed_loop_id = %s and ucl.unique_identifier = %s
        """
    uow.cursor.execute(sql, [closed_loop_id, unique_identifier])
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
        location=authentication_model.Location(
            latitude=float(row[11][1:-1].split(",")[0]),
            longitude=float(row[11][1:-1].split(",")[0]),
        ),
        created_at=row[12],
    )

    return user


def get_all_active_users(uow: AbstractUnitOfWork):
    """Get all active users"""

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
            location=authentication_model.Location(
                latitude=float(row[11][1:-1].split(",")[0]),
                longitude=float(row[11][1:-1].split(",")[0]),
            ),
            created_at=row[12],
        )
        for row in rows
    ]
    return users


def get_all_inactive_users(uow: AbstractUnitOfWork):
    """Get all inactive users"""

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
            location=authentication_model.Location(
                latitude=float(row[11][1:-1].split(",")[0]),
                longitude=float(row[11][1:-1].split(",")[0]),
            ),
            created_at=row[12],
        )
        for row in rows
    ]

    return users


def get_all_users_of_a_user_type(
    uow: AbstractUnitOfWork, user_type: authentication_model.UserType
):
    """Get all users of a user type"""

    sql = """
        select id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at 
        from users 
        where user_type = %s
    """
    uow.cursor.execute(sql, [user_type.name])
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
            location=authentication_model.Location(
                latitude=float(row[11][1:-1].split(",")[0]),
                longitude=float(row[11][1:-1].split(",")[0]),
            ),
            created_at=row[12],
        )
        for row in rows
    ]
    return users


def get_all_closed_loops_of_a_user(user_id: str, uow: AbstractUnitOfWork):
    """Get all closed loops of a user"""

    sql = """
        select cl.id, cl.name, cl.logo_url, cl.description, cl.regex, cl.verification_type, cl.created_at
        from closed_loops cl
        join user_closed_loops ucl ON cl.id = ucl.closed_loop_id
        where ucl.user_id = %s
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

    sql = """
        select u.id, u.personal_email, u.phone_number, u.user_type, u.pin, u.full_name, u.wallet_id, u.is_active, u.is_phone_number_verified, u.otp, u.otp_generated_at, u.location, u.created_at
        from users u
        join user_closed_loops ucl on u.id = ucl.user_id
        where ucl.closed_loop_id = %s
    """
    uow.cursor.execute(sql, [closed_loop_id])
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
            location=authentication_model.Location(
                latitude=float(row[11][1:-1].split(",")[0]),
                longitude=float(row[11][1:-1].split(",")[0]),
            ),
            created_at=row[12],
        )
        for row in rows
    ]
    return users


def get_all_unique_identifier_of_a_closed_loop(
    closed_loop_id: str, uow: AbstractUnitOfWork
):
    """Get all unique identifiers of a closed loop (all roll numbers of LUMS)"""

    sql = """
        select unique_identifier
        from user_closed_loops
        where closed_loop_id = %s
    """
    uow.cursor.execute(sql, [closed_loop_id])
    rows = uow.cursor.fetchall()
    unique_identifiers = [row[0] for row in rows]
    return unique_identifiers


def get_user_balance(user_id: str, uow: AbstractUnitOfWork):
    """Get user from user id"""
    # TODO: fix this to user user id as wallet id
    sql = """
        select balance
        from wallets
        where id = (
            select wallet_id
            from users
            where id = %s
        )        
    """
    uow.cursor.execute(sql, [user_id])
    row = uow.cursor.fetchone()
    balance = row[0]

    return balance


def get_user_count_of_all_closed_loops(uow: AbstractUnitOfWork):
    sql = """
        select cl.id, cl.name, count(ucl.user_id)
        from closed_loops cl
        join user_closed_loops ucl on cl.id = ucl.closed_loop_id
        group by cl.id, cl.name
    """
    uow.cursor.execute(sql)
    rows = uow.cursor.fetchall()
    closed_loops_user_count = [
        {
            "id": row[0],
            "name": row[1],
            "user_count": row[2],
        }
        for row in rows
    ]
    return closed_loops_user_count


def get_information_of_all_users_of_a_closed_loop(
    closed_loop_id: str, uow: AbstractUnitOfWork
):
    """Get information of all users of a closed loop"""
    sql = """
        select
        u.id, u.personal_email, u.phone_number, u.user_type, u.full_name, u.wallet_id, u.is_active, u.is_phone_number_verified, u.location, u.loyalty_points, u.referral_id, u.created_at,
        ucl.unique_identifier, ucl.closed_loop_user_id, ucl.created_at 
        from users u
        join user_closed_loops ucl on u.id = ucl.user_id
        where ucl.closed_loop_id = %s
    """
    uow.cursor.execute(sql, [closed_loop_id])

    rows = uow.cursor.fetchall()
    users = [
        {
            "id": row[0],
            "personal_email": row[1],
            "phone_number": row[2],
            "user_type": row[3],
            "full_name": row[4],
            "wallet_id": row[5],
            "is_active": row[6],
            "is_phone_number_verified": row[7],
            "location": row[8],
            "loyalty_points": row[9],
            "referral_id": row[10],
            "card_pay_joining_date": row[11],
            "closed_loop_unique_identifier": row[12],
            "closed_loop_user_id": row[13],
            "closed_loop_joining_date": row[14],
        }
        for row in rows
    ]
    return users


def get_active_inactive_counts_of_a_closed_loop(
    closed_loop_id: str, uow: AbstractUnitOfWork
):
    """Get active inactive counts of a closed loop"""

    active_sql = """
        select
        count(u.id)
        from users u
        join user_closed_loops ucl on u.id = ucl.user_id
        where ucl.closed_loop_id = %s and u.is_active = true
    """
    uow.cursor.execute(active_sql, [closed_loop_id])
    active_count = uow.cursor.fetchone()[0]

    inactive_sql = """
        select
        count(u.id)
        from users u
        join user_closed_loops ucl on u.id = ucl.user_id
        where ucl.closed_loop_id = %s and u.is_active = false
    """
    uow.cursor.execute(inactive_sql, [closed_loop_id])
    inactive_count = uow.cursor.fetchone()[0]

    return [
        {
            "label": "active",
            "count": active_count,
        },
        {
            "label": "inactive",
            "count": inactive_count,
        },
    ]


def get_unique_identifier_from_user_id(user_id: str, uow: AbstractUnitOfWork) -> str:
    sql = """
        select unique_identifier
        from user_closed_loops
        where user_id = %s
    """
    uow.cursor.execute(sql, [user_id])
    row = uow.cursor.fetchone()

    return row[0]


def user_id_from_firestore(unique_identifier: str, uow: AbstractUnitOfWork) -> str:
    sql = """
        select
            id
        from 
            users_firestore
        where 
            personal_email ilike %s
            and not migrated
    """
    uow.cursor.execute(sql, ["%" + unique_identifier + "%"])
    row = uow.cursor.fetchone()

    if row is None:
        raise ex.UserNotInFirestore("User not found")

    return row[0]


def wallet_balance_from_firestore(user_id: str, uow: AbstractUnitOfWork) -> int:
    sql = """
        select
            balance
        from 
            wallets_firestore
        where 
            id = %s
            and not migrated
    """
    uow.cursor.execute(sql, [user_id])
    row = uow.cursor.fetchone()

    if row is None:
        raise ex.WalletNotInFirestore("Wallet not found")

    return row[0]


def _get_latest_closed_loop_id(uow: AbstractUnitOfWork) -> str:
    sql = """
        select
            id
        from 
            closed_loops
        order by created_at desc
        limit 1
    """
    uow.cursor.execute(sql)
    row = uow.cursor.fetchone()

    return row[0]


def user_verification_status_from_user_id(
    user_id: str, uow: AbstractUnitOfWork
) -> bool:
    sql = """
        select
            is_phone_number_verified
        from 
            users
        where 
            id = %s
    """
    uow.cursor.execute(sql, [user_id])
    row = uow.cursor.fetchone()

    return row[0] if row else False


def unique_identifier_already_exists(
    closed_loop_id: str, unique_identifier: str, uow: AbstractUnitOfWork
) -> bool:
    sql = """
        select unique_identifier
        from user_closed_loops
        where closed_loop_id = %s and unique_identifier = %s
    """
    uow.cursor.execute(sql, [closed_loop_id, unique_identifier])
    result = uow.cursor.fetchone()
    return result is not None

def get_unique_identifier_from_user_id_and_closed_loop_id(
    user_id: str, closed_loop_id: str, uow: AbstractUnitOfWork
) -> str:
    sql = """
        select unique_identifier
        from user_closed_loops
        where user_id = %s and closed_loop_id = %s
    """
    uow.cursor.execute(sql, [user_id, closed_loop_id])
    result = uow.cursor.fetchone()
    return result[0]
