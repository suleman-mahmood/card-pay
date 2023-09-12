import threading
import multiprocessing as mp
from time import sleep
from ...entrypoint.commands import (
    create_wallet,
    execute_transaction,
    accept_p2p_pull_transaction,
    decline_p2p_pull_transaction,
    redeem_voucher,
    generate_voucher,
    slow_execute_transaction,
    _get_paypro_auth_token,
    get_deposit_checkout_url,
    execute_qr_transaction,
    payment_retools_reconcile_vendor,
)
from ....marketing.entrypoint import commands as marketing_commands
from ....authentication.tests.conftest import (
    seed_auth_user,
    seed_verified_auth_user,
    seed_auth_vendor,
    seed_verified_auth_vendor,
    seed_auth_cardpay,
    seed_verified_auth_cardpay,
)
from ....entrypoint.uow import UnitOfWork, AbstractUnitOfWork
from ...domain.model import (
    TransactionMode,
    TransactionType,
    TransactionStatus,
    Transaction,
)
from queue import Queue
from uuid import uuid4
import pytest
from core.authentication.entrypoint import queries as auth_queries
from core.payment.entrypoint import exceptions as pmt_cmd_ex
from core.payment.domain import model as pmt_mdl

def _get_wallet_from_wallet_id(wallet_id: str, uow: AbstractUnitOfWork):
    sql = """
        select id, balance, qr_id
        from wallets
        where id = %s
    """
    uow.cursor.execute(sql, [wallet_id])
    row = uow.cursor.fetchone()
    return pmt_mdl.Wallet(
        id=row[0],
        balance=row[1],
        qr_id=row[2],
    )

