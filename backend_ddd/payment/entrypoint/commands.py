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
from ...payment.domain.model import TransactionType, TransactionMode
from time import sleep
from queue import Queue
from uuid import uuid4
# Features left:
# -> Balance locking for fuel

CARD_PAY_WALLET_ID = "d8f32ce7-1136-421e-bab2-68a94ac183e4"


def create_wallet(uow: AbstractUnitOfWork) -> Wallet:
    """Create wallet"""
    # please only call this from create_user
    wallet = Wallet()
    uow.transactions.add_wallet(wallet)

    return wallet


def execute_cashback_transaction(
    sender_wallet_id: str,
    recipient_wallet_id: str,
    amount: int,
    uow: AbstractUnitOfWork,
) -> Transaction:
    # using wallet id as txn does not exist yet
    tx = uow.transactions.get_wallets_create_transaction(
        amount=amount,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.CASH_BACK,
        sender_wallet_id=sender_wallet_id,
        recipient_wallet_id=recipient_wallet_id,
    )
    tx.execute_transaction()
    uow.transactions.save(tx)
    return tx

def _add_loyalty_points(
    wallet_id: str,
    transaction_amount: int,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
):

    loyalty_points_recipient = marketing_queries.get_user_id_from_wallet_id(
        wallet_id=wallet_id,
        uow=uow
    )
    # adding loyalty points
    marketing_commands.add_loyalty_points(
        user_id= loyalty_points_recipient,
        transaction_amount=transaction_amount,
        transaction_type=transaction_type,
        uow=uow,
    )
    
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


        if transaction_type != TransactionType.P2P_PULL:
            tx.execute_transaction()

            # selecting loyalty points recipient based on transaction type
            if transaction_type == TransactionType.P2P_PUSH:
                _add_loyalty_points(
                    wallet_id=sender_wallet_id,
                    transaction_amount=amount,
                    transaction_type= transaction_type,
                    uow=uow)
            elif transaction_type == TransactionType.PAYMENT_GATEWAY:
                _add_loyalty_points(
                    wallet_id=recipient_wallet_id,
                    transaction_amount=amount,
                    transaction_type= transaction_type,
                    uow=uow)

        uow.transactions.save(tx)

        # giving cashback
        if transaction_type == TransactionType.PAYMENT_GATEWAY:
            # UNCOMMENT FOR MARKETING TESTS
            # card_pay_wallet = create_wallet(uow)
            # uow.transactions.add_1000_wallet(card_pay_wallet)

            marketing_commands.give_cashback(
                sender_wallet_id= CARD_PAY_WALLET_ID,
                recipient_wallet_id=recipient_wallet_id,
                deposited_amount=amount,
                uow=uow
            )

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
        tx.accept_p2p_pull_transaction()


        _add_loyalty_points(
            wallet_id=wallet_id,
            transaction_amount=amount,
            transaction_type= TransactionType.P2P_PULL,
            uow=uow)

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
