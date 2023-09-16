import pytest
from uuid import uuid4
from datetime import datetime
from core.payment.adapters import repository as pmt_repo
from core.payment.domain import model as pmt_model
from core.entrypoint.uow import UnitOfWork, FakeUnitOfWork


def test_transaction_repository(seed_wallet, seed_txn):
    for uow in [UnitOfWork(), FakeUnitOfWork()]:
        recipient_wallet = seed_wallet()
        sender_wallet = seed_wallet()

        uow.transactions.add_wallet(wallet=recipient_wallet)
        uow.transactions.add_wallet(wallet=sender_wallet)

        tx = seed_txn(recipient_wallet=recipient_wallet, sender_wallet=sender_wallet)

        uow.transactions.add(transaction=tx)
        repo_tx = uow.transactions.get(transaction_id=tx.id)

        assert repo_tx == tx

        tx.amount = 1000
        tx.mode = pmt_model.TransactionMode.NFC
        tx.status = pmt_model.TransactionStatus.DECLINED
        recipient_wallet = seed_wallet()
        sender_wallet = seed_wallet()

        uow.transactions.add_wallet(wallet=recipient_wallet)
        uow.transactions.add_wallet(wallet=sender_wallet)
        uow.transactions.save(transaction=tx)
        repo_tx = uow.transactions.get(transaction_id=tx.id)

        assert repo_tx == tx

        created_at = datetime.now()
        last_updated = datetime.now()
        tx_id = str(uuid4())

        repo_tx = uow.transactions.get_wallets_create_transaction(
            id=tx_id,
            amount=100,
            created_at=created_at,
            last_updated=last_updated,
            mode=pmt_model.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_model.TransactionType.P2P_PUSH,
            status=pmt_model.TransactionStatus.SUCCESSFUL,
            sender_wallet_id=sender_wallet.id,
            recipient_wallet_id=recipient_wallet.id,
        )

        tx = seed_txn(
            tx_id=tx_id,
            created_at=created_at,
            last_updated=last_updated,
            sender_wallet=sender_wallet,
            recipient_wallet=recipient_wallet,
        )

        assert repo_tx == tx

        tx_id = str(uuid4())

        tx = seed_txn(
            tx_id=tx_id,
            sender_wallet=sender_wallet,
            recipient_wallet=sender_wallet,
            transaction_type=pmt_model.TransactionType.VOUCHER,
            status=pmt_model.TransactionStatus.PENDING,
        )

        uow.transactions.add(transaction=tx)

        repo_tx = uow.transactions.get_with_different_recipient(
            transaction_id=tx_id,
            recipient_wallet_id=recipient_wallet.id,
        )

        assert repo_tx.recipient_wallet == recipient_wallet

        uow.close_connection()
