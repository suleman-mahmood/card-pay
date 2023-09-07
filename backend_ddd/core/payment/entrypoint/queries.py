# from ..domain.model import Wallet
from ..domain import model as payment_model
from ...entrypoint.uow import AbstractUnitOfWork
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass
from ...authentication.domain import model as auth_mdl
from core.payment.entrypoint.queries_exceptions import UserDoesNotExistException
from core.payment.entrypoint import view_models as auth_vm


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
        uow.cursor.execute(sql, [wallet_id])
        row = uow.cursor.fetchone()
        return row[0]


def get_wallet_from_wallet_id(wallet_id: str, uow: AbstractUnitOfWork):
    with uow:
        sql = """
            select id, balance, qr_id
            from wallets
            where id = %s
        """
        uow.cursor.execute(sql, [wallet_id])
        row = uow.cursor.fetchone()
        return payment_model.Wallet(
            id=row[0],
            balance=row[1],
            qr_id=row[2],
        )


def get_user_id_from_wallet_id(wallet_id: str, uow: AbstractUnitOfWork) -> str:
    sql = """
        select id
        from users
        where wallet_id = %s
    """
    uow.cursor.execute(sql, [wallet_id])
    row = uow.cursor.fetchone()
    return row[0]


# def add_starred_wallet_id(wallet_id: str, uow: AbstractUnitOfWork):
#     """
#     keeping it here for now, will move it later after discussion
#     """
#     with uow:
#         delete_sql = """
#             delete from starred_wallet_id
#         """
#         uow.cursor.execute(delete_sql)

#         sql = """
#             insert into starred_wallet_id
#             values (%s)
#         """
#         uow.cursor.execute(sql, [wallet_id])
#         uow.connection.commit()


def get_starred_wallet_id(uow: AbstractUnitOfWork) -> str:
    """
    keeping it here for now, will move it later after discussion
    """
    sql = """
        select wallet_id
        from starred_wallet_id
    """
    uow.cursor.execute(sql)
    rows = uow.cursor.fetchall()
    return rows[0]


def get_transaction_by_transaction_id(transaction_id: str, uow: AbstractUnitOfWork):
    with uow:
        transaction = uow.transactions.get(transaction_id)
        return transaction


def _helper_generate_list_of_transactions_for_admin(rows):
    """for admin get functions | helper function to create multiple transaction objects"""
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
            "recipient_name": row[10],
        }
        for row in rows
    ]

    return transactions


def _helper_generate_list_of_transactions_for_general_case(rows):
    "for general get functions | helper function to create multiple transaction objects. Dont return IDs here. Check references before changing return structure"

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
            "recipient_name": row[8],
        }
        for row in rows
    ]

    return transactions


def get_all_transactions(uow: AbstractUnitOfWork, page_size: int, offset: int):
    """admin function | Get all transactions"""
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.id AS sender_id, sender.full_name AS sender_name,
            recipient.id AS recipient_id, recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            order by txn.created_at desc
            limit %s offset %s
        """

        uow.cursor.execute(sql, [page_size, offset])

        rows = uow.cursor.fetchall()
        transactions = _helper_generate_list_of_transactions_for_admin(rows)

        return transactions


def get_all_transactions_of_a_type(
    transaction_type: payment_model.TransactionType,
    uow: AbstractUnitOfWork,
    page_size: int,
    offset: int,
):
    """admin function | Get all transactions of a type"""

    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.id AS sender_id, sender.full_name AS sender_name,
            recipient.id AS recipient_id, recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where txn.transaction_type = %s::transaction_type_enum
            order by txn.created_at desc
            limit %s offset %s
        """

        uow.cursor.execute(sql, [transaction_type.name, page_size, offset])
        rows = uow.cursor.fetchall()
        transactions = _helper_generate_list_of_transactions_for_admin(rows)

        return transactions


