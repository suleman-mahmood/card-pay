from ...domain.model import (
    TransactionMode,
    TransactionStatus,
    TransactionType,
    Transaction,
)
from uuid import uuid4
import pytest
from ...domain.exceptions import TransactionNotAllowedException


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


def test_wallet_is_unique(seed_wallet):
    wallet = seed_wallet()
    wallet2 = seed_wallet()

    # Ensure that wallet ids and user ids are unique
    assert wallet.id != wallet2.id


def test_p2p_push_transaction(seed_wallet):
    wallet1 = seed_wallet()
    wallet2 = seed_wallet()

    wallet1.balance = 1000
    tx = Transaction(
        amount=1000,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        recipient_wallet=wallet2,
        sender_wallet=wallet1,
    )
    tx.execute_transaction()

    assert tx.sender_wallet.balance == 0
    assert tx.recipient_wallet.balance == 1000

    assert tx.status == TransactionStatus.SUCCESSFUL
    assert tx.mode == TransactionMode.APP_TRANSFER
    assert tx.transaction_type == TransactionType.P2P_PUSH

    assert tx.sender_wallet == tx.sender_wallet
    assert tx.recipient_wallet == tx.recipient_wallet

    assert tx.status == TransactionStatus.SUCCESSFUL


def test_initiate_deposit(seed_wallet):
    wallet = seed_wallet()
    pg_wallet = seed_wallet()

    pg_wallet.balance = 1000000

    tx = Transaction(
        amount=1000,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.PAYMENT_GATEWAY,
        recipient_wallet=wallet,
        sender_wallet=pg_wallet,
    )
            
    tx.execute_transaction()

    assert tx.recipient_wallet.balance == 1000
    assert tx.sender_wallet.balance == 1000000 - 1000

    assert tx.status == TransactionStatus.SUCCESSFUL
    assert tx.mode == TransactionMode.APP_TRANSFER
    assert tx.transaction_type == TransactionType.PAYMENT_GATEWAY
    assert tx.amount == 1000


def test_pos_transaction(seed_wallet):
    customer_wallet = seed_wallet()
    vendor_wallet = seed_wallet()

    customer_wallet.balance = 1000
    tx = Transaction(
        amount=1000,
        mode=TransactionMode.QR,
        transaction_type=TransactionType.POS,
        recipient_wallet=vendor_wallet,
        sender_wallet=customer_wallet,
    )
    tx.execute_transaction()

    assert customer_wallet.balance == 0
    assert vendor_wallet.balance == 1000

    assert tx.status == TransactionStatus.SUCCESSFUL
    assert tx.mode == TransactionMode.QR
    assert tx.transaction_type == TransactionType.POS

    assert tx.status == TransactionStatus.SUCCESSFUL


def test_accept_p2p_pull_transaction(seed_wallet):
    """consider adding request feature if a transaction has been made previously"""
    wallet1 = seed_wallet()
    wallet2 = seed_wallet()

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
    assert tx.recipient_wallet.balance == 0
    assert tx.sender_wallet.balance == 1000

    assert tx.status == TransactionStatus.PENDING
    assert tx.mode == TransactionMode.APP_TRANSFER
    assert tx.transaction_type == TransactionType.P2P_PULL

    # Complete transaction
    tx.accept_p2p_pull_transaction()

    assert tx.recipient_wallet.balance == 1000
    assert tx.sender_wallet.balance == 0
    assert tx.status == TransactionStatus.SUCCESSFUL


def test_decline_p2p_pull_transaction(seed_wallet):
    """consider adding request feature if a transaction has been made previously"""
    wallet1 = seed_wallet()
    wallet2 = seed_wallet()

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
    assert tx.recipient_wallet.balance == 0
    assert tx.sender_wallet.balance == 1000

    assert tx.status == TransactionStatus.PENDING
    assert tx.mode == TransactionMode.APP_TRANSFER
    assert tx.transaction_type == TransactionType.P2P_PULL

    # Complete transaction
    tx.decline_p2p_pull_transaction()

    assert tx.recipient_wallet.balance == 0
    assert tx.sender_wallet.balance == 1000
    assert tx.status == TransactionStatus.DECLINED


def test_p2p_push_transaction_insufficient_balance(seed_wallet):
    wallet1 = seed_wallet()
    wallet2 = seed_wallet()

    wallet1.balance = 1000
    tx = Transaction(
        amount=2000,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        recipient_wallet=wallet2,
        sender_wallet=wallet1,
    )

    with pytest.raises(TransactionNotAllowedException) as e_info:
        tx.execute_transaction()

    assert str(e_info.value) == "Insufficient balance in sender's wallet"
    assert tx.sender_wallet.balance == 1000
    assert tx.recipient_wallet.balance == 0
    assert tx.status == TransactionStatus.FAILED
    assert tx.mode == TransactionMode.APP_TRANSFER
    assert tx.transaction_type == TransactionType.P2P_PUSH


def test_p2p_push_transaction_self_wallet(seed_wallet):
    wallet1 = seed_wallet()

    wallet1.balance = 1000
    tx = Transaction(
        amount=1000,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        recipient_wallet=wallet1,
        sender_wallet=wallet1,
    )

    with pytest.raises(TransactionNotAllowedException) as e_info:
        tx.execute_transaction()

    assert (
        str(e_info.value)
        == "Constraint violated, sender and recipient wallets are the same"
    )
    assert tx.sender_wallet.balance == 1000
    assert tx.recipient_wallet.balance == 1000
    assert tx.status == TransactionStatus.FAILED
    assert tx.mode == TransactionMode.APP_TRANSFER
    assert tx.transaction_type == TransactionType.P2P_PUSH


def test_redeem_voucher(seed_wallet):
    sender_wallet = seed_wallet()
    recipient_wallet = seed_wallet()
    # giving money to source wallet (cardpay)
    sender_wallet.balance = 1000

    tx = Transaction(
        amount=1000,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.VOUCHER,
        recipient_wallet=recipient_wallet,
        sender_wallet=sender_wallet,
    )

    tx.redeem_voucher()

    assert recipient_wallet.balance == 1000
    assert sender_wallet.balance == 0
    assert tx.status == TransactionStatus.SUCCESSFUL


def test_redeemed_voucher(seed_wallet):
    recipient_wallet = seed_wallet()
    sender_wallet = seed_wallet()
    # giving money to source wallet (cardpay)
    sender_wallet.balance = 1000

    tx = Transaction(
        amount=1000,
        mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.VOUCHER,
        recipient_wallet=recipient_wallet,
        sender_wallet=sender_wallet,
    )
    # legal redeem
    tx.redeem_voucher()

    with pytest.raises(TransactionNotAllowedException) as e_info:
        # illegal redeem
        tx.redeem_voucher()

    assert recipient_wallet.balance == 1000
    assert sender_wallet.balance == 0
    assert str(e_info.value) == "Constraint violated, voucher is no longer valid"

def test_amount_negative(seed_wallet):
    customer_wallet = seed_wallet()
    vendor_wallet = seed_wallet()

    tx = Transaction(
        amount= -1000,
        mode=TransactionMode.QR,
        transaction_type=TransactionType.POS,
        recipient_wallet=vendor_wallet,
        sender_wallet=customer_wallet,
    )
    with pytest.raises(TransactionNotAllowedException, match="Amount is zero or negative"):
        tx.execute_transaction()

    assert tx.sender_wallet.balance == 0
    assert tx.recipient_wallet.balance == 0

    assert tx.status == TransactionStatus.FAILED
    assert tx.mode == TransactionMode.QR
    assert tx.transaction_type == TransactionType.POS