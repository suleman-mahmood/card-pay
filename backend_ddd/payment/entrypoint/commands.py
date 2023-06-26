"""Payments micro-service commands"""
from backend_ddd.entrypoint.uow import AbstractUnitOfWork
from ..domain.model import (
    Transaction,
    Wallet,
    TransactionMode,
    TransactionType,
)
from ...marketing.entrypoint import commands as marketing_commands
from ...marketing.entrypoint import queries as marketing_queries
from time import sleep
from queue import Queue

# Features left:
# -> Balance locking for fuel


def create_wallet(uow: AbstractUnitOfWork) -> Wallet:
    """Create wallet"""
    # please only call this from create_user
    wallet = Wallet()
    uow.transactions.add_wallet(wallet)

    return wallet


def execute_transaction(
    sender_wallet_id: str,
    recipient_wallet_id: str,
    amount: int,
    transaction_mode: TransactionMode,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
) -> Transaction:
    with uow:
        # using wallet id as txn does not exist yet
        tx = uow.transactions.get_wallets_create_transaction(
            amount=amount,
            mode=transaction_mode,
            transaction_type=transaction_type,
            sender_wallet_id=sender_wallet_id,
            recipient_wallet_id=recipient_wallet_id,
        )

        user_id = marketing_queries.get_user_id_from_wallet_id(
            wallet_id=sender_wallet_id,
            uow=uow
        )

        if transaction_type != TransactionType.P2P_PULL:
            tx.execute_transaction()

        # Give Loyalty Points

        if transaction_type == TransactionType.P2P_PUSH:
            marketing_commands.add_loyalty_points_for_push_transaction(
                user_id= user_id,
                transaction_amount= amount,
                uow= uow,
            )


        if transaction_type == TransactionType.PAYMENT_GATEWAY:
            marketing_commands.give_cashback(
                recipient_wallet_id=sender_wallet_id,
                deposited_amount=amount,
                uow= uow
            )
            marketing_commands.add_loyalty_points_for_deposit(
                user_id= user_id,
                transaction_amount= amount,
                uow= uow,
            )
            
        uow.transactions.save(tx)

    return tx


# for testing purposes only
def slow_execute_transaction(
    sender_wallet_id: str,
    recipient_wallet_id: str,
    amount: int,
    transaction_mode: TransactionMode,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
    queue: Queue,
):
    with uow:
        # using wallet id as txn does not exist yet
        tx = uow.transactions.get_wallets_create_transaction(
            amount=amount,
            mode=transaction_mode,
            transaction_type=transaction_type,
            sender_wallet_id=sender_wallet_id,
            recipient_wallet_id=recipient_wallet_id,
        )
        sleep(1)
        if transaction_type != TransactionType.P2P_PULL:
            tx.execute_transaction()

        uow.transactions.save(tx)

    queue.put(tx)


def accept_p2p_pull_transaction(
    transaction_id: str, uow: AbstractUnitOfWork
) -> Transaction:
    with uow:
        tx = uow.transactions.get(transaction_id=transaction_id)
        user_id = marketing_queries.get_user_id_from_wallet_id(
            wallet_id=tx.sender_wallet.id,
            uow=uow,
        )

        tx.accept_p2p_pull_transaction()
        marketing_commands.add_loyalty_points_for_pull_transaction(
            user_id= user_id,
            transaction_amount= tx.amount,
            uow= uow,
        )
        
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


def generate_voucher(
    sender_wallet_id: str, amount: int, uow: AbstractUnitOfWork
) -> Transaction:
    """creates a txn object whith same sender and recipient"""
    with uow:
        tx = uow.transactions.get_wallets_create_transaction(
            amount=amount,
            mode=TransactionMode.APP_TRANSFER,
            transaction_type=TransactionType.VOUCHER,
            sender_wallet_id=sender_wallet_id,
            recipient_wallet_id=sender_wallet_id,
        )

        uow.transactions.save(tx)

    return tx


# transaction_id ~= voucher_id
def redeem_voucher(
    recipient_wallet_id: str, transaction_id: str, uow: AbstractUnitOfWork
) -> Transaction:
    with uow:
        tx = uow.transactions.get_with_different_recipient(
            transaction_id=transaction_id, recipient_wallet_id=recipient_wallet_id
        )
        tx.redeem_voucher()
        uow.transactions.save(tx)

    return tx
