"""
1. get wallet balance from wallet_id    || later update to get balance from user_id
2. get user id from wallet id           || will be removed once refactored
3. get wallet from wallet id            || will be updated to get wallet from user id
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
12. get all transactions between two specified users
13. get all transaction from specifies sender to receiver
14. get all beneficiaries of a user
15. get all benefactors of a user
"""

from datetime import datetime
from typing import List, Optional

from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import view_models as pmt_vm


def get_wallet_balance(
    wallet_id: str,
    uow: AbstractUnitOfWork,
) -> int:
    sql = """
        select balance
        from wallets
        where id = %(wallet_id)s
        """
    uow.dict_cursor.execute(sql, {"wallet_id": wallet_id})
    row = uow.dict_cursor.fetchone()

    if row is None:
        raise pmt_svc_ex.WalletNotExists

    return row["balance"]


def get_starred_wallet_id(uow: AbstractUnitOfWork) -> str:
    """
    keeping it here for now, will move it later after discussion
    """
    sql = """
        select wallet_id
        from starred_wallet_id
    """
    uow.dict_cursor.execute(sql)
    row = uow.dict_cursor.fetchone()

    if row is None:
        raise pmt_svc_ex.CardPayWalletNotExists

    return row["wallet_id"]


def get_wallet_id_from_unique_identifier_and_closed_loop_id(
    unique_identifier: str, closed_loop_id: str, uow: AbstractUnitOfWork
) -> str:
    """generel fuction | Get wallet id from unique identifier and closed loop id"""
    sql = """
        select
            user_id
        from
            user_closed_loops ucl
        where
            ucl.unique_identifier = %(unique_identifier)s
            and ucl.closed_loop_id = %(closed_loop_id)s
            and ucl.status = 'VERIFIED'::closed_loop_user_state_enum
    """
    uow.dict_cursor.execute(
        sql,
        {
            "unique_identifier": unique_identifier,
            "closed_loop_id": closed_loop_id,
        },
    )
    rows = uow.dict_cursor.fetchall()

    if len(rows) == 0:
        raise pmt_svc_ex.UserDoesNotExistException(f"No user found against {unique_identifier}")
    assert len(rows) == 1

    return rows[0]["user_id"]


def get_all_closed_loops_id_and_names(
    uow: AbstractUnitOfWork,
):
    sql = """
            select id, name
            from closed_loops
        """

    uow.dict_cursor.execute(sql)
    rows = uow.dict_cursor.fetchall()

    closed_loops = [pmt_vm.ClosedLoopIdNameDTO.from_db_dict_row(row) for row in rows]

    return closed_loops


def get_all_successful_transactions_of_a_user(
    user_id: str, uow: AbstractUnitOfWork, page_size: int, offset: int
) -> List[pmt_vm.TransactionWithIdsDTO]:
    """generel fuction | Get all transactions of a user"""
    sql = """
        select 
            txn.id, 
            txn.amount, 
            txn.mode, 
            txn.transaction_type, 
            txn.status, 
            txn.created_at, 
            txn.last_updated,
            txn.sender_wallet_id as sender_id,
            txn.recipient_wallet_id as recipient_id,
            sender.full_name as sender_name,
            recipient.full_name as recipient_name
        from 
            transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
        where 
            (
                txn.sender_wallet_id = %(user_id)s 
                or txn.recipient_wallet_id = %(user_id)s
            )
            and txn.status = 'SUCCESSFUL'::transaction_status_enum
        order by 
            txn.created_at desc
        limit %(page_size)s offset %(offset)s
    """
    uow.dict_cursor.execute(
        sql,
        {
            "user_id": user_id,
            "page_size": page_size,
            "offset": offset,
        },
    )
    rows = uow.dict_cursor.fetchall()

    transactions = [pmt_vm.TransactionWithIdsDTO.from_db_dict_row(row) for row in rows]
    return transactions


