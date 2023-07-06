from ..domain.model import Wallet
from ...entrypoint.uow import AbstractUnitOfWork
from ...authentication.domain.model import User


def get_wallet_from_wallet_id(wallet_id: str, uow: AbstractUnitOfWork):
    sql = """
        select id, balance
        from wallets 
        where id = %s
        for update
    """
    uow.cursor.execute(
        sql,
        [
            wallet_id
        ]
    )
    row = uow.cursor.fetchone()
    return Wallet(
        id=row[0],
        balance=row[1],
    )


def get_user_id_from_wallet_id(
    wallet_id: str,
    uow: AbstractUnitOfWork
) -> str:

    sql = """
        select id
        from users
        where wallet_id = %s
    """
    uow.cursor.execute(
        sql,
        [
            wallet_id
        ]
    )
    row = uow.cursor.fetchone()
    return row[0]


def add_starred_wallet_id(
    wallet_id: str,
    uow: AbstractUnitOfWork
):
    """
    keeping it here for now, will move it later after discussion
    """
    delete_sql = """
        delete from starred_wallet_id
    """
    uow.cursor.execute(
        delete_sql
    )

    sql = """
        insert into starred_wallet_id
        values (%s)
    """
    uow.cursor.execute(
        sql,
        [
            wallet_id
        ]
    )
    uow.connection.commit()


def get_starred_wallet_id(
    uow: AbstractUnitOfWork
):
    """
    keeping it here for now, will move it later after discussion
    """
    sql = """
        select wallet_id
        from starred_wallet_id
    """
    uow.cursor.execute(
        sql
    )
    rows = uow.cursor.fetchall()
    return rows[0]
