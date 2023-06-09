import pytest
from ...entrypoint.commands import (
    create_wallet,
    execute_transaction,
    accept_p2p_pull_transaction,
    decline_p2p_pull_transaction,
    redeem_voucher,
    generate_voucher,
)
from ....entrypoint.uow import FakeUnitOfWork
from ...domain.model import TransactionMode, TransactionType, TransactionStatus


def test_create_wallet():
    with FakeUnitOfWork() as uow:
        wallet = create_wallet(uow)

    assert wallet.balance == 0
    assert wallet.id in uow.transactions.wallets
    assert uow.transactions.wallets[wallet.id] == wallet


def test_execute_transaction():
    with FakeUnitOfWork() as uow:
        sender_wallet = create_wallet(uow)
        recipient_wallet = create_wallet(uow)

        # for testing purposes
        uow.transactions.add_1000_wallet(sender_wallet)

        tx = execute_transaction(
            sender_wallet_id=sender_wallet.id,
            recipient_wallet_id=recipient_wallet.id,
            amount=1000,
            transaction_mode=TransactionMode.APP_TRANSFER,
            transaction_type=TransactionType.P2P_PUSH,
            uow=uow,
        )

        fetched_tx = uow.transactions.get(transaction_id=tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.mode == TransactionMode.APP_TRANSFER
        assert fetched_tx.transaction_type == TransactionType.P2P_PUSH
        assert fetched_tx.status == TransactionStatus.SUCCESSFUL
        assert fetched_tx.sender_wallet.id == sender_wallet.id
        assert fetched_tx.recipient_wallet.id == recipient_wallet.id


def test_accept_p2p_pull_transaction():
    with FakeUnitOfWork() as uow:
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
            uow=uow,
        )

        # accept previously created pull transaction
        tx = accept_p2p_pull_transaction(transaction_id=tx.id, uow=uow)

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
    with FakeUnitOfWork() as uow:
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
            uow=uow,
        )

        # decline previously created pull transaction
        tx = decline_p2p_pull_transaction(transaction_id=tx.id, uow=uow)

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
    with FakeUnitOfWork() as uow:
        generator_wallet = create_wallet(uow)

        uow.transactions.add_1000_wallet(generator_wallet)

        tx = generate_voucher(
            sender_wallet_id=generator_wallet.id, amount=1000, uow=uow
        )

        fetched_tx = uow.transactions.get(transaction_id=tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.sender_wallet.id == generator_wallet.id
        assert fetched_tx.recipient_wallet.id == generator_wallet.id
        assert fetched_tx.mode == TransactionMode.APP_TRANSFER
        assert fetched_tx.transaction_type == TransactionType.VOUCHER
        assert fetched_tx.status == TransactionStatus.PENDING


def test_redeem_voucher():
    with FakeUnitOfWork() as uow:
        generator_wallet = create_wallet(uow)
        redeemer_wallet = create_wallet(uow)

        uow.transactions.add_1000_wallet(generator_wallet)

        tx = generate_voucher(
            sender_wallet_id=generator_wallet.id, amount=1000, uow=uow
        )

        tx = redeem_voucher(
            recipient_wallet_id=redeemer_wallet.id, transaction_id=tx.id, uow=uow
        )

        fetched_tx = uow.transactions.get(tx.id)

        assert fetched_tx.amount == 1000
        assert fetched_tx.recipient_wallet.balance == 1000
        assert fetched_tx.sender_wallet.balance == 0
        assert fetched_tx.transaction_type == TransactionType.VOUCHER
        assert fetched_tx.status == TransactionStatus.SUCCESSFUL
