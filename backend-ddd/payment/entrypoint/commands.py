from ..domain.model import (
    Transaction,
    Wallet,
    User,
    TransactionMode,
    TransactionType,
    TransactionStatus,
)
from ..entrypoint.uow import AbstractUnitOfWork


def create_wallet(uow: AbstractUnitOfWork) -> Wallet:
    """Create wallet for the user"""
    wallet = Wallet()

    with uow:
        uow.transactions.add_wallet(wallet)

    return wallet


def make_transaction(
    sender_wallet_id: str,
    recipient_wallet_id: str,
    amount: int,
    transaction_mode: TransactionMode,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
) -> Transaction:
    with uow:
        # using wallet id as txn does not exist yet
        tx = uow.transactions.get_by_wallet_ids(
            amount=amount,
            mode=transaction_mode,
            transaction_type=transaction_type,
            sender_wallet_id=sender_wallet_id,
            recipient_wallet_id=recipient_wallet_id,
        )

        if transaction_type != TransactionType.P2P_PULL:
            tx.make_transaction()

        uow.transactions.save(tx)

    return tx


def accept_p2p_pull_transaction(
    transaction_id: str, uow: AbstractUnitOfWork
) -> Transaction:
    with uow:
        tx = uow.transactions.get(transaction_id=transaction_id)

        tx.make_transaction()

        uow.transactions.save(tx)

    return tx
