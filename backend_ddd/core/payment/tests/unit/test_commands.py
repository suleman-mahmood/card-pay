import threading
import multiprocessing as mp
from time import sleep
from datetime import datetime
from ...entrypoint.commands import (
    create_wallet,
    execute_transaction,
    accept_p2p_pull_transaction,
    decline_p2p_pull_transaction,
    redeem_voucher,
    generate_voucher,
    # slow_execute_transaction,
    # _get_paypro_auth_token,
    # get_deposit_checkout_url,
    execute_qr_transaction,
    payment_retools_reconcile_vendor,
)
from ....marketing.entrypoint import commands as marketing_commands
from ....authentication.tests.conftest import (
    seed_auth_user,
    seed_verified_auth_user,
    seed_auth_vendor,
    seed_verified_auth_vendor,
    seed_auth_cardpay,
    seed_verified_auth_cardpay,
)
from ....entrypoint.uow import UnitOfWork, AbstractUnitOfWork, FakeUnitOfWork
from ...domain.model import (
    TransactionMode,
    TransactionType,
    TransactionStatus,
    Transaction,
)
from queue import Queue
from uuid import uuid4
import pytest
from core.authentication.entrypoint import queries as auth_queries
from core.payment.entrypoint import exceptions as pmt_cmd_ex
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as acl
from core.authentication.domain import model as auth_mdl


def test_accept_p2p_pull_transaction(seed_verified_auth_user):
    uow = FakeUnitOfWork()
    sender, sender_wallet = seed_verified_auth_user(uow)
    recipient, recipient_wallet = seed_verified_auth_user(uow)

    # for testing purposes
    uow.transactions.add_1000_wallet(wallet_id=sender_wallet.id)

    # make pull transaction
    tx_id = str(uuid4())
    execute_transaction(
        tx_id=tx_id,
        sender_wallet_id=sender_wallet.id,
        recipient_wallet_id=recipient_wallet.id,
        amount=1000,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PULL,
        uow=uow,
        mktg_svc=acl.FakeMarketingService(),
        auth_svc=acl.FakeAuthenticationService(),
    )

    # accept previously created pull transaction
    accept_p2p_pull_transaction(
        transaction_id=tx_id, uow=uow, mktg_svc=acl.FakeMarketingService()
    )

    # fetch tx from memory
    fetched_tx = uow.transactions.get(transaction_id=tx_id)

    assert fetched_tx.amount == 1000
    assert fetched_tx.mode == TransactionMode.APP_TRANSFER
    assert fetched_tx.transaction_type == TransactionType.P2P_PULL
    assert fetched_tx.status == TransactionStatus.SUCCESSFUL
    assert fetched_tx.sender_wallet.id == sender_wallet.id
    assert fetched_tx.recipient_wallet.id == recipient_wallet.id
    assert fetched_tx.recipient_wallet.balance == 1000
    assert fetched_tx.sender_wallet.balance == 0

    uow.close_connection()


def test_decline_p2p_pull_transaction(seed_verified_auth_user):
    uow = FakeUnitOfWork()
    sender, _ = seed_verified_auth_user(uow=uow)
    recipient, _ = seed_verified_auth_user(uow=uow)

    # for testing purposes
    uow.transactions.add_1000_wallet(wallet_id=sender.id)

    tx_id = str(uuid4())
    execute_transaction(
        tx_id=tx_id,
        sender_wallet_id=sender.id,
        recipient_wallet_id=recipient.id,
        amount=1000,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PULL,
        uow=uow,
        mktg_svc=acl.FakeMarketingService(),
        auth_svc=acl.FakeAuthenticationService(),
    )

    decline_p2p_pull_transaction(transaction_id=tx_id, uow=uow)
    fetched_tx = uow.transactions.get(transaction_id=tx_id)

    assert fetched_tx.amount == 1000
    assert fetched_tx.mode == TransactionMode.APP_TRANSFER
    assert fetched_tx.transaction_type == TransactionType.P2P_PULL
    assert fetched_tx.status == TransactionStatus.DECLINED
    assert fetched_tx.sender_wallet.id == sender.id
    assert fetched_tx.recipient_wallet.id == recipient.id
    assert fetched_tx.recipient_wallet.balance == 0
    assert fetched_tx.sender_wallet.balance == 1000

    uow.close_connection()


def test_generate_voucher(seed_verified_auth_user):
    uow = FakeUnitOfWork()

    user, _ = seed_verified_auth_user(uow=uow)
    uow.transactions.add_1000_wallet(wallet_id=user.id)

    tx_id = str(uuid4())
    generate_voucher(
        tx_id=tx_id,
        sender_wallet_id=user.id,
        amount=1000,
        uow=uow,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx_id)

    assert fetched_tx.amount == 1000
    assert fetched_tx.sender_wallet.id == user.id
    assert fetched_tx.recipient_wallet.id == user.id
    assert fetched_tx.mode == TransactionMode.APP_TRANSFER
    assert fetched_tx.transaction_type == TransactionType.VOUCHER
    assert fetched_tx.status == TransactionStatus.PENDING