def get_all_successful_transactions_of_a_user(
    user_id: str, uow: AbstractUnitOfWork, page_size: int, offset: int
) -> List[Dict[str, str]]:
    """generel fuction | Get all transactions of a user"""
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.full_name AS sender_name,
            recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where txn.sender_wallet_id = %s or txn.recipient_wallet_id = %s
            and txn.status = 'SUCCESSFUL'::transaction_status_enum
            order by txn.created_at desc
            limit %s offset %s
        """
        uow.cursor.execute(sql, [user_id, user_id, page_size, offset])
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(rows)
        return transactions


def get_all_transactions_of_a_user_of_a_type(
    user_id: str,
    transaction_type: payment_model.TransactionType,
    uow: AbstractUnitOfWork,
    page_size: int,
    offset: int,
):
    """generel fuction | Get all transactions of a user of a type"""
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            sender.full_name AS sender_name,
            recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where (txn.sender_wallet_id = %s or txn.recipient_wallet_id = %s) and txn.transaction_type = %s::transaction_type_enum
            order by txn.created_at desc
            limit %s offset %s
        """
        uow.cursor.execute(
            sql, [user_id, user_id, transaction_type.name, page_size, offset]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(rows)
        return transactions


def get_all_cash_inflow_transactions_of_a_user(
    user_id: str, uow: AbstractUnitOfWork, page_size: int, offset: int
):
    """generel fuction | Get all cash inflow transactions of a user"""
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
            limit %s offset %s
        """
        uow.cursor.execute(sql, [user_id, page_size, offset])
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(rows)

        return transactions


def get_all_cash_outflow_transactions_of_a_user(
    user_id: str, uow: AbstractUnitOfWork, page_size: int, offset: int
):
    """generel fuction | Get all cash outflow transactions of a user"""
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
            limit %s offset %s
        """
        uow.cursor.execute(sql, [user_id, page_size, offset])
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(rows)

        return transactions


def get_all_transactions_between_two_users(
    user1_id: str, user2_id: str, uow: AbstractUnitOfWork, page_size: int, offset: int
):
    """admin fuction | Get all transactions between two users"""
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
            limit %s offset %s
        """
        uow.cursor.execute(
            sql, [user1_id, user2_id, user2_id, user1_id, page_size, offset]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_admin(rows)

        return transactions


def get_all_transactions_from_sender_to_receiver(
    sender_id: str,
    receiver_id: str,
    uow: AbstractUnitOfWork,
    page_size: int,
    offset: int,
):
    """generel fuction | Get all transactions from sender to receiver"""
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
            limit %s offset %s
        """
        uow.cursor.execute(sql, [sender_id, receiver_id, page_size, offset])
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(rows)

        return transactions


def get_all_beneficiaries_of_passed_user(
    sender_id: str, uow: AbstractUnitOfWork, page_size: int, offset: int
):
    """generel fuction | Get all beneficiaries of a user"""
    sql = """
        select txn.recipient_wallet_id,
        beneficiary.full_name AS beneficiary_name
        from transactions txn
        inner join users beneficiary on txn.recipient_wallet_id = beneficiary.id
        where txn.sender_wallet_id = %s
        limit %s offset %s
    """
    uow.cursor.execute(sql, [sender_id, page_size, offset])
    rows = uow.cursor.fetchall()

    beneficiaries = [{"id": row[0], "name": row[1]} for row in rows]

    return beneficiaries


def get_all_benefactors_of_passed_user(
    receiver_id: str, uow: AbstractUnitOfWork, page_size: int, offset: int
):
    """generel fuction | Get all benefactors of a user"""
    sql = """
        select txn.sender_wallet_id,
        benefactor.full_name AS benefactor_name
        from transactions txn
        inner join users benefactor on txn.sender_wallet_id = benefactor.id
        where txn.recipient_wallet_id = %s
        limit %s offset %s
    """
    uow.cursor.execute(sql, [receiver_id, page_size, offset])
    rows = uow.cursor.fetchall()

    benefactors = [{"id": row[0], "name": row[1]} for row in rows]
    return benefactors


def get_wallet_id_from_unique_identifier(
    unique_identifier: str, closed_loop_id: str, uow: AbstractUnitOfWork
) -> str:
    """generel fuction | Get wallet id from unique identifier and closed loop id"""
    sql = """
        select u.wallet_id
        from users u
        join user_closed_loops ucl on u.id = ucl.user_id
        where ucl.unique_identifier = %s
        and ucl.closed_loop_id = %s
        and ucl.status = 'VERIFIED'::closed_loop_user_state_enum
    """
    uow.cursor.execute(sql, [unique_identifier, closed_loop_id])
    row = uow.cursor.fetchall()

    if len(row) == 0:
        raise UserDoesNotExistException(f"No user found against {unique_identifier}")
    assert len(row) == 1

    return row[0]


def payment_retools_get_all_closed_loops(
    uow: AbstractUnitOfWork,
):
    with uow:
        sql = """
                select id, name
                from closed_loops
            """

        uow.cursor.execute(sql)
        rows = uow.cursor.fetchall()

        closed_loops = [{"id": row[0], "name": row[1]} for row in rows]

    return closed_loops


def payment_retools_get_customers_and_ventors_of_selected_closed_loop(
    uow: AbstractUnitOfWork, closed_loop_id: str
):
    with uow:
        sql = """
                select count(*)
                from users u
                join user_closed_loops ucl on u.id = ucl.user_id
                where ucl.closed_loop_id = %s
            """

        uow.cursor.execute(sql, [closed_loop_id])
        row = uow.cursor.fetchone()
        user_count = row[0]

        sql = """
                select u.id, u.full_name, u.wallet_id, ucl.unique_identifier, ucl.closed_loop_user_id
                from users u
                join user_closed_loops ucl on u.id = ucl.user_id
                where ucl.closed_loop_id = %s
                and u.user_type = 'CUSTOMER'::user_type_enum
            """
        uow.cursor.execute(sql, [closed_loop_id])
        rows = uow.cursor.fetchall()

        customers = [
            {
                "id": row[0],
                "full_name": row[1],
                "wallet_id": row[2],
                "unique_identifier": row[3],
                "closed_loop_user_id": row[4],
            }
            for row in rows
        ]

        sql = """
                select u.id, u.full_name, u.wallet_id, ucl.unique_identifier, ucl.closed_loop_user_id
                from users u
                join user_closed_loops ucl on u.id = ucl.user_id
                where ucl.closed_loop_id = %s
                and u.user_type = 'VENDOR'::user_type_enum
            """

        uow.cursor.execute(sql, [closed_loop_id])
        rows = uow.cursor.fetchall()

        vendors = [
            {
                "id": row[0],
                "full_name": row[1],
                "wallet_id": row[2],
                "unique_identifier": row[3],
                "closed_loop_user_id": row[4],
            }
            for row in rows
        ]

        counts = [
            {"customers": len(customers), "vendors": len(vendors), "total": user_count}
        ]

    return customers, vendors, counts


def payment_retools_get_all_transactions_of_selected_user(
    user_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            txn.sender_wallet_id, txn.recipient_wallet_id,
            sender.full_name AS sender_name,
            recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where txn.sender_wallet_id = %s or txn.recipient_wallet_id = %s
            order by txn.created_at desc
        """

        uow.cursor.execute(sql, [user_id, user_id])
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(rows)

    return transactions


def payment_retools_get_vendors_and_balance(
    closed_loop_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        sql = """
            select u.id, u.full_name, u.wallet_id, w.balance
            from users u
            join wallets w on u.wallet_id = w.id
            join user_closed_loops ucl on u.id = ucl.user_id
            where ucl.closed_loop_id = %s
            and u.user_type = 'VENDOR'::user_type_enum
            and w.balance > 0
        """

        uow.cursor.execute(sql, [closed_loop_id])
        rows = uow.cursor.fetchall()
        vendors = [
            {
                "id": row[0],
                "full_name": row[1],
                "wallet_id": row[2],
                "balance": row[3],
            }
            for row in rows
        ]

    return vendors


def payment_retools_get_transactions_to_be_reconciled(
    vendor_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        last_reconciliation_timestamp = """
        select max(created_at) from transactions
        where transaction_type = 'RECONCILIATION'::transaction_type_enum
        and sender_wallet_id = %s;

        """

        uow.cursor.execute(last_reconciliation_timestamp, [vendor_id])
        row = uow.cursor.fetchone()

        sql = """
            select txn.id, txn.amount, txn.mode, txn.transaction_type, txn.status, txn.created_at, txn.last_updated,
            txn.sender_wallet_id, txn.recipient_wallet_id,
            sender.full_name AS sender_name,
            recipient.full_name AS recipient_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where (txn.sender_wallet_id = %s or txn.recipient_wallet_id = %s) and txn.status = 'SUCCESSFUL'::transaction_status_enum
        """

        if row[0] is not None:
            last_reconciliation_timestamp = row[0]
            sql += f" and txn.last_updated >= '{str(last_reconciliation_timestamp)}'"

        sql += " order by txn.last_updated desc"

        uow.cursor.execute(sql, [vendor_id, vendor_id])
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(rows)

    return transactions


def payment_retools_get_vendors(
    closed_loop_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        sql = """
                select u.id, u.full_name, u.wallet_id
                from users u
                join user_closed_loops ucl on u.id = ucl.user_id
                where ucl.closed_loop_id = %s
                and u.user_type = 'VENDOR'::user_type_enum
            """

        uow.cursor.execute(sql, [closed_loop_id])
        rows = uow.cursor.fetchall()

        vendors = [
            {
                "id": row[0],
                "name": row[1],
                "wallet_id": row[2],
            }
            for row in rows
        ]

    return vendors


def payment_retools_get_reconciliation_history(
    vendor_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        sql = """
            select txn.id, txn.amount, txn.created_at, txn.last_updated
            from transactions txn
            where txn.transaction_type = 'RECONCILIATION'::transaction_type_enum
            and txn.sender_wallet_id = %s
            order by txn.created_at desc
        """

        uow.cursor.execute(sql, [vendor_id])
        rows = uow.cursor.fetchall()

        transactions = [
            {
                "id": row[0],
                "amount": row[1],
                "created_at": row[2],
                "last_updated": row[3],
            }
            for row in rows
        ]

    return transactions


def payment_retools_get_reconciled_transactions(
    reconciliation_timestamp: str,
    vendor_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        datetime_obj = datetime.strptime(
            reconciliation_timestamp, "%a, %d %b %Y %H:%M:%S %Z"
        )
        formatted_reconciliation_timestamp = datetime_obj.strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

        # NOTE: the above time is not perfect to the millisecond
        previous_vendor_reconciliation_timestamp = """
        select max(created_at) from transactions
        where transaction_type = 'RECONCILIATION'::transaction_type_enum
        and created_at < %s
        and sender_wallet_id = %s
        """

        uow.cursor.execute(
            previous_vendor_reconciliation_timestamp,
            [str(formatted_reconciliation_timestamp), vendor_id],
        )

        row = uow.cursor.fetchone()

        sql = """
            select 
                txn.id,
                txn.amount,
                txn.mode,
                txn.transaction_type,
                txn.status,
                txn.created_at,
                txn.last_updated,
                txn.sender_wallet_id,
                txn.recipient_wallet_id,
                sender.full_name as sender_name,
                recipient.full_name as recipient_name
            from transactions txn
                inner join users sender 
                    on txn.sender_wallet_id = sender.id
                inner join users recipient 
                    on txn.recipient_wallet_id = recipient.id
            where 
                (txn.sender_wallet_id = %s or txn.recipient_wallet_id = %s)
                and txn.status != 'PENDING'::transaction_status_enum
                and txn.last_updated < %s
        """

        if row[0] is not None:
            previous_reconciliation_timestamp = row[0]
            sql += (
                f" and txn.last_updated >= '{str(previous_reconciliation_timestamp)}'"
            )

        sql += " order by txn.last_updated desc"

        uow.cursor.execute(
            sql, [vendor_id, vendor_id, str(formatted_reconciliation_timestamp)]
        )
        rows = uow.cursor.fetchall()

        transactions = _helper_generate_list_of_transactions_for_general_case(rows)

    return transactions


@dataclass
class UserWalletIDAndTypeDTO:
    user_wallet_id: str
    user_type: auth_mdl.UserType


def get_user_wallet_id_and_type_from_qr_id(
    qr_id: str,
    uow: AbstractUnitOfWork,
) -> Optional[UserWalletIDAndTypeDTO]:
    sql = """
        select w.id, u.user_type
        from wallets w
        join users u on w.id = u.wallet_id
        where w.qr_id = %s
    """

    uow.cursor.execute(sql, [qr_id])
    row = uow.cursor.fetchone()

    if row is None:
        return None

    user_info = UserWalletIDAndTypeDTO(
        user_wallet_id=row[0], user_type=auth_mdl.UserType.__members__[row[1]]
    )

    return user_info


def get_all_vendor_id_name_and_qr_id_of_a_closed_loop(
    closed_loop_id: str,
    uow: AbstractUnitOfWork,
) -> List[auth_vm.VendorQrIdDTO]:
    sql = """

        select u.id, u.full_name, w.qr_id
        from users u
            join wallets w on u.wallet_id = w.id
            join user_closed_loops ucl on u.id = ucl.user_id
        where ucl.closed_loop_id = %s
            and u.user_type = 'VENDOR'::user_type_enum
            and u.is_active = true
            and u.is_phone_number_verified = true
            and ucl.status = 'VERIFIED'::closed_loop_user_state_enum
        """

    uow.cursor.execute(sql, [closed_loop_id])
    rows = uow.cursor.fetchall()

    vendors = [
        auth_vm.VendorQrIdDTO(id=row[0], full_name=row[1], qr_id=row[2]) for row in rows
    ]

    return vendors


def vendor_app_get_transactions_to_be_reconciled(
    vendor_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        last_reconciliation_timestamp = """
        select max(created_at) from transactions
        where transaction_type = 'RECONCILIATION'::transaction_type_enum
        and sender_wallet_id = %s;

        """

        uow.cursor.execute(last_reconciliation_timestamp, [vendor_id])
        row = uow.cursor.fetchone()

        sql = """
            select txn.amount, txn.status, txn.created_at, txn.last_updated,
            sender.full_name as sender_name
            from transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            where (txn.sender_wallet_id = %s or txn.recipient_wallet_id = %s) and txn.status = 'SUCCESSFUL'::transaction_status_enum
        """

        if row[0] is not None:
            last_reconciliation_timestamp = row[0]
            sql += f" and txn.last_updated >= '{str(last_reconciliation_timestamp)}'"

        sql += " order by txn.last_updated desc"

        uow.cursor.execute(sql, [vendor_id, vendor_id])
        rows = uow.cursor.fetchall()

        transactions = [
            {
                "amount": row[0],
                "status": row[1],
                "created_at": row[2],
                "last_updated": row[3],
                "sender_name": row[4],
            }
            for row in rows
        ]

    return transactions
