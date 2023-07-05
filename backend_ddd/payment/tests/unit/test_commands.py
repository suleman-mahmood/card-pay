import pytest
from ...entrypoint.commands import (
    create_wallet,
    execute_transaction,
    accept_p2p_pull_transaction,
    decline_p2p_pull_transaction,
    redeem_voucher,
    generate_voucher,
    slow_execute_transaction,
)
from ...entrypoint.queries import get_wallet_from_wallet_id
from ....authentication.tests.conftest import seed_verified_auth_user
from ....entrypoint.uow import FakeUnitOfWork, UnitOfWork
from ...domain.model import TransactionMode, TransactionType, TransactionStatus
import threading
from queue import Queue


def test_create_wallet():
    with UnitOfWork() as uow:
        wallet = create_wallet(uow)

    assert wallet.balance == 0


def test_execute_transaction(seed_verified_auth_user):
    uow = UnitOfWork()
    sender = seed_verified_auth_user(uow)
    recipient = seed_verified_auth_user(uow)

    with uow:
        sender_wallet = get_wallet_from_wallet_id(wallet_id=sender.wallet_id, uow=uow)
        recipient_wallet = get_wallet_from_wallet_id(wallet_id=recipient.wallet_id, uow=uow)
        # for testing purposes
        uow.transactions.add_1000_wallet(sender_wallet)

    tx = execute_transaction(
        sender_wallet_id=sender_wallet.id,
        recipient_wallet_id=recipient_wallet.id,
        amount=1000,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        uow=UnitOfWork(),
    )

    with UnitOfWork() as uow:
        fetched_tx = uow.transactions.get(transaction_id=tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.mode == TransactionMode.APP_TRANSFER
        assert fetched_tx.transaction_type == TransactionType.P2P_PUSH
        assert fetched_tx.status == TransactionStatus.SUCCESSFUL
        assert fetched_tx.sender_wallet.id == sender_wallet.id
        assert fetched_tx.recipient_wallet.id == recipient_wallet.id


def test_slow_execute_transaction():
    with UnitOfWork() as uow:
        sender_wallet = create_wallet(uow)

        # recipient_wallet = create_wallet(uow)

        recipient_wallets = [create_wallet(uow) for i in range(5)]

        # for testing purposes
        uow.transactions.add_1000_wallet(sender_wallet)

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

    with UnitOfWork() as uow:
        for i in range(5):
            fetched_tx = uow.transactions.get(transaction_id=txs[i].id)

            assert fetched_tx.amount == 100
            assert fetched_tx.mode == TransactionMode.APP_TRANSFER
            assert fetched_tx.transaction_type == TransactionType.P2P_PUSH
            assert fetched_tx.status == TransactionStatus.SUCCESSFUL
            assert fetched_tx.sender_wallet.id == sender_wallet.id
            # assert fetched_tx.recipient_wallet.id == recipient_wallets[i].id

        sender_wallet = uow.transactions.get(transaction_id=txs[0].id).sender_wallet
        assert sender_wallet.balance == 500


def test_accept_p2p_pull_transaction():
    with UnitOfWork() as uow:
        sender_wallet = create_wallet(uow)
        recipient_wallet = create_wallet(uow)

        # for testing purposes
        uow.transactions.add_1000_wallet(sender_wallet)

        # make pull transaction
    tx = execute_transaction(
        sender_wallet_id=sender_wallet.id,
        recipient_wallet_id=recipient_wallet.id,
        amount=1000,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PULL,
        uow=UnitOfWork(),
    )

    # accept previously created pull transaction
    tx = accept_p2p_pull_transaction(transaction_id=tx.id, uow=UnitOfWork())

    with UnitOfWork() as uow:
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


def test_decline_p2p_pull_transaction():
    with UnitOfWork() as uow:
        sender_wallet = create_wallet(uow)
        recipient_wallet = create_wallet(uow)

        # for testing purposes
        uow.transactions.add_1000_wallet(sender_wallet)

    # make pull transaction
    tx = execute_transaction(
        sender_wallet_id=sender_wallet.id,
        recipient_wallet_id=recipient_wallet.id,
        amount=1000,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PULL,
        uow=UnitOfWork(),
    )

    # decline previously created pull transaction
    tx = decline_p2p_pull_transaction(transaction_id=tx.id, uow=UnitOfWork())

    with UnitOfWork() as uow:
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
    with UnitOfWork() as uow:
        generator_wallet = create_wallet(uow)

        uow.transactions.add_1000_wallet(generator_wallet)

    tx = generate_voucher(
        sender_wallet_id=generator_wallet.id, amount=1000, uow=UnitOfWork()
    )

    with UnitOfWork() as uow:
        fetched_tx = uow.transactions.get(transaction_id=tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.sender_wallet.id == generator_wallet.id
        assert fetched_tx.recipient_wallet.id == generator_wallet.id
        assert fetched_tx.mode == TransactionMode.APP_TRANSFER
        assert fetched_tx.transaction_type == TransactionType.VOUCHER
        assert fetched_tx.status == TransactionStatus.PENDING


def test_redeem_voucher():
    with UnitOfWork() as uow:
        generator_wallet = create_wallet(uow)
        redeemer_wallet = create_wallet(uow)

        uow.transactions.add_1000_wallet(generator_wallet)

    tx = generate_voucher(
        sender_wallet_id=generator_wallet.id, amount=1000, uow=UnitOfWork()
    )

    tx = redeem_voucher(
        recipient_wallet_id=redeemer_wallet.id, transaction_id=tx.id, uow=UnitOfWork()
    )

    with UnitOfWork() as uow:
        fetched_tx = uow.transactions.get(tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.recipient_wallet.balance == 1000
        assert fetched_tx.sender_wallet.balance == 0
        assert fetched_tx.transaction_type == TransactionType.VOUCHER
        assert fetched_tx.status == TransactionStatus.SUCCESSFUL
