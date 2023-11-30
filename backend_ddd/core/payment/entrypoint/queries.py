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

RECENT_TXS_COUNT = 10


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
            txn.created_at at time zone '+5', 
            txn.last_updated at time zone '+5',
            txn.sender_wallet_id as sender_id,
            txn.recipient_wallet_id as recipient_id,
            txn.paypro_id,
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
            txn.paypro_id,
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
            and (u.user_type = 'VENDOR'::user_type_enum or u.user_type = 'EVENT_ORGANIZER'::user_type_enum)
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
            txn.paypro_id,
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

    if row is not None and row["max"] is not None:
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
    reconciliation_txn_id: str,
    vendor_id: str,
    uow: AbstractUnitOfWork,
) -> List[pmt_vm.TransactionWithIdsDTO]:
    sql = """
        select
            created_at
        from
            transactions
        where
            id = %(reconciliation_txn_id)s
    """

    uow.dict_cursor.execute(
        sql,
        {"reconciliation_txn_id": reconciliation_txn_id},
    )

    selected_reconciliation_timestamp = uow.dict_cursor.fetchone()

    sql = """
        select 
            max(created_at) as prev_created_at
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
            "ts": str(selected_reconciliation_timestamp["created_at"]),
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
            txn.paypro_id,
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
            and txn.status = 'SUCCESSFUL'::transaction_status_enum
            and txn.transaction_type != 'RECONCILIATION'::transaction_type_enum
            and txn.last_updated < %(ts)s
    """

    if row is not None and row["prev_created_at"] is not None:
        previous_reconciliation_timestamp = row["prev_created_at"]
        sql += f" and txn.last_updated > '{str(previous_reconciliation_timestamp)}'"

    sql += " order by txn.last_updated desc"

    uow.dict_cursor.execute(
        sql,
        {
            "vendor_id": vendor_id,
            "ts": str(selected_reconciliation_timestamp["created_at"]),
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


def get_daily_successful_deposits(uow: AbstractUnitOfWork):
    sql = """
        select
            date(tx.created_at at time zone '+5') as day,
            count(*) as successful_deposit_count,
            sum(tx.amount) as total_amount,
            avg(tx.amount)::int as avg_amount,
            json_agg(u.full_name) as heros
        from
            transactions tx
            join users u on u.id = tx.recipient_wallet_id
        where
            transaction_type = 'PAYMENT_GATEWAY'
            and status = 'SUCCESSFUL'
        group by day
        order by day desc;
        """
    uow.dict_cursor.execute(sql)
    rows = uow.dict_cursor.fetchall()

    return [pmt_vm.DailySuccessfulDepositsDTO.from_db_dict_row(row) for row in rows]


def get_daily_pending_deposits(uow: AbstractUnitOfWork):
    sql = """
        select
            date(tx.created_at at time zone '+5') as day,
            count(*) as pending_deposit_count,
            sum(tx.amount) as total_amount,
            avg(tx.amount)::int as avg_amount,
            json_agg(u.full_name) as pending_heros
        from
            transactions tx
            join users u on u.id = tx.recipient_wallet_id
        where
            transaction_type = 'PAYMENT_GATEWAY'
            and status = 'PENDING'
        group by day
        order by day desc;
        """
    uow.dict_cursor.execute(sql)
    rows = uow.dict_cursor.fetchall()

    return [pmt_vm.DailyPendingDepositsDTO.from_db_dict_row(row) for row in rows]


def get_daily_transactions(uow: AbstractUnitOfWork):
    sql = """
    SELECT DATE(created_at at time zone '+5') AS day,
        COUNT(*) AS transaction_count,
        SUM(amount) AS total_amount,
        AVG(amount)::INT AS avg_amount
    FROM transactions
    where
        status = 'SUCCESSFUL'
        and transaction_type != 'CARD_PAY'

    GROUP BY day
    ORDER BY day desc;
    """

    uow.dict_cursor.execute(sql)
    rows = uow.dict_cursor.fetchall()

    return [pmt_vm.DailyTransactionsDTO.from_db_dict_row(row) for row in rows]


def get_monthly_transactions(uow: AbstractUnitOfWork):
    sql = """
        SELECT
            DATE_TRUNC('month', created_at at time zone '+5') AS month,
            COUNT(*) AS transaction_count,
            SUM(amount) AS total_amount,
            AVG(amount)::INT AS avg_amount
        FROM
            transactions
        where
            status = 'SUCCESSFUL'
            and transaction_type != 'CARD_PAY'

        GROUP BY DATE_TRUNC('month', created_at at time zone '+5')
        ORDER BY month;
        """

    uow.dict_cursor.execute(sql)
    rows = uow.dict_cursor.fetchall()

    return [pmt_vm.MonthlyTransactionsDTO.from_db_dict_row(row) for row in rows]


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


def get_last_deposit_transaction(
    user_id: str, uow: AbstractUnitOfWork
) -> pmt_vm.DepositTransactionDTO:
    sql = """
        select
            id,
            paypro_id,
            amount,
            mode,
            transaction_type,
            status,
            created_at at time zone '+5' as created_at,
            last_updated at time zone '+5' as last_updated
        from
            transactions
        where
            recipient_wallet_id = %(user_id)s
            and transaction_type = 'PAYMENT_GATEWAY'::transaction_type_enum
        order by
            created_at desc
        limit 1
    """
    uow.dict_cursor.execute(sql, {"user_id": user_id})
    row = uow.dict_cursor.fetchone()

    if row is None:
        raise pmt_svc_ex.NoUserDepositRequest(f"User has no deposit request for id {user_id}")

    return pmt_vm.DepositTransactionDTO.from_db_dict_row(row)


def get_vendor_latest_reconciliation_txn_id(
    vendor_id: str,
    uow: AbstractUnitOfWork,
):
    sql = """
        select
            id
        from
            transactions
        where
            transaction_type = 'RECONCILIATION'::transaction_type_enum
            and sender_wallet_id = %(vendor_id)s
        order by
            created_at desc
        limit 1
    """

    uow.dict_cursor.execute(sql, {"vendor_id": vendor_id})
    row = uow.dict_cursor.fetchone()
    if row is None:
        raise pmt_svc_ex.NoLatestReconciliationFound("No Latest Reconcilation txn found.")
    return row["id"]


def get_vendor_previous_reconciliation_txn_id(
    vendor_id: str, reconciled_txn_id: str, uow: AbstractUnitOfWork
):
    sql = """
        select
            id
        from
            transactions
        where
            transaction_type = 'RECONCILIATION'::transaction_type_enum
            and sender_wallet_id = %(vendor_id)s
            and created_at < (
                select created_at
                from transactions
                where id = %(ts)s
            )
        order by
            created_at desc
        limit 1
    """

    uow.dict_cursor.execute(
        sql,
        {
            "vendor_id": vendor_id,
            "ts": str(reconciled_txn_id),
        },
    )

    row = uow.dict_cursor.fetchone()

    if row is None:
        raise pmt_svc_ex.NoPreviousReconciliationFound("No previous reconciliation found")
    return row["id"]


def get_vendor_next_reconciliation_txn_id(
    vendor_id: str, reconciled_txn_id: str, uow: AbstractUnitOfWork
):
    sql = """
        select
            id
        from
            transactions
        where
            transaction_type = 'RECONCILIATION'::transaction_type_enum
            and sender_wallet_id = %(vendor_id)s
            and created_at > (
                select created_at
                from transactions
                where id = %(ts)s
            )
        order by
            created_at asc
        limit 1
    """

    uow.dict_cursor.execute(
        sql,
        {
            "vendor_id": vendor_id,
            "ts": str(reconciled_txn_id),
        },
    )

    row = uow.dict_cursor.fetchone()

    if row is None:
        raise pmt_svc_ex.NoNextReconciliationFound(f"No next reconciliation found")

    return row["id"]


def get_last_n_pending_deposit_transactions(
    uow: AbstractUnitOfWork,
) -> List[pmt_vm.PayProAndTxIDsDTO]:
    sql = """
        select
            paypro_id,
            id
        from
            transactions tx
        where
            transaction_type='PAYMENT_GATEWAY'
            and status = 'PENDING'
        order by tx.created_at desc
        limit %(recent_txs_count)s
    """
    uow.dict_cursor.execute(sql, {"recent_txs_count": RECENT_TXS_COUNT})
    rows = uow.dict_cursor.fetchall()

    return [pmt_vm.PayProAndTxIDsDTO.from_db_dict_row(row=r) for r in rows]


def get_deposit_requests(uow: AbstractUnitOfWork) -> List[pmt_vm.DepositRequest]:
    sql = """
        select
            tx.id,
            tx.created_at at time zone '+5' as created_at,
            tx.last_updated at time zone '+5' as last_updated,
            amount,
            r.full_name as recipient_name,
            s.full_name as sender_name,
            status,
            tx.paypro_id
        from
            transactions tx
            inner join users r on tx.recipient_wallet_id = r.wallet_id
            inner join users s on tx.sender_wallet_id = s.wallet_id
        where
            transaction_type='PAYMENT_GATEWAY'
        order by tx.created_at desc
    """

    uow.dict_cursor.execute(sql)
    rows = uow.dict_cursor.fetchall()

    return [pmt_vm.DepositRequest.from_db_dict_row(r) for r in rows]


def get_daily_user_checkpoints(
    uow: AbstractUnitOfWork,
) -> List[pmt_vm.DailyUserCheckpoints]:
    sql = """
        with total_users as (
            -- Daily users that tried to sign up
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
            group by day
            order by day desc
        ), phone_verified_users as (
            -- Daily users that verified their phone otp
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
                join users u on w.id = u.wallet_id
            where
                is_phone_number_verified
            group by day
            order by day desc
        ), phone_unverified_users as (
            -- Daily users that failed to verify their phone otp
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
                join users u on w.id = u.wallet_id
            where
                not is_phone_number_verified
            group by day
            order by day desc
        ), lums_registered_users as (
            -- Daily users that tried to register to a closed loop
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
                join user_closed_loops ucl on w.id = ucl.user_id
            group by day
            order by day desc
        ), lums_verified_users as (
            -- Daily users that verified their closed loop
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
                join user_closed_loops ucl on w.id = ucl.user_id
            where
                ucl.status = 'VERIFIED'
            group by day
            order by day desc
        ), lums_unverified_users as (
            -- Daily users that failed to verify their closed loop
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
                join user_closed_loops ucl on w.id = ucl.user_id
            where
                ucl.status = 'UN_VERIFIED'
            group by day
            order by day desc
        ), signup_success_users as (
            -- Daily users that are at the dashboard
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
                join users u on w.id = u.wallet_id
            where
                pin != '0000'
            group by day
            order by day desc
        ),  pin_not_setup_users as (
            -- Daily users that are at the dashboard
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
                join users u on w.id = u.wallet_id
            where
                pin = '0000'
            group by day
            order by day desc
        ), successful_deposit_users as (
            -- Daily users that have done at least one successful deposit!
            with wallets_with_transactions as (
                select
                    w.id as wallet_id
                from
                    wallets w
                    join transactions tx on tx.recipient_wallet_id = w.id
                where
                    tx.transaction_type = 'PAYMENT_GATEWAY'
                    and tx.status = 'SUCCESSFUL'
                group by w.id
            )
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
                join wallets_with_transactions wth on wth.wallet_id = w.id
            group by day
            order by day desc
        ), pending_deposit_users as (
            -- Daily users that have done at least one pending deposit!
            with wallets_with_transactions as (
                select
                    w.id as wallet_id
                from
                    wallets w
                    join transactions tx on tx.recipient_wallet_id = w.id
                where
                    tx.transaction_type = 'PAYMENT_GATEWAY'
                    and tx.status = 'PENDING'
                group by w.id
            )
            select
                date(w.created_at at time zone '+5') as day,
                count(*) as user_count
            from
                wallets w
                join wallets_with_transactions wth on wth.wallet_id = w.id
            group by day
            order by day desc
        )
        select
            tu.day,
            tu.user_count as total_users,
            pvu.user_count as phone_verified_users,
            lru.user_count as lums_registered_users,
            lvu.user_count as lums_verified_users,
            ssu.user_count as signup_success_users,
            pdu.user_count as pending_deposit_users,
            sdu.user_count as successful_deposit_users,
            round(cast(((sdu.user_count * 100)::double precision / tu.user_count::double precision) as numeric), 2) as percentage_acquisition
        from
            total_users tu
            join phone_verified_users pvu on pvu.day = tu.day
            join lums_registered_users lru on lru.day = tu.day
            join lums_verified_users lvu on lvu.day = tu.day
            join signup_success_users ssu on ssu.day = tu.day
            join pending_deposit_users pdu on pdu.day = tu.day
            join successful_deposit_users sdu on sdu.day = tu.day
    """

    uow.dict_cursor.execute(sql)
    rows = uow.dict_cursor.fetchall()

    return [pmt_vm.DailyUserCheckpoints.from_db_dict_row(r) for r in rows]


def get_many_transactions(
    tx_ids: List[str], uow: AbstractUnitOfWork
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
            txn.paypro_id,
            sender.full_name as sender_name,
            recipient.full_name as recipient_name
        from 
            transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
            right join unnest(%(tx_ids)s::uuid[]) txs(id) on txs.id = txn.id
        order by txn.created_at desc
    """

    uow.dict_cursor.execute(sql, {"tx_ids": tx_ids})
    rows = uow.dict_cursor.fetchall()

    return [pmt_vm.TransactionWithIdsDTO.from_db_dict_row(row) for row in rows]


def get_pending_pg_txs_from_ids(tx_ids: List[str], uow: AbstractUnitOfWork) -> List[str]:
    sql = """
        select
            txs.id
        from
            transactions txn
            join unnest(%(tx_ids)s::uuid[]) txs(id) on txs.id = txn.id
        where
            status = 'PENDING'::transaction_status_enum
            and transaction_type = 'PAYMENT_GATEWAY'::transaction_type_enum
    """
    uow.dict_cursor.execute(sql, {"tx_ids": tx_ids})
    rows = uow.dict_cursor.fetchall()

    return [row["id"] for row in rows]


def get_successful_pg_txs_from_ids(tx_ids: List[str], uow: AbstractUnitOfWork) -> List[str]:
    sql = """
        select
            txs.id
        from
            transactions txn
            join unnest(%(tx_ids)s::uuid[]) txs(id) on txs.id = txn.id
        where
            status = 'SUCCESSFUL'::transaction_status_enum
            and transaction_type = 'PAYMENT_GATEWAY'::transaction_type_enum
    """
    uow.dict_cursor.execute(sql, {"tx_ids": tx_ids})
    rows = uow.dict_cursor.fetchall()

    return [row["id"] for row in rows]


def get_all_deposits_to_reverse(uow: AbstractUnitOfWork) -> List[pmt_vm.TransactionWithIdsDTO]:
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
            txn.paypro_id,
            sender.full_name as sender_name,
            recipient.full_name as recipient_name
        from 
            transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
        where 
            txn.status = 'TO_REVERSE'::transaction_status_enum
            and 
            txn.transaction_type = 'PAYMENT_GATEWAY'::transaction_type_enum
        order by txn.created_at desc
        """

    uow.dict_cursor.execute(sql)

    rows = uow.dict_cursor.fetchall()

    transactions = [pmt_vm.TransactionWithIdsDTO.from_db_dict_row(row) for row in rows]

    return transactions


def get_all_failed_reversals(uow: AbstractUnitOfWork) -> List[pmt_vm.TransactionWithIdsDTO]:
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
            txn.paypro_id,
            sender.full_name as sender_name,
            recipient.full_name as recipient_name
        from 
            transactions txn
            inner join users sender on txn.sender_wallet_id = sender.id
            inner join users recipient on txn.recipient_wallet_id = recipient.id
        where 
            txn.status = 'FAILED'::transaction_status_enum
            and txn.transaction_type = 'REVERSAL'::transaction_type_enum
        order by txn.created_at desc
        """

    uow.dict_cursor.execute(sql)

    rows = uow.dict_cursor.fetchall()

    transactions = [pmt_vm.TransactionWithIdsDTO.from_db_dict_row(row) for row in rows]

    return transactions
