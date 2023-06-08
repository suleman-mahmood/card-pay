from ...domain.model import (
    TransactionMode,
    TransactionStatus,
    TransactionType,
    Transaction,
    Wallet,
    User,
)
from uuid import uuid4
import pytest


def behaviour():
    """
    - wallet creation
    - deposit amount in wallet
    - direct transfer to cardpay wallet using phone num
    - direct transfer to cardpay wallet using email


    # deposit
    # view
    # transfer
        # p2p
        # pos
        # virtual pos
    """


def test_wallet_is_created_after_customer_creation(seed_user_wallet):
    user, wallet = seed_user_wallet()
    user2, wallet2 = seed_user_wallet()

    # Ensure that right wallet is assigned to right user
    assert user.wallet_id == wallet.id
    assert user2.wallet_id == wallet2.id

    # Ensure that wallet ids and user ids are unique
    assert wallet.id != wallet2.id
    assert user.id != user2.id


def test_p2p_push_transaction(seed_user_wallet):
    _, wallet1 = seed_user_wallet()
    _, wallet2 = seed_user_wallet()

    wallet1.balance = 1000
    tx = Transaction(
        amount=1000,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        recipient_wallet=wallet2,
        sender_wallet=wallet1,
    )
    tx.make_transaction()

    assert wallet1.balance == 0
    assert wallet2.balance == 1000

    assert tx.status == TransactionStatus.SUCCESSFUL
    assert tx.mode == TransactionMode.APP_TRANSFER
    assert tx.transaction_type == TransactionType.P2P_PUSH

    assert tx.sender_wallet == wallet1
    assert tx.recipient_wallet == wallet2

    assert tx.status == TransactionStatus.SUCCESSFUL


def test_initaite_deposit(seed_user_wallet, seed_wallet):
    _, wallet = seed_user_wallet()
    pg_wallet = seed_wallet()

    pg_wallet.balance = 1000000

    tx = Transaction(
        amount=1000,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.PAYMENT_GATEWAY,
        recipient_wallet=wallet,
        sender_wallet=pg_wallet,
    )
    tx.make_transaction()

    assert wallet.balance == 0
    assert pg_wallet.balance == 1000000 - 1000

    assert tx.status == TransactionStatus.PENDING
    assert tx.mode == TransactionMode.APP_TRANSFER
    assert tx.transaction_type == TransactionType.PAYMENT_GATEWAY
    assert tx.amount == 1000

    assert tx.sender_wallet == pg_wallet
    assert tx.recipient_wallet == wallet


def test_pos_transaction(seed_user_wallet):
    _, customer_wallet = seed_user_wallet()
    _, vendor_wallet = seed_user_wallet()

    customer_wallet.balance = 1000
    tx = Transaction(
        amount=1000,
        mode=TransactionMode.QR,
        transaction_type=TransactionType.POS,
        recipient_wallet=vendor_wallet,
        sender_wallet=customer_wallet,
    )
    tx.make_transaction()

    assert customer_wallet.balance == 0
    assert vendor_wallet.balance == 1000

    assert tx.status == TransactionStatus.SUCCESSFUL
    assert tx.mode == TransactionMode.QR
    assert tx.transaction_type == TransactionType.POS

    assert tx.sender_wallet == customer_wallet
    assert tx.recipient_wallet == vendor_wallet

    assert tx.status == TransactionStatus.SUCCESSFUL


def test_p2p_pull_transaction(seed_user_wallet):
    """consider adding request feature if a transaction has been made previously"""
    _, wallet1 = seed_user_wallet()
    _, wallet2 = seed_user_wallet()

    # Wallet1 requesting 1000 from wallet 2
    wallet2.balance = 1000
    tx = Transaction(
        amount=1000,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PULL,
        recipient_wallet=wallet1,
        sender_wallet=wallet2,
    )

    # Initiate transaction
    assert wallet1.balance == 0
    assert wallet2.balance == 1000

    assert tx.status == TransactionStatus.PENDING
    assert tx.mode == TransactionMode.APP_TRANSFER
    assert tx.transaction_type == TransactionType.P2P_PULL

    assert tx.sender_wallet == wallet1
    assert tx.recipient_wallet == wallet2

    # Complete transaction
    tx.accept_p2p_pull_transaction()

    assert wallet1.balance == 1000
    assert wallet2.balance == 0
    assert tx.status == TransactionStatus.SUCCESSFUL
