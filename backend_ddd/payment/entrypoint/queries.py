from ..domain.model import Wallet
from ...entrypoint.uow import AbstractUnitOfWork

def get_wallet_from_wallet_id(wallet_id:str, uow:AbstractUnitOfWork):
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