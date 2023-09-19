from datetime import datetime
from uuid import uuid4
import pytest
from core.payment.domain import model as mdl
from core.payment.domain import exceptions as ex


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
    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=1000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.P2P_PUSH,
        recipient_wallet=wallet2,
        sender_wallet=wallet1,
    )
    tx.execute_transaction()

    assert tx.sender_wallet.balance == 0
    assert tx.recipient_wallet.balance == 1000

    assert tx.status == mdl.TransactionStatus.SUCCESSFUL
    assert tx.mode == mdl.TransactionMode.APP_TRANSFER
    assert tx.transaction_type == mdl.TransactionType.P2P_PUSH

    assert tx.sender_wallet == tx.sender_wallet
    assert tx.recipient_wallet == tx.recipient_wallet

    assert tx.status == mdl.TransactionStatus.SUCCESSFUL


def test_initiate_deposit(seed_wallet):
    wallet = seed_wallet()
    pg_wallet = seed_wallet()

    pg_wallet.balance = 1000000

    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=1000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.PAYMENT_GATEWAY,
        recipient_wallet=wallet,
        sender_wallet=pg_wallet,
    )

    tx.execute_transaction()

    assert tx.recipient_wallet.balance == 1000
    assert tx.sender_wallet.balance == 1000000 - 1000

    assert tx.status == mdl.TransactionStatus.SUCCESSFUL
    assert tx.mode == mdl.TransactionMode.APP_TRANSFER
    assert tx.transaction_type == mdl.TransactionType.PAYMENT_GATEWAY
    assert tx.amount == 1000


def test_pos_transaction(seed_wallet):
    customer_wallet = seed_wallet()
    vendor_wallet = seed_wallet()

    customer_wallet.balance = 1000
    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=1000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.QR,
        transaction_type=mdl.TransactionType.POS,
        recipient_wallet=vendor_wallet,
        sender_wallet=customer_wallet,
    )
    tx.execute_transaction()

    assert customer_wallet.balance == 0
    assert vendor_wallet.balance == 1000

    assert tx.status == mdl.TransactionStatus.SUCCESSFUL
    assert tx.mode == mdl.TransactionMode.QR
    assert tx.transaction_type == mdl.TransactionType.POS

    assert tx.status == mdl.TransactionStatus.SUCCESSFUL


def test_accept_p2p_pull_transaction(seed_wallet):
    """consider adding request feature if a transaction has been made previously"""
    wallet1 = seed_wallet()
    wallet2 = seed_wallet()

    # Wallet1 requesting 1000 from wallet 2
    wallet2.balance = 1000
    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=1000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.P2P_PULL,
        recipient_wallet=wallet1,
        sender_wallet=wallet2,
    )

    # Initiate transaction
    assert tx.recipient_wallet.balance == 0
    assert tx.sender_wallet.balance == 1000

    assert tx.status == mdl.TransactionStatus.PENDING
    assert tx.mode == mdl.TransactionMode.APP_TRANSFER
    assert tx.transaction_type == mdl.TransactionType.P2P_PULL

    # Complete transaction
    tx.accept_p2p_pull_transaction()

    assert tx.recipient_wallet.balance == 1000
    assert tx.sender_wallet.balance == 0
    assert tx.status == mdl.TransactionStatus.SUCCESSFUL


def test_decline_p2p_pull_transaction(seed_wallet):
    """consider adding request feature if a transaction has been made previously"""
    wallet1 = seed_wallet()
    wallet2 = seed_wallet()

    # Wallet1 requesting 1000 from wallet 2
    wallet2.balance = 1000
    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=1000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.P2P_PULL,
        recipient_wallet=wallet1,
        sender_wallet=wallet2,
    )

    # Initiate transaction
    assert tx.recipient_wallet.balance == 0
    assert tx.sender_wallet.balance == 1000

    assert tx.status == mdl.TransactionStatus.PENDING
    assert tx.mode == mdl.TransactionMode.APP_TRANSFER
    assert tx.transaction_type == mdl.TransactionType.P2P_PULL

    # Complete transaction
    tx.decline_p2p_pull_transaction()

    assert tx.recipient_wallet.balance == 0
    assert tx.sender_wallet.balance == 1000
    assert tx.status == mdl.TransactionStatus.DECLINED


def test_p2p_push_transaction_insufficient_balance(seed_wallet):
    wallet1 = seed_wallet()
    wallet2 = seed_wallet()

    wallet1.balance = 1000
    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=2000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.P2P_PUSH,
        recipient_wallet=wallet2,
        sender_wallet=wallet1,
    )

    with pytest.raises(ex.TransactionNotAllowedException) as e_info:
        tx.execute_transaction()

    assert str(e_info.value) == "Insufficient balance in sender's wallet"
    assert tx.sender_wallet.balance == 1000
    assert tx.recipient_wallet.balance == 0
    assert tx.status == mdl.TransactionStatus.FAILED
    assert tx.mode == mdl.TransactionMode.APP_TRANSFER
    assert tx.transaction_type == mdl.TransactionType.P2P_PUSH


