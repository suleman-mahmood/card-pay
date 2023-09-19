import pytest
from uuid import uuid4
from core.payment.domain import model as pmt_mdl
from datetime import datetime


@pytest.fixture
def seed_wallet():
    def _seed_wallet() -> pmt_mdl.Wallet:
        return pmt_mdl.Wallet(id=str(uuid4()), qr_id=str(uuid4()), balance=0)

    return _seed_wallet


@pytest.fixture
def seed_txn(seed_wallet):
    def _seed_txn(
        tx_id=str(uuid4()),
        amount=100,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
        status=pmt_mdl.TransactionStatus.SUCCESSFUL,
        recipient_wallet=seed_wallet(),
        sender_wallet=seed_wallet(),
    ) -> pmt_mdl.Transaction:
        return pmt_mdl.Transaction(
            id=tx_id,
            amount=amount,
            created_at=created_at,
            last_updated=last_updated,
            mode=mode,
            transaction_type=transaction_type,
            status=status,
            recipient_wallet=recipient_wallet,
            sender_wallet=sender_wallet,
        )

    return _seed_txn