def payment_retools_get_customers_and_vendors_of_selected_closed_loop(
    uow: AbstractUnitOfWork, closed_loop_id: str
):
    sql = """
            select count(*)
            from users u
            join user_closed_loops ucl on u.id = ucl.user_id
            where ucl.closed_loop_id = %(closed_loop_id)s
        """

    uow.dict_cursor.execute(sql, {"closed_loop_id": closed_loop_id})
    row = uow.dict_cursor.fetchone()
    user_count = row["count"] if row else 0

    sql = """
            select 
                u.id as id,
                u.full_name as full_name,
                u.wallet_id as wallet_id,
                ucl.unique_identifier as unique_identifier,
                ucl.closed_loop_user_id as closed_loop_user_id
            from 
                users u
                join user_closed_loops ucl on u.id = ucl.user_id
            where 
                ucl.closed_loop_id = %(closed_loop_id)s
                and u.user_type = 'CUSTOMER'::user_type_enum
        """
    uow.dict_cursor.execute(sql, {"closed_loop_id": closed_loop_id})
    rows = uow.dict_cursor.fetchall()

    customers = [pmt_vm.CustomerDTO.from_db_dict_row(row) for row in rows]

    sql = """
            select 
                u.id as id,
                u.full_name as full_name,
                u.wallet_id as wallet_id,
                ucl.unique_identifier as unique_identifier,
                ucl.closed_loop_user_id as closed_loop_user_id
            from 
                users u
                join user_closed_loops ucl on u.id = ucl.user_id
            where 
                ucl.closed_loop_id = %(closed_loop_id)s
                and u.user_type = 'VENDOR'::user_type_enum
        """

    uow.dict_cursor.execute(sql, {"closed_loop_id": closed_loop_id})
    rows = uow.dict_cursor.fetchall()

    vendors = [pmt_vm.VendorDTO.from_db_dict_row(row) for row in rows]

    counts = pmt_vm.CountsDTO(
        customers=len(customers),
        vendors=len(vendors),
        count=user_count,
    )

    return pmt_vm.CustomerVendorCountsDTO(
        customers=customers,
        vendors=vendors,
        counts=counts,
    )


def payment_retools_get_all_transactions_of_selected_user(
    user_id: str,
    uow: AbstractUnitOfWork,
) -> List[pmt_vm.TransactionWithIdsDTO]:
    sql = """
        select 
            txn.id,
            txn.amount,
            txn.mode,
            txn.transaction_type,
            txn.status,
            txn.created_at,
            txn.last_updated,
            txn.sender_wallet_id as sender_id,
            txn.recipient_wallet_id as recipient_id,
            sender.full_name as sender_name,
            recipient.full_name as recipient_name
        from 
            transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
        where 
            txn.sender_wallet_id = %(user_id)s
            or txn.recipient_wallet_id = %(user_id)s
        order by txn.created_at desc
    """

    uow.dict_cursor.execute(sql, {"user_id": user_id})
    rows = uow.dict_cursor.fetchall()

    transactions = [pmt_vm.TransactionWithIdsDTO.from_db_dict_row(row) for row in rows]

    return transactions


def payment_retools_get_vendors_and_balance(
    closed_loop_id: str,
    uow: AbstractUnitOfWork,
):
    sql = """
        select
            u.id,
            u.full_name,
            u.wallet_id,
            w.balance
        from 
            users u
            join wallets w on u.wallet_id = w.id
            join user_closed_loops ucl on u.id = ucl.user_id
        where 
            ucl.closed_loop_id = %(closed_loop_id)s
            and u.user_type = 'VENDOR'::user_type_enum
            and w.balance > 0
    """

    uow.dict_cursor.execute(sql, {"closed_loop_id": closed_loop_id})
    rows = uow.dict_cursor.fetchall()
    vendors = [pmt_vm.VendorAndBalanceDTO.from_db_dict_row(row) for row in rows]

    return vendors


def payment_retools_get_transactions_to_be_reconciled(
    vendor_id: str,
    uow: AbstractUnitOfWork,
) -> List[pmt_vm.TransactionWithIdsDTO]:
    last_reconciliation_timestamp = """
        select 
            max(created_at)
        from 
            transactions
        where 
            transaction_type = 'RECONCILIATION'::transaction_type_enum
            and sender_wallet_id = %(vendor_id)s;
    """

    uow.dict_cursor.execute(last_reconciliation_timestamp, {"vendor_id": vendor_id})
    row = uow.dict_cursor.fetchone()

    sql = """
        select 
            txn.id, 
            txn.amount, 
            txn.mode, 
            txn.transaction_type, 
            txn.status, 
            txn.created_at, 
            txn.last_updated,
            txn.sender_wallet_id as sender_id,
            txn.recipient_wallet_id as recipient_id,
            sender.full_name as sender_name,
            recipient.full_name as recipient_name
        from 
            transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
        where 
            (
                txn.sender_wallet_id = %(vendor_id)s 
                or txn.recipient_wallet_id = %(vendor_id)s
            ) 
            and txn.status = 'SUCCESSFUL'::transaction_status_enum
            and txn.transaction_type != 'RECONCILIATION'::transaction_type_enum
    """

    if row is not None:
        last_reconciliation_timestamp = row["max"]
        sql += f" and txn.last_updated >= '{str(last_reconciliation_timestamp)}'"

    sql += " order by txn.last_updated desc"

    uow.dict_cursor.execute(sql, {"vendor_id": vendor_id})
    rows = uow.dict_cursor.fetchall()

    transactions = [pmt_vm.TransactionWithIdsDTO.from_db_dict_row(row) for row in rows]

    return transactions