def test_redeem_voucher(seed_verified_auth_user):
    uow = FakeUnitOfWork()
    generator, _ = seed_verified_auth_user(uow=uow)
    redeemer, _ = seed_verified_auth_user(uow=uow)

    uow.transactions.add_1000_wallet(wallet_id=generator.id)

    tx_id = str(uuid4())
    generate_voucher(
        tx_id=tx_id,
        sender_wallet_id=generator.id,
        amount=1000,
        uow=uow,
    )

    redeem_voucher(
        recipient_wallet_id=redeemer.id,
        transaction_id=tx_id,
        uow=uow,
    )

    fetched_tx = uow.transactions.get(tx_id)

    assert fetched_tx.amount == 1000
    assert fetched_tx.recipient_wallet.balance == 1000
    assert fetched_tx.sender_wallet.balance == 0
    assert fetched_tx.transaction_type == TransactionType.VOUCHER
    assert fetched_tx.status == TransactionStatus.SUCCESSFUL


def test_execute_qr_transaction(seed_verified_auth_vendor, seed_verified_auth_user):
    uow = FakeUnitOfWork()
    mktg_svc = acl.FakeMarketingService()
    auth_svc = acl.FakeAuthenticationService()
    pmt_svc = acl.FakePaymentService()
    sender_customer, _ = seed_verified_auth_user(uow)
    vendor, vendor_wallet = seed_verified_auth_vendor(uow)

    mktg_svc.add_and_set_missing_weightages_to_zero(uow=uow)

    uow.transactions.add_1000_wallet(wallet_id=sender_customer.wallet_id)

    # test qr txn to invalid qr version
    with pytest.raises(
        pmt_cmd_ex.InvalidQRVersionException, match="Invalid QR version"
    ):
        execute_qr_transaction(
            tx_id=str(uuid4()),
            amount=400,
            sender_wallet_id=sender_customer.wallet_id,
            recipient_qr_id=vendor_wallet.qr_id,
            version=0,
            uow=uow,
            mktg_svc=mktg_svc,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )

    with pytest.raises(pmt_cmd_ex.InvalidQRCodeException, match="Invalid QR code"):
        execute_qr_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=sender_customer.wallet_id,
            recipient_qr_id=str(uuid4()),
            version=1,
            amount=400,
            uow=uow,
            mktg_svc=mktg_svc,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )

    # test qr txn to vendor from customer
    tx_id = str(uuid4())
    pmt_svc.set_user_wallet_id_and_type(
        wallet_id=vendor.wallet_id, user_type=auth_mdl.UserType.VENDOR
    )
    execute_qr_transaction(
        tx_id=tx_id,
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=vendor_wallet.qr_id,
        amount=400,
        version=1,
        uow=uow,
        mktg_svc=mktg_svc,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx_id)
    assert fetched_tx.id == tx_id
    assert fetched_tx.amount == 400
    assert fetched_tx.sender_wallet.id == sender_customer.wallet_id
    assert fetched_tx.recipient_wallet.id == vendor_wallet.id
    assert fetched_tx.mode == TransactionMode.QR
    assert fetched_tx.status == TransactionStatus.SUCCESSFUL
    assert fetched_tx.transaction_type == TransactionType.VIRTUAL_POS

    # test insufficient balance
    with pytest.raises(
        pmt_cmd_ex.TransactionFailedException,
        match="Insufficient balance in sender's wallet",
    ):
        execute_qr_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=sender_customer.wallet_id,
            recipient_qr_id=vendor_wallet.qr_id,
            amount=601,
            version=1,
            uow=uow,
            mktg_svc=mktg_svc,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )

    # test p2p qr txn
    recipient_customer, recipient_customer_wallet = seed_verified_auth_user(uow)
    pmt_svc.set_user_wallet_id_and_type(
        wallet_id=recipient_customer.wallet_id, user_type=auth_mdl.UserType.CUSTOMER
    )
    tx_id = str(uuid4())
    execute_qr_transaction(
        tx_id=tx_id,
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=recipient_customer_wallet.qr_id,
        amount=500,
        version=1,
        uow=uow,
        mktg_svc=mktg_svc,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx_id)
    assert fetched_tx.id == tx_id
    assert fetched_tx.amount == 500
    assert fetched_tx.sender_wallet.id == sender_customer.wallet_id
    assert fetched_tx.recipient_wallet.id == recipient_customer_wallet.id
    assert fetched_tx.mode == TransactionMode.QR
    assert fetched_tx.status == TransactionStatus.SUCCESSFUL
    assert fetched_tx.transaction_type == TransactionType.P2P_PUSH

    uow.close_connection()


