from backend_ddd.entrypoint.uow import AbstractUnitOfWork
from ..domain.model import (
    Transaction,
    Wallet,
    TransactionMode,
    TransactionType,
)

# Features left:
# -> Top up vouchers
# -> Block card
# -> Balance locking for fuel


def create_wallet(uow: AbstractUnitOfWork) -> Wallet:
    """Create wallet"""
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

        tx.accept_p2p_pull_transaction()

        uow.transactions.save(tx)

    return tx


def decline_p2p_pull_transaction(
    transaction_id: str, uow: AbstractUnitOfWork
) -> Transaction:
    with uow:
        tx = uow.transactions.get(transaction_id=transaction_id)

        tx.decline_p2p_pull_transaction()

        uow.transactions.save(tx)

    return tx