def test_p2p_push_transaction_self_wallet(seed_wallet):
    wallet1 = seed_wallet()

    wallet1.balance = 1000
    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=1000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.P2P_PUSH,
        recipient_wallet=wallet1,
        sender_wallet=wallet1,
    )

    with pytest.raises(ex.TransactionNotAllowedException) as e_info:
        tx.execute_transaction()

    assert (
        str(e_info.value)
        == "Constraint violated, sender and recipient wallets are the same"
    )
    assert tx.sender_wallet.balance == 1000
    assert tx.recipient_wallet.balance == 1000
    assert tx.status == mdl.TransactionStatus.FAILED
    assert tx.mode == mdl.TransactionMode.APP_TRANSFER
    assert tx.transaction_type == mdl.TransactionType.P2P_PUSH


def test_redeem_voucher(seed_wallet):
    sender_wallet = seed_wallet()
    recipient_wallet = seed_wallet()
    # giving money to source wallet (cardpay)
    sender_wallet.balance = 1000

    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=1000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.VOUCHER,
        recipient_wallet=recipient_wallet,
        sender_wallet=sender_wallet,
    )

    tx.redeem_voucher()

    assert recipient_wallet.balance == 1000
    assert sender_wallet.balance == 0
    assert tx.status == mdl.TransactionStatus.SUCCESSFUL


def test_redeemed_voucher(seed_wallet):
    recipient_wallet = seed_wallet()
    sender_wallet = seed_wallet()
    # giving money to source wallet (cardpay)
    sender_wallet.balance = 1000

    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=1000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.VOUCHER,
        recipient_wallet=recipient_wallet,
        sender_wallet=sender_wallet,
    )
    # legal redeem
    tx.redeem_voucher()

    with pytest.raises(ex.TransactionNotAllowedException) as e_info:
        # illegal redeem
        tx.redeem_voucher()

    assert recipient_wallet.balance == 1000
    assert sender_wallet.balance == 0
    assert str(e_info.value) == "Constraint violated, voucher is no longer valid"


def test_amount_negative(seed_wallet):
    customer_wallet = seed_wallet()
    vendor_wallet = seed_wallet()

    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=-1000,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.QR,
        transaction_type=mdl.TransactionType.POS,
        recipient_wallet=vendor_wallet,
        sender_wallet=customer_wallet,
    )
    with pytest.raises(
        mdl.ex.TransactionNotAllowedException, match="Amount is zero or negative"
    ):
        tx.execute_transaction()

    assert tx.sender_wallet.balance == 0
    assert tx.recipient_wallet.balance == 0

    assert tx.status == mdl.TransactionStatus.FAILED
    assert tx.mode == mdl.TransactionMode.QR
    assert tx.transaction_type == mdl.TransactionType.POS


def test_amount_fractional(seed_wallet):
    wallet1 = seed_wallet()
    wallet2 = seed_wallet()
    wallet1.balance = 1000

    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=500.5,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.P2P_PUSH,
        recipient_wallet=wallet2,
        sender_wallet=wallet1,
    )
    with pytest.raises(
        mdl.ex.TransactionNotAllowedException,
        match="Constraint violated, amount is not an integer",
    ):
        tx.execute_transaction()

    tx.amount = 500  # legal amount

    tx.execute_transaction()

    assert tx.sender_wallet.balance == 500
    assert tx.recipient_wallet.balance == 500


def test_amount_breach_upper_limit(seed_wallet):
    wallet1 = seed_wallet()
    wallet2 = seed_wallet()
    wallet1.balance = mdl.TX_UPPER_LIMIT

    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=mdl.TX_UPPER_LIMIT,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.P2P_PUSH,
        recipient_wallet=wallet2,
        sender_wallet=wallet1,
    )
    with pytest.raises(
        mdl.ex.TransactionNotAllowedException,
        match=f"Amount is greater than or equal to {mdl.TX_UPPER_LIMIT}",
    ):
        tx.execute_transaction()


def test_reconciliation_upper_limit_tx(seed_wallet):
    vendor_wallet = seed_wallet()
    cardpay_wallet = seed_wallet()
    vendor_wallet.balance = mdl.TX_UPPER_LIMIT * 2

    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=mdl.TX_UPPER_LIMIT,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.RECONCILIATION,
        recipient_wallet=cardpay_wallet,
        sender_wallet=vendor_wallet,
    )
    tx.execute_transaction()

    assert tx.sender_wallet.balance == mdl.TX_UPPER_LIMIT
    assert tx.recipient_wallet.balance == mdl.TX_UPPER_LIMIT

    tx = mdl.Transaction(
        id=str(uuid4()),
        amount=mdl.TX_UPPER_LIMIT,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        status=mdl.TransactionStatus.PENDING,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.P2P_PUSH,
        recipient_wallet=cardpay_wallet,
        sender_wallet=vendor_wallet,
    )

    with pytest.raises(
        mdl.ex.TransactionNotAllowedException,
        match=f"Amount is greater than or equal to {mdl.TX_UPPER_LIMIT}",
    ):
        tx.execute_transaction()

    assert tx.sender_wallet.balance == mdl.TX_UPPER_LIMIT
    assert tx.recipient_wallet.balance == mdl.TX_UPPER_LIMIT