def test_reconcile_vendor(
    seed_verified_auth_user, seed_verified_auth_vendor, seed_verified_auth_cardpay
):
    uow = FakeUnitOfWork()
    sender_customer, _ = seed_verified_auth_user(uow)
    recipient_vendor, vendor_wallet = seed_verified_auth_vendor(uow)
    cardpay = seed_verified_auth_cardpay(uow)
    mktg_svc = acl.FakeMarketingService()
    auth_svc = acl.FakeAuthenticationService()
    pmt_svc = acl.FakePaymentService()

    mktg_svc.add_and_set_missing_weightages_to_zero(uow=uow)

    uow.transactions.add_1000_wallet(wallet_id=sender_customer.wallet_id)
    pmt_svc.set_user_wallet_id_and_type(
        wallet_id=vendor_wallet.id, user_type=auth_mdl.UserType.VENDOR
    )

    execute_qr_transaction(
        tx_id=str(uuid4()),
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=vendor_wallet.qr_id,
        amount=400,
        version=1,
        uow=uow,
        mktg_svc=mktg_svc,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )
    execute_qr_transaction(
        tx_id=str(uuid4()),
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=vendor_wallet.qr_id,
        amount=200,
        version=1,
        uow=uow,
        mktg_svc=mktg_svc,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )

    sender_balance = uow.transactions.get_wallet(
        wallet_id=sender_customer.wallet_id
    ).balance
    vendor_balance = uow.transactions.get_wallet(
        wallet_id=recipient_vendor.wallet_id
    ).balance

    assert sender_balance == 400
    assert vendor_balance == 600

    # test reconciliation
    pmt_svc.set_starred_wallet_id(wallet_id=cardpay.wallet_id)
    pmt_svc.set_wallet_balance(600)
    payment_retools_reconcile_vendor(
        tx_id=str(uuid4()),
        vendor_wallet_id=vendor_wallet.id,
        uow=uow,
        mktg_svc=mktg_svc,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )

    cardpay_balance = uow.transactions.get_wallet(wallet_id=cardpay.wallet_id).balance
    vendor_balance = uow.transactions.get_wallet(
        wallet_id=recipient_vendor.wallet_id
    ).balance

    assert vendor_balance == 0
    assert cardpay_balance == 600

    # test reconciliation with zero balance
    pmt_svc.set_wallet_balance(0)
    with pytest.raises(
        pmt_cmd_ex.TransactionFailedException, match="Amount is zero or negative"
    ):
        payment_retools_reconcile_vendor(
            tx_id=str(uuid4()),
            vendor_wallet_id=vendor_wallet.id,
            uow=uow,
            mktg_svc=mktg_svc,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )

    uow.close_connection()


def test_failing_txn(seed_verified_auth_user):
    uow = FakeUnitOfWork()
    user_1, _ = seed_verified_auth_user(uow)
    user_2, _ = seed_verified_auth_user(uow)

    tx_id = str(uuid4())
    with pytest.raises(pmt_cmd_ex.TransactionFailedException):
        execute_transaction(
            tx_id=tx_id,
            sender_wallet_id=user_1.id,
            recipient_wallet_id=user_2.id,
            amount=1000,
            transaction_mode=TransactionMode.APP_TRANSFER,
            transaction_type=TransactionType.P2P_PUSH,
            uow=uow,
            mktg_svc=acl.FakeMarketingService(),
            auth_svc=acl.FakeAuthenticationService(),
        )

    fetched_failed_tx = uow.transactions.get(transaction_id=tx_id)
    assert fetched_failed_tx.amount == 1000
    assert fetched_failed_tx.status == TransactionStatus.FAILED
    uow.close_connection()


# Keep these commented, only for testing at certain times

# def test_get_paypro_token():
# uow = UnitOfWork()

# token = _get_paypro_auth_token(uow=uow)
# sleep(1)
# token_2 = _get_paypro_auth_token(uow=uow)

# assert token == token_2


# def test_get_deposit_checkout_url():
# uow = UnitOfWork()

# payment_url = get_deposit_checkout_url(
# amount=500,
# transaction_id=str(uuid4()),
# email="test@tdd.com",
# full_name="TDD test case",
# phone_number="03333333333",
# uow=uow,
# )

# assert payment_url is not None


# def _get_latest_failed_txn_of_user(user_id: str, uow: AbstractUnitOfWork):
#     with uow:
#         sql = """
#            select id from transactions txn
#            where (sender_wallet_id = %s or recipient_wallet_id = %s)
#            and status = 'FAILED'::transaction_status_enum
#            order by created_at desc
#        """
#         uow.cursor.execute(sql, [user_id, user_id])
#         rows = uow.cursor.fetchone()

#         return uow.transactions.get(transaction_id=rows[0])