def payment_retools_get_vendors(
    closed_loop_id: str,
    uow: AbstractUnitOfWork,
):
    sql = """
            select 
                u.id as id, 
                u.full_name as full_name, 
                u.wallet_id as wallet_id,
                ucl.unique_identifier as unique_identifier,
                ucl.closed_loop_user_id as closed_loop_user_id
            from 
                users u
                join user_closed_loops ucl on u.id = ucl.user_id
            where 
                ucl.closed_loop_id = %(closed_loop_id)s
                and u.user_type = 'VENDOR'::user_type_enum
        """

    uow.dict_cursor.execute(sql, {"closed_loop_id": closed_loop_id})
    rows = uow.dict_cursor.fetchall()

    vendors = [pmt_vm.VendorDTO.from_db_dict_row(row) for row in rows]

    return vendors


def payment_retools_get_reconciliation_history(
    vendor_id: str,
    uow: AbstractUnitOfWork,
):
    sql = """
        select 
            txn.id, 
            txn.amount, 
            txn.created_at, 
            txn.last_updated
        from 
            transactions txn
        where 
            txn.transaction_type = 'RECONCILIATION'::transaction_type_enum
            and txn.sender_wallet_id = %(vendor_id)s
        order by txn.created_at desc
    """

    uow.dict_cursor.execute(sql, {"vendor_id": vendor_id})
    rows = uow.dict_cursor.fetchall()

    transactions = [pmt_vm.TransactionWithDates.from_db_dict_row(row) for row in rows]

    return transactions


def payment_retools_get_reconciled_transactions(
    reconciliation_timestamp: str,
    vendor_id: str,
    uow: AbstractUnitOfWork,
) -> List[pmt_vm.TransactionWithIdsDTO]:
    datetime_obj = datetime.strptime(reconciliation_timestamp, "%a, %d %b %Y %H:%M:%S %Z")
    formatted_reconciliation_timestamp = datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")

    # NOTE: the above time is not perfect to the millisecond
    sql = """
        select 
            max(created_at)
        from 
            transactions
        where 
            transaction_type = 'RECONCILIATION'::transaction_type_enum
            and created_at < %(ts)s
            and sender_wallet_id = %(vendor_id)s
    """

    uow.dict_cursor.execute(
        sql,
        {
            "ts": str(formatted_reconciliation_timestamp),
            "vendor_id": vendor_id,
        },
    )

    row = uow.dict_cursor.fetchone()

    sql = """
        select 
            txn.id,
            txn.amount,
            txn.mode,
            txn.transaction_type,
            txn.status,
            txn.created_at,
            txn.last_updated,
            txn.sender_wallet_id as sender_id,
            txn.recipient_wallet_id as recipient_id,
            sender.full_name as sender_name,
            recipient.full_name as recipient_name
        from transactions txn
            inner join users sender 
                on txn.sender_wallet_id = sender.id
            inner join users recipient 
                on txn.recipient_wallet_id = recipient.id
        where 
            (
                txn.sender_wallet_id = %(vendor_id)s 
                or txn.recipient_wallet_id = %(vendor_id)s
            )
            and txn.status != 'PENDING'::transaction_status_enum
            and txn.last_updated < %(ts)s
    """

    if row is not None:
        previous_reconciliation_timestamp = row["max"]
        sql += f" and txn.last_updated >= '{str(previous_reconciliation_timestamp)}'"

    sql += " order by txn.last_updated desc"

    uow.dict_cursor.execute(
        sql,
        {
            "vendor_id": vendor_id,
            "ts": str(formatted_reconciliation_timestamp),
        },
    )
    rows = uow.dict_cursor.fetchall()

    transactions = [pmt_vm.TransactionWithIdsDTO.from_db_dict_row(row) for row in rows]
    return transactions


def get_user_wallet_id_and_type_from_qr_id(
    qr_id: str,
    uow: AbstractUnitOfWork,
) -> Optional[pmt_vm.UserWalletIDAndTypeDTO]:
    sql = """
        select 
            w.id as user_wallet_id,
            u.user_type as user_type
        from 
            wallets w
            join users u on w.id = u.wallet_id
        where 
            w.qr_id = %(qr_id)s
    """

    uow.dict_cursor.execute(sql, {"qr_id": qr_id})
    row = uow.dict_cursor.fetchone()

    return pmt_vm.UserWalletIDAndTypeDTO.from_db_dict_row(row) if row else None


