# from ..domain.model import Wallet
from ..domain import model as payment_model
from ...entrypoint.uow import AbstractUnitOfWork

def usecases():
    """
    1. get wallet balance from wallet_id    || later update to get balance from user_id
    2. get user id from wallet id           || will be removed once refactores
    3. get wallet from wallet id            ||  will be updated to get wallet from user id
    4. add starred wallet id                || will be updated to add starred user id
    5. get starred wallet id                || will be updated to get starred user id

    following transactions will be sorted by time with recent coming first
    5. get transaction by transaction id
    6. get all transactions sorted 
    7. get all transactions of passed type sorted 

    8. get all transactions of a user sorted 
    9. get all transactions of a user of passed type sorted

    10. get all cash inflow transactions of a user sorted 
    11. get all cash outflow transactions of a user sorted 
    12. get all transactions betweeen two specified users sorted 
    13. get all transaction from specifies sender to receiver sorted 
    """


def get_wallet_balance(
    wallet_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        sql = """
            select balance
            from wallets
            where id = %s
            """
        uow.cursor.execute(
            sql,
            [
                wallet_id
            ]
        )
        row = uow.cursor.fetchone()
        return row[0]


def get_wallet_from_wallet_id(wallet_id: str, uow: AbstractUnitOfWork):

    with uow:
        sql = """
            select id, balance
            from wallets
            where id = %s
        """
        uow.cursor.execute(
            sql,
            [
                wallet_id
            ]
        )
        row = uow.cursor.fetchone()
        return payment_model.Wallet(
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
    with uow:
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


def get_transaction_by_transaction_id(
    transaction_id: str,
    uow: AbstractUnitOfWork
):
    with uow:
        transaction = uow.transactions.get(transaction_id)
        return transaction


def _helper_generate_list_of_transactions(rows):
    """ helper function to create multiple transaction objects"""
    transactions = [
        payment_model.Transaction(
            id=row[0],
            amount=row[1],
            mode=payment_model.TransactionMode[row[2]],
            transaction_type=payment_model.TransactionType[row[3]],
            status=payment_model.TransactionStatus[row[4]],
            sender_wallet=payment_model.Wallet(
                id=row[5], balance=row[10]
            ),
            recipient_wallet=payment_model.Wallet(
                id=row[6], balance=row[12]
            ),
            created_at=row[7],
            last_updated=row[8]
        )
        for row in rows
    ]

    return transactions


def get_all_transactions(uow: AbstractUnitOfWork):
    """ Get all transactions sorted by time with recent coming first"""
    with uow:
        sql = """
            select t.id, t.amount, t.mode, t.transaction_type, t.status, t.sender_wallet_id, t.recipient_wallet_id, t.created_at, t.last_updated,
            s.id AS sender_wallet_id, s.balance AS sender_balance, r.id AS recipient_wallet_id, r.balance AS recipient_balance
            from transactions t
            inner join wallets s on t.sender_wallet_id = s.id
            inner join wallets r on t.recipient_wallet_id = r.id
            order by created_at desc
        """

        uow.cursor.execute(
            sql
        )

        transactions = _helper_generate_list_of_transactions(
            uow.cursor.fetchall())

        return transactions


def get_all_transactions_of_a_type(transaction_type: payment_model.TransactionType, uow: AbstractUnitOfWork):
    with uow:
        sql = """
            select t.id, t.amount, t.mode, t.transaction_type, t.status, t.sender_wallet_id, t.recipient_wallet_id, t.created_at, t.last_updated,
            s.id AS sender_wallet_id, s.balance AS sender_balance, r.id AS recipient_wallet_id, r.balance AS recipient_balance
            from transactions t
            inner join wallets s on t.sender_wallet_id = s.id
            inner join wallets r on t.recipient_wallet_id = r.id
            where t.transaction_type = %s
            order by created_at desc
        """

        uow.cursor.execute(
            sql,
            [
                transaction_type.name
            ]
        )
        rows = uow.cursor.fetchall()
        transactions = _helper_generate_list_of_transactions(rows)

        return transactions


def get_all_transactions_of_a_user(user_id: str, uow: AbstractUnitOfWork):
    with uow:
        sql = """
            select t.id, t.amount, t.mode, t.transaction_type, t.status, t.sender_wallet_id, t.recipient_wallet_id, t.created_at, t.last_updated,
            s.id AS sender_wallet_id, s.balance AS sender_balance, r.id AS recipient_wallet_id, r.balance AS recipient_balance
            from transactions t
            inner join wallets s on t.sender_wallet_id = s.id
            inner join wallets r on t.recipient_wallet_id = r.id
            where sender_wallet_id = %s or recipient_wallet_id = %s
            order by created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                user_id,
                user_id
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions(rows)
        return transactions


def get_all_transactions_of_a_user_of_a_type(user_id: str, transaction_type: payment_model.TransactionType, uow: AbstractUnitOfWork):
    with uow:
        sql = """
            select t.id, t.amount, t.mode, t.transaction_type, t.status, t.sender_wallet_id, t.recipient_wallet_id, t.created_at, t.last_updated,
            s.id AS sender_wallet_id, s.balance AS sender_balance, r.id AS recipient_wallet_id, r.balance AS recipient_balance
            from transactions t
            inner join wallets s on t.sender_wallet_id = s.id
            inner join wallets r on t.recipient_wallet_id = r.id
            where (sender_wallet_id = %s or recipient_wallet_id = %s) and t.transaction_type = %s
            order by created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                user_id,
                user_id,
                transaction_type.name
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions(rows)
        return transactions


def get_all_cash_inflow_transactions_of_a_user(user_id: str, uow: AbstractUnitOfWork):
    with uow:
        sql = """
            select t.id, t.amount, t.mode, t.transaction_type, t.status, t.sender_wallet_id, t.recipient_wallet_id, t.created_at, t.last_updated,
            s.id AS sender_wallet_id, s.balance AS sender_balance, r.id AS recipient_wallet_id, r.balance AS recipient_balance
            from transactions t
            inner join wallets s on t.sender_wallet_id = s.id
            inner join wallets r on t.recipient_wallet_id = r.id
            where recipient_wallet_id = %s
            order by created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                user_id
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions(rows)

        return transactions


def get_all_cash_outflow_transactions_of_a_user(user_id: str, uow: AbstractUnitOfWork):
    with uow:
        sql = """
            select t.id, t.amount, t.mode, t.transaction_type, t.status, t.sender_wallet_id, t.recipient_wallet_id, t.created_at, t.last_updated,
            s.id AS sender_wallet_id, s.balance AS sender_balance, r.id AS recipient_wallet_id, r.balance AS recipient_balance
            from transactions t
            inner join wallets s on t.sender_wallet_id = s.id
            inner join wallets r on t.recipient_wallet_id = r.id
            where sender_wallet_id = %s
            order by created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                user_id
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions(rows)

        return transactions


def get_all_transactions_between_two_users(user1_id: str, user2_id: str, uow: AbstractUnitOfWork):
    with uow:
        sql = """
            select t.id, t.amount, t.mode, t.transaction_type, t.status, t.sender_wallet_id, t.recipient_wallet_id, t.created_at, t.last_updated,
            s.id AS sender_wallet_id, s.balance AS sender_balance, r.id AS recipient_wallet_id, r.balance AS recipient_balance
            from transactions t
            inner join wallets s on t.sender_wallet_id = s.id
            inner join wallets r on t.recipient_wallet_id = r.id
            where (sender_wallet_id = %s and recipient_wallet_id = %s) or (sender_wallet_id = %s and recipient_wallet_id = %s)
            order by created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                user1_id,
                user2_id,
                user2_id,
                user1_id
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions(rows)

        return transactions

def get_all_transactions_from_sender_to_receiver(sender_id: str, receiver_id: str, uow: AbstractUnitOfWork):
    with uow:
        sql = """
            select t.id, t.amount, t.mode, t.transaction_type, t.status, t.sender_wallet_id, t.recipient_wallet_id, t.created_at, t.last_updated,
            s.id AS sender_wallet_id, s.balance AS sender_balance, r.id AS recipient_wallet_id, r.balance AS recipient_balance
            from transactions t
            inner join wallets s on t.sender_wallet_id = s.id
            inner join wallets r on t.recipient_wallet_id = r.id
            where sender_wallet_id = %s and recipient_wallet_id = %s
            order by created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                sender_id,
                receiver_id
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions(rows)

        return transactions
