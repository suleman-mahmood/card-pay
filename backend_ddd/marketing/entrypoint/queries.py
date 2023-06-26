from ...authentication.domain.model import User
from ...entrypoint.uow import AbstractUnitOfWork

def get_user_id_from_wallet_id(
    wallet_id: str, 
    uow: AbstractUnitOfWork
)->str:

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