def test_slow_execute_transaction():
    uow = UnitOfWork()

    with uow:
        sender_wallet = create_wallet(user_id=str(uuid4()), uow=uow)
        recipient_wallets = [
            create_wallet(user_id=str(uuid4()), uow=uow) for i in range(5)
        ]

        # for testing purposes
        uow.transactions.add_1000_wallet(wallet_id=sender_wallet.id)

    uow.commit_close_connection()

    threads = []
    queue = Queue()
    for i in range(5):
        t = threading.Thread(
            target=slow_execute_transaction,
            args=(
                sender_wallet.id,
                recipient_wallets[i].id,
                100,
                TransactionMode.APP_TRANSFER,
                TransactionType.P2P_PUSH,
                UnitOfWork(),
                queue,
            ),
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    txs = []
    for i in range(5):
        x = queue.get()
        txs.append(x)

    uow = UnitOfWork()
    with uow:
        for i in range(5):
            fetched_tx = uow.transactions.get(transaction_id=txs[i].id)

            assert fetched_tx.amount == 100
            assert fetched_tx.mode == TransactionMode.APP_TRANSFER
            assert fetched_tx.transaction_type == TransactionType.P2P_PUSH
            assert fetched_tx.status == TransactionStatus.SUCCESSFUL
            assert fetched_tx.sender_wallet.id == sender_wallet.id
            # assert fetched_tx.recipient_wallet.id == recipient_wallets[i].id

        sender_wallet = uow.transactions.get(
            transaction_id=txs[0].id).sender_wallet
        assert sender_wallet.balance == 500

    uow.commit_close_connection()


def test_accept_p2p_pull_transaction(seed_verified_auth_user):
    uow = UnitOfWork()
    sender = seed_verified_auth_user(uow)
    recipient = seed_verified_auth_user(uow)
    marketing_commands.add_weightage(
        weightage_type="P2P_PULL",
        weightage_value=10,
        uow=uow,
    )

    sender_wallet = _get_wallet_from_wallet_id(
        wallet_id=sender.wallet_id, uow=uow)
    recipient_wallet = _get_wallet_from_wallet_id(
        wallet_id=recipient.wallet_id, uow=uow)

    with uow:
        # for testing purposes
        uow.transactions.add_1000_wallet(wallet_id=sender_wallet.id)

        # make pull transaction
    tx = execute_transaction(
        sender_wallet_id=sender_wallet.id,
        recipient_wallet_id=recipient_wallet.id,
        amount=1000,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PULL,
        uow=uow,
    )

    # accept previously created pull transaction
    tx = accept_p2p_pull_transaction(transaction_id=tx.id, uow=uow)

    with uow:
        # fetch tx from memory
        fetched_tx = uow.transactions.get(transaction_id=tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.mode == TransactionMode.APP_TRANSFER
        assert fetched_tx.transaction_type == TransactionType.P2P_PULL
        assert fetched_tx.status == TransactionStatus.SUCCESSFUL
        assert fetched_tx.sender_wallet.id == sender_wallet.id
        assert fetched_tx.recipient_wallet.id == recipient_wallet.id
        assert fetched_tx.recipient_wallet.balance == 1000
        assert fetched_tx.sender_wallet.balance == 0


def test_decline_p2p_pull_transaction(mocker):
    uow = UnitOfWork()

    with uow:
        sender_wallet = create_wallet(user_id=str(uuid4()), uow=uow)
        recipient_wallet = create_wallet(user_id=str(uuid4()), uow=uow)

        # for testing purposes
        uow.transactions.add_1000_wallet(wallet_id=sender_wallet.id)

    # make pull transaction
    mocker.patch(
        "core.authentication.entrypoint.queries.user_verification_status_from_user_id",
        return_value=True,
    )
    tx = execute_transaction(
        sender_wallet_id=sender_wallet.id,
        recipient_wallet_id=recipient_wallet.id,
        amount=1000,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PULL,
        uow=uow,
    )

    # decline previously created pull transaction
    tx = decline_p2p_pull_transaction(transaction_id=tx.id, uow=uow)

    with uow:
        # fetch tx from memory
        fetched_tx = uow.transactions.get(transaction_id=tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.mode == TransactionMode.APP_TRANSFER
        assert fetched_tx.transaction_type == TransactionType.P2P_PULL
        assert fetched_tx.status == TransactionStatus.DECLINED
        assert fetched_tx.sender_wallet.id == sender_wallet.id
        assert fetched_tx.recipient_wallet.id == recipient_wallet.id
        assert fetched_tx.recipient_wallet.balance == 0
        assert fetched_tx.sender_wallet.balance == 1000


def test_generate_voucher():
    uow = UnitOfWork()

    with uow:
        generator_wallet = create_wallet(user_id=str(uuid4()), uow=uow)

        uow.transactions.add_1000_wallet(wallet_id=generator_wallet.id)

    tx = generate_voucher(
        sender_wallet_id=generator_wallet.id, amount=1000, uow=uow)

    with uow:
        fetched_tx = uow.transactions.get(transaction_id=tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.sender_wallet.id == generator_wallet.id
        assert fetched_tx.recipient_wallet.id == generator_wallet.id
        assert fetched_tx.mode == TransactionMode.APP_TRANSFER
        assert fetched_tx.transaction_type == TransactionType.VOUCHER
        assert fetched_tx.status == TransactionStatus.PENDING


def test_redeem_voucher():
    uow = UnitOfWork()

    with uow:
        generator_wallet = create_wallet(user_id=str(uuid4()), uow=uow)
        redeemer_wallet = create_wallet(user_id=str(uuid4()), uow=uow)

        uow.transactions.add_1000_wallet(wallet_id=generator_wallet.id)

    tx = generate_voucher(
        sender_wallet_id=generator_wallet.id, amount=1000, uow=uow)

    tx = redeem_voucher(
        recipient_wallet_id=redeemer_wallet.id, transaction_id=tx.id, uow=uow
    )

    with uow:
        fetched_tx = uow.transactions.get(tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.recipient_wallet.balance == 1000
        assert fetched_tx.sender_wallet.balance == 0
        assert fetched_tx.transaction_type == TransactionType.VOUCHER
        assert fetched_tx.status == TransactionStatus.SUCCESSFUL


# Keep these commented, only for testing at certain times

# def test_get_paypro_token():
#     uow = UnitOfWork()

#     token = _get_paypro_auth_token(uow=uow)
#     sleep(1)
#     token_2 = _get_paypro_auth_token(uow=uow)

#     assert token == token_2


# def test_get_deposit_checkout_url():
#    uow = UnitOfWork()

#    payment_url = get_deposit_checkout_url(
#        amount=500,
#        transaction_id=str(uuid4()),
#        email="test@tdd.com",
#        full_name="TDD test case",
#        phone_number="03333333333",
#        uow=uow,
#    )

#    assert payment_url is not None


def test_execute_qr_transaction(seed_verified_auth_vendor, seed_verified_auth_user):
    uow = UnitOfWork()
    sender_customer = seed_verified_auth_user(uow)
    vendor = seed_verified_auth_vendor(uow)

    marketing_commands.add_and_set_missing_weightages_to_zero(uow=uow)

    uow.transactions.add_1000_wallet(wallet_id=sender_customer.wallet_id)
    vendor_wallet = _get_wallet_from_wallet_id(
        wallet_id=vendor.wallet_id, uow=uow
    )

    #test qr txn to invalid qr version
    with pytest.raises(
        payment_exc.InvalidQRVersionException, match="Invalid QR version"
    ):
        tx = execute_qr_transaction(
            sender_wallet_id=sender_customer.wallet_id,
            recipient_qr_id=vendor_wallet.qr_id,
            amount=400,
            version=0,
            uow=uow,
        )

    # test qr txn to invalid qr_id

    with pytest.raises(
        pmt_cmd_ex.InvalidQRCodeException, match="Invalid QR code"
    ):
        tx = execute_qr_transaction(
            sender_wallet_id=sender_customer.wallet_id,
            recipient_qr_id=str(uuid4()),
            version=1,
            amount=400,
            uow=uow,
        )

    # test qr txn to vendor from customer
    tx = execute_qr_transaction(
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=vendor_wallet.qr_id,
        amount=400,
        version=1,
        uow=uow,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx.id)
    assert fetched_tx == tx

    # test insufficient balance
    with pytest.raises(
        pmt_cmd_ex.TransactionFailedException, match="Insufficient balance in sender's wallet"
    ):
        tx = execute_qr_transaction(
            sender_wallet_id=sender_customer.wallet_id,
            recipient_qr_id=vendor_wallet.qr_id,
            amount=601,
            version=1,
            uow=uow,
        )

    # test p2p qr txn
    recipient_customer = seed_verified_auth_user(uow)
    recipient_customer_wallet = _get_wallet_from_wallet_id(
        wallet_id=recipient_customer.wallet_id, uow=uow
    )

    tx = execute_qr_transaction(
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=recipient_customer_wallet.qr_id,
        amount=500,
        version=1,
        uow=uow,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx.id)
    assert fetched_tx == tx


    uow.close_connection()


def test_reconcile_vendor(seed_verified_auth_user, seed_verified_auth_vendor, seed_verified_auth_cardpay):

    uow = UnitOfWork()
    sender_customer = seed_verified_auth_user(uow)
    recipient_vendor = seed_verified_auth_vendor(uow)
    cardpay = seed_verified_auth_cardpay(uow)

    marketing_commands.add_and_set_missing_weightages_to_zero(uow=uow)

    uow.transactions.add_1000_wallet(wallet_id=sender_customer.wallet_id)
    vendor_wallet = _get_wallet_from_wallet_id(
        wallet_id=recipient_vendor.wallet_id, uow=uow
    )

    execute_qr_transaction(
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=vendor_wallet.qr_id,
        amount=400,
        version=1,
        uow=uow,
    )
    execute_qr_transaction(
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=vendor_wallet.qr_id,
        amount=200,
        version=1,
        uow=uow,
    )

    assert auth_queries.get_user_balance(
        user_id=sender_customer.id, uow=uow) == 400
    assert auth_queries.get_user_balance(
        user_id=recipient_vendor.id, uow=uow) == 600
    assert auth_queries.get_user_balance(
        user_id=cardpay.id, uow=uow) == 0

    # test reconciliation
    payment_retools_reconcile_vendor(
        vendor_wallet_id=vendor_wallet.id,
        uow=uow,
    )

    assert auth_queries.get_user_balance(
        user_id=recipient_vendor.id, uow=uow) == 0
    assert auth_queries.get_user_balance(
        user_id=cardpay.id, uow=uow) == 600

    # test reconciliation with zero balance
    with pytest.raises(
        pmt_cmd_ex.TransactionFailedException, match="Amount is zero or negative"
    ):
        payment_retools_reconcile_vendor(
            vendor_wallet_id=vendor_wallet.id,
            uow=uow,
        )

    uow.close_connection()

def _get_latest_failed_txn_of_user(user_id: str, uow: AbstractUnitOfWork):
    with uow:
        sql = """
            select id from transactions txn
            where (sender_wallet_id = %s or recipient_wallet_id = %s)
            and status = 'FAILED'::transaction_status_enum
            order by created_at desc
        """
        uow.cursor.execute(sql, [user_id,user_id])
        rows = uow.cursor.fetchone()

        return uow.transactions.get(transaction_id=rows[0])

def test_failing_txn(seed_verified_auth_user):
    
    uow = UnitOfWork()
    user_1 = seed_verified_auth_user(uow)
    user_2 = seed_verified_auth_user(uow)

    with pytest.raises(pmt_cmd_ex.TransactionFailedException):
        tx = execute_transaction(
            sender_wallet_id=user_1.id,
            recipient_wallet_id=user_2.id,
            amount=1000,
            transaction_mode=TransactionMode.APP_TRANSFER,
            transaction_type=TransactionType.P2P_PUSH,
            uow=uow,
        )

    fetched_failed_tx = _get_latest_failed_txn_of_user(user_id=user_1.id, uow=uow)
    assert fetched_failed_tx.amount == 1000
    assert fetched_failed_tx.status == TransactionStatus.FAILED
    uow.close_connection()
    