def get_all_vendor_id_name_and_qr_id_of_a_closed_loop(
    closed_loop_id: str,
    uow: AbstractUnitOfWork,
) -> List[pmt_vm.VendorQrIdDTO]:
    sql = """

        select 
            u.id, 
            u.full_name, 
            w.qr_id
        from 
            users u
            join wallets w on u.wallet_id = w.id
            join user_closed_loops ucl on u.id = ucl.user_id
        where 
            ucl.closed_loop_id = %(closed_loop_id)s
            and u.user_type = 'VENDOR'::user_type_enum
            and u.is_active = true
            and u.is_phone_number_verified = true
            and ucl.status = 'VERIFIED'::closed_loop_user_state_enum
        """

    uow.dict_cursor.execute(sql, {"closed_loop_id": closed_loop_id})
    rows = uow.dict_cursor.fetchall()

    vendors = [pmt_vm.VendorQrIdDTO.from_db_dict_row(row) for row in rows]

    return vendors


def vendor_app_get_transactions_to_be_reconciled(
    vendor_id: str,
    uow: AbstractUnitOfWork,
) -> List[pmt_vm.TransactionWithIdsDTO]:
    sql = """
        select 
            max(created_at)
        from
            transactions
        where 
            transaction_type = 'RECONCILIATION'::transaction_type_enum
            and sender_wallet_id = %(vendor_id)s;
    """

    uow.dict_cursor.execute(sql, {"vendor_id": vendor_id})
    row = uow.dict_cursor.fetchone()

    sql = """
        select 
            txn.id, 
            txn.amount, 
            txn.mode, 
            txn.transaction_type, 
            txn.status, 
            txn.created_at, 
            txn.last_updated,
            txn.sender_wallet_id as sender_id,
            txn.recipient_wallet_id as recipient_id,
            sender.full_name as sender_name,
            recipient.full_name as recipient_name
        from 
            transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
        where
            txn.recipient_wallet_id = %(vendor_id)s
            and txn.status = 'SUCCESSFUL'::transaction_status_enum
            and txn.transaction_type != 'RECONCILIATION'::transaction_type_enum
    """

    if row is not None:
        last_reconciliation_timestamp = row["max"]
        sql += f" and txn.last_updated >= '{str(last_reconciliation_timestamp)}'"

    sql += " order by txn.last_updated desc"

    uow.dict_cursor.execute(sql, {"vendor_id": vendor_id})
    rows = uow.dict_cursor.fetchall()

    transactions = [pmt_vm.TransactionWithIdsDTO.from_db_dict_row(row) for row in rows]

    return transactions


def get_tx_balance(tx_id: str, uow: AbstractUnitOfWork) -> int:
    sql = """
        select amount
        from transactions
        where id = %(tx_id)s
    """
    uow.dict_cursor.execute(sql, {"tx_id": tx_id})
    row = uow.dict_cursor.fetchone()

    if row is None:
        raise pmt_svc_ex.TransactionNotFound(f"Transaction not found for id {tx_id}")

    return row["amount"]


def get_tx_recipient(tx_id: str, uow: AbstractUnitOfWork) -> str:
    sql = """
        select recipient_wallet_id
        from transactions
        where id = %(tx_id)s
    """
    uow.dict_cursor.execute(sql, {"tx_id": tx_id})
    row = uow.dict_cursor.fetchone()

    if row is None:
        raise pmt_svc_ex.TransactionNotFound(f"Transaction not found for id {tx_id}")

    return row["recipient_wallet_id"]


# def get_all_beneficiaries_of_passed_user(
#     sender_id: str, uow: AbstractUnitOfWork, page_size: int, offset: int
# ):
#     """generel fuction | Get all beneficiaries of a user"""
#     sql = """
#         select txn.recipient_wallet_id,
#         beneficiary.full_name AS beneficiary_name
#         from transactions txn
#         inner join users beneficiary on txn.recipient_wallet_id = beneficiary.id
#         where txn.sender_wallet_id = %s
#         limit %s offset %s
#     """
#     uow.cursor.execute(sql, [sender_id, page_size, offset])
#     rows = uow.cursor.fetchall()

#     beneficiaries = [{"id": row[0], "name": row[1]} for row in rows]

#     return beneficiaries


# def get_all_benefactors_of_passed_user(
#     receiver_id: str, uow: AbstractUnitOfWork, page_size: int, offset: int
# ):
#     """generel fuction | Get all benefactors of a user"""
#     sql = """
#         select txn.sender_wallet_id,
#         benefactor.full_name AS benefactor_name
#         from transactions txn
#         inner join users benefactor on txn.sender_wallet_id = benefactor.id
#         where txn.recipient_wallet_id = %s
#         limit %s offset %s
#     """
#     uow.cursor.execute(sql, [receiver_id, page_size, offset])
#     rows = uow.cursor.fetchall()

#     benefactors = [{"id": row[0], "name": row[1]} for row in rows]
#     return benefactors
