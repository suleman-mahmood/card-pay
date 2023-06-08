from ...domain.model import TransactionMode, TransactionStatus, TransactionType
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

    assert user.wallet == wallet
    assert user2.wallet == wallet2
    assert wallet.id != wallet2.id
    assert user.id != user2.id


def test_initaite_deposit(seed_user_wallet, seed_payment_gateway):
    user, wallet = seed_user_wallet()
    payment_gateway_name, payment_gateway_id = seed_payment_gateway

    wallet.initiate_deposit(amount=1000, payment_gateway_id=payment_gateway_id)

    assert len(wallet.transactions[0]) == 1
    assert wallet.transactions[0].amount == 10000
    assert wallet.transactions[0].mode == TransactionMode.APP_TRANSFER
    assert wallet.transactions[0].transaction_type == TransactionType.PAYMENT_GATEWAY
    assert wallet.transactions[0].status == TransactionStatus.PENDING
    assert wallet.transactions[0].sender_id == payment_gateway_id
    assert user.wallet_id == wallet.transactions[0].recipient_id
    assert wallet.balance == 0


def test_p2p_push_transaction(seed_user_wallet):
    user1, wallet1 = seed_user_wallet()
    user2, wallet2 = seed_user_wallet()

    wallet1.balance = 1000
    user1.make_transaction(
        recipient_id=wallet2.id,
        amount=1000,
        mode=TransactionMode.APP_TRANSFER,
        type=TransactionType.P2P_PUSH,
    )
    transaction = wallet1.transactions[0]

    assert wallet1.balance == 0
    assert wallet2.balance == 1000
    assert wallet1.transactions[0] == wallet2.transactions[0]
    assert transaction.recipient_id == wallet2.id
    assert transaction.sender_id == wallet1.id
    assert transaction.mode == TransactionMode.APP_TRANSFER
    assert transaction.transaction_type == TransactionType.P2P_PUSH
    assert transaction.status == TransactionStatus.SUCCESSFUL


def test_initiate_p2p_pull_transaction(seed_user_wallet):
    """consider adding request feature if a transaction has been made previously"""
    user1, wallet1 = seed_user_wallet()
    user2, wallet2 = seed_user_wallet()

    wallet1.initiate_p2p_pull_transaction(recipient_id=user2.id, amount=1000)
    transaction = wallet1.transactions[0]

    assert wallet1.transactions[0] == wallet2.transactions[0]
    assert transaction.recipient_id == user2.id
    assert transaction.sender_id == user1.id
    assert wallet2.transactions[0].mode == TransactionMode.APP_TRANSFER
    assert wallet2.transactions[0].transaction_type == TransactionType.P2P_PULL
    assert transaction.status == TransactionStatus.PENDING


def test_pos_transaction(seed_user_wallet):
    customer, customer_wallet = seed_user_wallet()
    vendor, vendor_wallet = seed_user_wallet()

    customer.wallet.balance = 1000
    customer.make_transaction(
        recipient_id=vendor_wallet.id,
        amount=1000,
        mode=TransactionMode.QR,
        type=TransactionType.POS,
    )
    transaction = customer.wallet.transactions[0]

    assert customer_wallet.balance == 0
    assert vendor_wallet.balance == 1000
    assert customer_wallet.transactions[0] == vendor_wallet.transactions[0]
    assert transaction.recipient_id == vendor_wallet.id
    assert transaction.sender_id == customer_wallet.id
    assert transaction.mode == TransactionMode.APP_TRANSFER
    assert transaction.transaction_type == TransactionType.P2P_PUSH
    assert transaction.status == TransactionStatus.SUCCESSFUL
