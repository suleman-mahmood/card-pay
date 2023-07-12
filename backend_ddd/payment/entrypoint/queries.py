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
    6. get all transactions 
    7. get all transactions of passed type 

    8. get all transactions of a user 
    9. get all transactions of a user of passed type

    10. get all cash inflow transactions of a user 
    11. get all cash outflow transactions of a user 
    12. get all transactions betweeen two specified users 
    13. get all transaction from specifies sender to receiver 
    14. get all beneficiaries of a user
    15. get all benefactors of a user
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


def _helper_generate_list_of_transactions_for_admin(rows):
    """ for admin get functions | helper function to create multiple transaction objects"""
    transactions = [
        {
            "id": row[0],
            "amount": row[1],
            "mode": row[2],
            "transaction_type": row[3],
            "status": row[4],
            "created_at": row[5],
            "last_updated": row[6],
            "sender_id": row[7],
            "sender_name": row[8],
            "recipient_id": row[9],
            "recipient_name": row[10]
        }
        for row in rows
    ]

    return transactions


def _helper_generate_list_of_transactions_for_general_case(rows):
    " for general get functions | helper function to create multiple transaction objects"
    transactions = [
        {
            "id": row[0],
            "amount": row[1],
            "mode": row[2],
            "transaction_type": row[3],
            "status": row[4],
            "created_at": row[5],
            "last_updated": row[6],
            "sender_name": row[7],
            "recipient_name": row[8]
        }
        for row in rows
    ]

    return transactions


def get_all_transactions(uow: AbstractUnitOfWork):
    """ admin function | Get all transactions"""
    with uow:

        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.id AS sender_id, sender.full_name AS sender_name,
            recipient.id AS recipient_id, recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            order by txn.created_at desc
        """

        uow.cursor.execute(
            sql
        )

        rows = uow.cursor.fetchall()
        transactions = _helper_generate_list_of_transactions_for_admin(
            rows)

        return transactions


def get_all_transactions_of_a_type(transaction_type: payment_model.TransactionType, uow: AbstractUnitOfWork):
    """ admin function | Get all transactions of a type"""

    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.id AS sender_id, sender.full_name AS sender_name,
            recipient.id AS recipient_id, recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where txn.transaction_type = %s
            order by txn.created_at desc
        """

        uow.cursor.execute(
            sql,
            [
                transaction_type.name
            ]
        )
        rows = uow.cursor.fetchall()
        transactions = _helper_generate_list_of_transactions_for_admin(rows)

        return transactions


def get_all_transactions_of_a_user(user_id: str, uow: AbstractUnitOfWork):
    """ generel fuction | Get all transactions of a user"""
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.full_name AS sender_name,
            recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where txn.sender_wallet_id = %s or txn.recipient_wallet_id = %s
            order by txn.created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                user_id,
                user_id
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(
            rows)
        return transactions


def get_all_transactions_of_a_user_of_a_type(user_id: str, transaction_type: payment_model.TransactionType, uow: AbstractUnitOfWork):
    """ generel fuction | Get all transactions of a user of a type"""
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.full_name AS sender_name,
            recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where (txn.sender_wallet_id = %s or txn.recipient_wallet_id = %s) and txn.transaction_type = %s
            order by txn.created_at desc
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

        transactions = _helper_generate_list_of_transactions_for_general_case(
            rows)
        return transactions


def get_all_cash_inflow_transactions_of_a_user(user_id: str, uow: AbstractUnitOfWork):
    """ generel fuction | Get all cash inflow transactions of a user"""
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.full_name AS sender_name,
            recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where txn.recipient_wallet_id = %s
            order by txn.created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                user_id
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(
            rows)

        return transactions


def get_all_cash_outflow_transactions_of_a_user(user_id: str, uow: AbstractUnitOfWork):
    """ generel fuction | Get all cash outflow transactions of a user"""
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.full_name AS sender_name,
            recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where txn.sender_wallet_id = %s
            order by txn.created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                user_id
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(
            rows)

        return transactions


def get_all_transactions_between_two_users(user1_id: str, user2_id: str, uow: AbstractUnitOfWork):
    """ admin fuction | Get all transactions between two users"""
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.id AS sender_id, sender.full_name AS sender_name,
            recipient.id AS recipient_id, recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where (txn.sender_wallet_id = %s and txn.recipient_wallet_id = %s) or (txn.sender_wallet_id = %s and txn.recipient_wallet_id = %s)
            order by txn.created_at desc
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

        transactions = _helper_generate_list_of_transactions_for_admin(rows)

        return transactions


def get_all_transactions_from_sender_to_receiver(sender_id: str, receiver_id: str, uow: AbstractUnitOfWork):
    """ generel fuction | Get all transactions from sender to receiver"""
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.full_name AS sender_name,
            recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where txn.sender_wallet_id = %s and txn.recipient_wallet_id = %s
            order by txn.created_at desc
        """
        uow.cursor.execute(
            sql,
            [
                sender_id,
                receiver_id
            ]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(
            rows)

        return transactions


def get_all_beneficiaries_of_passed_user(sender_id: str, uow: AbstractUnitOfWork):
    """ generel fuction | Get all beneficiaries of a user"""
    sql = """
        select txn.recipient_wallet_id,
        beneficiary.full_name AS beneficiary_name
        from transactions txn
        inner join users beneficiary on txn.recipient_wallet_id = beneficiary.id
        where txn.sender_wallet_id = %s
    """
    uow.cursor.execute(
        sql,
        [
            sender_id
        ]
    )
    rows = uow.cursor.fetchall()

    beneficiaries = [
        {
            "id": row[0],
            "name": row[1]
        }
        for row in rows
    ]

    return beneficiaries

def get_all_benefactors_of_passed_user(receiver_id: str, uow: AbstractUnitOfWork):
    """ generel fuction | Get all benefactors of a user"""
    sql = """
        select txn.sender_wallet_id,
        benefactor.full_name AS benefactor_name
        from transactions txn
        inner join users benefactor on txn.sender_wallet_id = benefactor.id
        where txn.recipient_wallet_id = %s
    """
    uow.cursor.execute(
        sql,
        [
            receiver_id
        ]
    )
    rows = uow.cursor.fetchall()

    benefactors = [
        {
            "id": row[0],
            "name": row[1]
        }
        for row in rows
    ]

    return benefactors