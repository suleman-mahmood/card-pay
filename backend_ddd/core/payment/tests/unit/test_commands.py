from uuid import uuid4

import pytest
from core.authentication.domain import model as auth_mdl
from core.entrypoint.uow import AbstractUnitOfWork, FakeUnitOfWork
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as acl
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import queries as pmt_qry


def test_accept_p2p_pull_transaction(seed_verified_auth_user, add_1000_wallet_fake):
    uow = FakeUnitOfWork()
    _, sender_wallet = seed_verified_auth_user(uow)
    _, recipient_wallet = seed_verified_auth_user(uow)

    # for testing purposes
    add_1000_wallet_fake(uow=uow, wallet_id=sender_wallet.id)

    # make pull transaction
    tx_id = str(uuid4())
    pmt_cmd._execute_transaction(
        tx_id=tx_id,
        sender_wallet_id=sender_wallet.id,
        recipient_wallet_id=recipient_wallet.id,
        amount=1000,
        transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.P2P_PULL,
        uow=uow,
        auth_svc=acl.FakeAuthenticationService(),
    )

    # accept previously created pull transaction
    pmt_cmd.accept_p2p_pull_transaction(transaction_id=tx_id, uow=uow)

    # fetch tx from memory
    fetched_tx = uow.transactions.get(transaction_id=tx_id)

    assert fetched_tx.amount == 1000
    assert fetched_tx.mode == pmt_mdl.TransactionMode.APP_TRANSFER
    assert fetched_tx.transaction_type == pmt_mdl.TransactionType.P2P_PULL
    assert fetched_tx.status == pmt_mdl.TransactionStatus.SUCCESSFUL
    assert fetched_tx.sender_wallet.id == sender_wallet.id
    assert fetched_tx.recipient_wallet.id == recipient_wallet.id
    assert fetched_tx.recipient_wallet.balance == 1000
    assert fetched_tx.sender_wallet.balance == 0

    uow.close_connection()


def test_decline_p2p_pull_transaction(seed_verified_auth_user, add_1000_wallet_fake):
    uow = FakeUnitOfWork()
    sender, _ = seed_verified_auth_user(uow=uow)
    recipient, _ = seed_verified_auth_user(uow=uow)

    # for testing purposes
    add_1000_wallet_fake(uow=uow, wallet_id=sender.id)

    tx_id = str(uuid4())
    pmt_cmd._execute_transaction(
        tx_id=tx_id,
        sender_wallet_id=sender.id,
        recipient_wallet_id=recipient.id,
        amount=1000,
        transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.P2P_PULL,
        uow=uow,
        auth_svc=acl.FakeAuthenticationService(),
    )

    pmt_cmd.decline_p2p_pull_transaction(transaction_id=tx_id, uow=uow)
    fetched_tx = uow.transactions.get(transaction_id=tx_id)

    assert fetched_tx.amount == 1000
    assert fetched_tx.mode == pmt_mdl.TransactionMode.APP_TRANSFER
    assert fetched_tx.transaction_type == pmt_mdl.TransactionType.P2P_PULL
    assert fetched_tx.status == pmt_mdl.TransactionStatus.DECLINED
    assert fetched_tx.sender_wallet.id == sender.id
    assert fetched_tx.recipient_wallet.id == recipient.id
    assert fetched_tx.recipient_wallet.balance == 0
    assert fetched_tx.sender_wallet.balance == 1000

    uow.close_connection()


def test_generate_voucher(seed_verified_auth_user, add_1000_wallet_fake):
    uow = FakeUnitOfWork()

    user, _ = seed_verified_auth_user(uow=uow)
    add_1000_wallet_fake(uow=uow, wallet_id=user.id)

    tx_id = str(uuid4())
    pmt_cmd.generate_voucher(
        tx_id=tx_id,
        sender_wallet_id=user.id,
        amount=1000,
        uow=uow,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx_id)

    assert fetched_tx.amount == 1000
    assert fetched_tx.sender_wallet.id == user.id
    assert fetched_tx.recipient_wallet.id == user.id
    assert fetched_tx.mode == pmt_mdl.TransactionMode.APP_TRANSFER
    assert fetched_tx.transaction_type == pmt_mdl.TransactionType.VOUCHER
    assert fetched_tx.status == pmt_mdl.TransactionStatus.PENDING


def test_redeem_voucher(seed_verified_auth_user, add_1000_wallet_fake):
    uow = FakeUnitOfWork()
    generator, _ = seed_verified_auth_user(uow=uow)
    redeemer, _ = seed_verified_auth_user(uow=uow)

    add_1000_wallet_fake(uow=uow, wallet_id=generator.id)

    tx_id = str(uuid4())
    pmt_cmd.generate_voucher(
        tx_id=tx_id,
        sender_wallet_id=generator.id,
        amount=1000,
        uow=uow,
    )

    pmt_cmd.redeem_voucher(
        recipient_wallet_id=redeemer.id,
        transaction_id=tx_id,
        uow=uow,
    )

    fetched_tx = uow.transactions.get(tx_id)

    assert fetched_tx.amount == 1000
    assert fetched_tx.recipient_wallet.balance == 1000
    assert fetched_tx.sender_wallet.balance == 0
    assert fetched_tx.transaction_type == pmt_mdl.TransactionType.VOUCHER
    assert fetched_tx.status == pmt_mdl.TransactionStatus.SUCCESSFUL


def test_execute_qr_transaction(
    seed_verified_auth_vendor, seed_verified_auth_user, add_1000_wallet_fake
):
    uow = FakeUnitOfWork()
    auth_svc = acl.FakeAuthenticationService()
    pmt_svc = acl.FakePaymentService()
    sender_customer, _ = seed_verified_auth_user(uow)
    vendor, vendor_wallet = seed_verified_auth_vendor(uow)

    add_1000_wallet_fake(uow=uow, wallet_id=sender_customer.wallet_id)

    # test qr txn to invalid qr version
    with pytest.raises(pmt_svc_ex.InvalidQRVersionException, match="Invalid QR version"):
        pmt_cmd.execute_qr_transaction(
            tx_id=str(uuid4()),
            amount=400,
            sender_wallet_id=sender_customer.wallet_id,
            recipient_qr_id=vendor_wallet.qr_id,
            version=0,
            uow=uow,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )

    with pytest.raises(pmt_svc_ex.InvalidQRCodeException, match="Invalid QR code"):
        pmt_cmd.execute_qr_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=sender_customer.wallet_id,
            recipient_qr_id=str(uuid4()),
            version=1,
            amount=400,
            uow=uow,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )

    # test qr txn to vendor from customer
    tx_id = str(uuid4())
    pmt_svc.set_user_wallet_id_and_type(
        wallet_id=vendor.wallet_id, user_type=auth_mdl.UserType.VENDOR
    )
    pmt_cmd.execute_qr_transaction(
        tx_id=tx_id,
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=vendor_wallet.qr_id,
        amount=400,
        version=1,
        uow=uow,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx_id)
    assert fetched_tx.id == tx_id
    assert fetched_tx.amount == 400
    assert fetched_tx.sender_wallet.id == sender_customer.wallet_id
    assert fetched_tx.recipient_wallet.id == vendor_wallet.id
    assert fetched_tx.mode == pmt_mdl.TransactionMode.QR
    assert fetched_tx.status == pmt_mdl.TransactionStatus.SUCCESSFUL
    assert fetched_tx.transaction_type == pmt_mdl.TransactionType.VIRTUAL_POS

    # test insufficient balance
    with pytest.raises(
        pmt_svc_ex.TransactionFailedException,
        match="Insufficient balance in sender's wallet",
    ):
        pmt_cmd.execute_qr_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=sender_customer.wallet_id,
            recipient_qr_id=vendor_wallet.qr_id,
            amount=601,
            version=1,
            uow=uow,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )

    # test p2p qr txn
    recipient_customer, recipient_customer_wallet = seed_verified_auth_user(uow)
    pmt_svc.set_user_wallet_id_and_type(
        wallet_id=recipient_customer.wallet_id, user_type=auth_mdl.UserType.CUSTOMER
    )
    tx_id = str(uuid4())
    pmt_cmd.execute_qr_transaction(
        tx_id=tx_id,
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=recipient_customer_wallet.qr_id,
        amount=500,
        version=1,
        uow=uow,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx_id)
    assert fetched_tx.id == tx_id
    assert fetched_tx.amount == 500
    assert fetched_tx.sender_wallet.id == sender_customer.wallet_id
    assert fetched_tx.recipient_wallet.id == recipient_customer_wallet.id
    assert fetched_tx.mode == pmt_mdl.TransactionMode.QR
    assert fetched_tx.status == pmt_mdl.TransactionStatus.SUCCESSFUL
    assert fetched_tx.transaction_type == pmt_mdl.TransactionType.P2P_PUSH

    uow.close_connection()


def test_reconcile_vendor(
    seed_verified_auth_user,
    seed_verified_auth_vendor,
    seed_verified_auth_cardpay_fake,
    add_1000_wallet_fake,
):
    uow = FakeUnitOfWork()
    sender_customer, _ = seed_verified_auth_user(uow)
    recipient_vendor, vendor_wallet = seed_verified_auth_vendor(uow)
    cardpay = seed_verified_auth_cardpay_fake(uow)
    auth_svc = acl.FakeAuthenticationService()
    pmt_svc = acl.FakePaymentService()

    add_1000_wallet_fake(uow=uow, wallet_id=sender_customer.wallet_id)
    pmt_svc.set_user_wallet_id_and_type(
        wallet_id=vendor_wallet.id, user_type=auth_mdl.UserType.VENDOR
    )

    pmt_cmd.execute_qr_transaction(
        tx_id=str(uuid4()),
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=vendor_wallet.qr_id,
        amount=400,
        version=1,
        uow=uow,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )
    pmt_cmd.execute_qr_transaction(
        tx_id=str(uuid4()),
        sender_wallet_id=sender_customer.wallet_id,
        recipient_qr_id=vendor_wallet.qr_id,
        amount=200,
        version=1,
        uow=uow,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )

    sender_balance = uow.transactions.get_wallet(wallet_id=sender_customer.wallet_id).balance
    vendor_balance = uow.transactions.get_wallet(wallet_id=recipient_vendor.wallet_id).balance

    assert sender_balance == 400
    assert vendor_balance == 600

    # test reconciliation
    pmt_svc.set_starred_wallet_id(wallet_id=cardpay.wallet_id)
    pmt_svc.set_wallet_balance(600)
    pmt_cmd.payment_retools_reconcile_vendor(
        tx_id=str(uuid4()),
        vendor_wallet_id=vendor_wallet.id,
        uow=uow,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )

    cardpay_balance = uow.transactions.get_wallet(wallet_id=cardpay.wallet_id).balance
    vendor_balance = uow.transactions.get_wallet(wallet_id=recipient_vendor.wallet_id).balance

    assert vendor_balance == 0
    assert cardpay_balance == 600

    # test reconciliation with zero balance
    pmt_svc.set_wallet_balance(0)
    with pytest.raises(pmt_svc_ex.TransactionFailedException, match="Amount is zero or negative"):
        pmt_cmd.payment_retools_reconcile_vendor(
            tx_id=str(uuid4()),
            vendor_wallet_id=vendor_wallet.id,
            uow=uow,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )

    uow.close_connection()


def test_failing_txn(seed_verified_auth_user):
    uow = FakeUnitOfWork()
    user_1, _ = seed_verified_auth_user(uow)
    user_2, _ = seed_verified_auth_user(uow)

    tx_id = str(uuid4())
    with pytest.raises(pmt_svc_ex.TransactionFailedException):
        pmt_cmd._execute_transaction(
            tx_id=tx_id,
            sender_wallet_id=user_1.id,
            recipient_wallet_id=user_2.id,
            amount=1000,
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
            uow=uow,
            auth_svc=acl.FakeAuthenticationService(),
        )

    fetched_failed_tx = uow.transactions.get(transaction_id=tx_id)
    assert fetched_failed_tx.amount == 1000
    assert fetched_failed_tx.status == pmt_mdl.TransactionStatus.FAILED
    uow.close_connection()


def test_accept_payment_gateway(seed_verified_auth_user, add_1000_wallet_fake):
    uow = FakeUnitOfWork()
    user, _ = seed_verified_auth_user(uow)
    pp_user, _ = seed_verified_auth_user(uow)

    add_1000_wallet_fake(uow=uow, wallet_id=pp_user.id)
    tx_id = str(uuid4())

    auth_svc = acl.FakeAuthenticationService()
    pp_svc = acl.FakePayproService()
    pp_svc.set_paypro_wallet(wallet_id=pp_user.id)

    pmt_cmd.create_deposit_request(
        tx_id=tx_id,
        user_id=user.id,
        amount=1000,
        auth_svc=auth_svc,
        pp_svc=pp_svc,
        uow=uow,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx_id)

    assert fetched_tx.id == tx_id
    assert fetched_tx.amount == 1000
    assert fetched_tx.mode == pmt_mdl.TransactionMode.APP_TRANSFER
    assert fetched_tx.transaction_type == pmt_mdl.TransactionType.PAYMENT_GATEWAY
    assert fetched_tx.status == pmt_mdl.TransactionStatus.PENDING
    assert fetched_tx.recipient_wallet.balance == 0
    assert fetched_tx.sender_wallet.balance == 1000

    pmt_cmd.accept_payment_gateway_transaction(transaction_id=tx_id, uow=uow)

    fetched_tx = uow.transactions.get(transaction_id=tx_id)

    assert fetched_tx.id == tx_id
    assert fetched_tx.amount == 1000
    assert fetched_tx.mode == pmt_mdl.TransactionMode.APP_TRANSFER
    assert fetched_tx.transaction_type == pmt_mdl.TransactionType.PAYMENT_GATEWAY
    assert fetched_tx.status == pmt_mdl.TransactionStatus.SUCCESSFUL
    assert fetched_tx.recipient_wallet.balance == 1000
    assert fetched_tx.sender_wallet.balance == 0


def test_create_deposit_request(seed_verified_auth_user, seed_wallet, add_1000_wallet_fake):
    uow = FakeUnitOfWork()
    user, _ = seed_verified_auth_user(uow)
    pp_user, _ = seed_verified_auth_user(uow)

    add_1000_wallet_fake(uow=uow, wallet_id=pp_user.id)
    tx_id = str(uuid4())

    auth_svc = acl.FakeAuthenticationService()
    pp_svc = acl.FakePayproService()
    pp_svc.set_paypro_wallet(wallet_id=pp_user.id)

    pmt_cmd.create_deposit_request(
        tx_id=tx_id,
        user_id=user.id,
        amount=1000,
        auth_svc=auth_svc,
        pp_svc=pp_svc,
        uow=uow,
    )

    fetched_tx = uow.transactions.get(transaction_id=tx_id)

    assert fetched_tx.id == tx_id
    assert fetched_tx.amount == 1000
    assert fetched_tx.mode == pmt_mdl.TransactionMode.APP_TRANSFER
    assert fetched_tx.transaction_type == pmt_mdl.TransactionType.PAYMENT_GATEWAY
    assert fetched_tx.status == pmt_mdl.TransactionStatus.PENDING
    assert fetched_tx.recipient_wallet.balance == 0
    assert fetched_tx.sender_wallet.balance == 1000


def test_execute_qr_transaction_invalid_qr_ids(
    seed_verified_auth_vendor, seed_verified_auth_user, add_1000_wallet_fake
):
    uow = FakeUnitOfWork()
    auth_svc = acl.FakeAuthenticationService()
    pmt_svc = acl.FakePaymentService()
    customer, _ = seed_verified_auth_user(uow)
    vendor, vendor_wallet = seed_verified_auth_vendor(uow)
    waiter, waiter_wallet = seed_verified_auth_vendor(uow)
    add_1000_wallet_fake(uow=uow, wallet_id=customer.wallet_id)

    with pytest.raises(pmt_svc_ex.InvalidQRCodeException, match="Invalid QR code"):
        pmt_cmd.execute_qr_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=customer.wallet_id,
            recipient_qr_id=str(uuid4()),
            amount=400,
            version=1,
            uow=uow,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )


def test_execute_qr_transaction_insufficient_balance(
    seed_verified_auth_vendor, seed_verified_auth_user, add_1000_wallet_fake
):
    uow = FakeUnitOfWork()
    auth_svc = acl.FakeAuthenticationService()
    pmt_svc = acl.FakePaymentService()
    customer, _ = seed_verified_auth_user(uow)
    vendor, vendor_wallet = seed_verified_auth_vendor(uow)
    waiter, waiter_wallet = seed_verified_auth_vendor(uow)
    add_1000_wallet_fake(uow=uow, wallet_id=customer.wallet_id)

    pmt_svc.set_user_wallet_id_and_type(
        wallet_id=vendor.wallet_id, user_type=auth_mdl.UserType.VENDOR
    )
    with pytest.raises(
        pmt_svc_ex.TransactionFailedException,
        match="Insufficient balance in sender's wallet",
    ):
        pmt_cmd.execute_qr_transaction(
            tx_id=str(uuid4()),
            sender_wallet_id=customer.wallet_id,
            recipient_qr_id=vendor_wallet.qr_id,
            amount=1001,
            version=1,
            uow=uow,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )


def test_bulk_reconcile_vendors(
    seed_verified_auth_vendor, seed_verified_auth_cardpay_fake, add_1000_wallet_fake
):
    uow = FakeUnitOfWork()
    auth_svc = acl.FakeAuthenticationService()
    pmt_svc = acl.FakePaymentService()

    cardpay = seed_verified_auth_cardpay_fake(uow)
    # add_1000_wallet_fake(uow=uow,wallet_id=cardpay.id)
    # add_1000_wallet_fake(uow=uow,wallet_id=cardpay.id)
    # add_1000_wallet_fake(uow=uow,wallet_id=cardpay.id)
    pmt_svc.set_starred_wallet_id(wallet_id=cardpay.id)

    vendor_1, vendor_wallet_1 = seed_verified_auth_vendor(uow)
    add_1000_wallet_fake(uow=uow, wallet_id=vendor_wallet_1.id)
    vendor_2, vendor_wallet_2 = seed_verified_auth_vendor(uow)
    add_1000_wallet_fake(uow=uow, wallet_id=vendor_wallet_2.id)
    vendor_3, vendor_wallet_3 = seed_verified_auth_vendor(uow)
    add_1000_wallet_fake(uow=uow, wallet_id=vendor_wallet_3.id)
    pmt_svc.set_wallet_balance(1000)
    # All vendors will be reconciled 1000 balance now

    pmt_cmd.bulk_reconcile_vendors(
        vendor_wallet_ids=[vendor_wallet_1.id, vendor_wallet_2.id, vendor_wallet_3.id],
        uow=uow,
        auth_svc=auth_svc,
        pmt_svc=pmt_svc,
    )

    assert uow.transactions.get_wallet(wallet_id=vendor_wallet_1.id).balance == 0
    assert uow.transactions.get_wallet(wallet_id=vendor_wallet_2.id).balance == 0
    assert uow.transactions.get_wallet(wallet_id=vendor_wallet_3.id).balance == 0
    assert uow.transactions.get_wallet(wallet_id=cardpay.wallet_id).balance == 3000


def test_bulk_reconcile_vendors_txn_failed(
    seed_verified_auth_vendor, seed_verified_auth_cardpay_fake, add_1000_wallet_fake
):
    uow = FakeUnitOfWork()
    auth_svc = acl.FakeAuthenticationService()
    pmt_svc = acl.FakePaymentService()

    cardpay = seed_verified_auth_cardpay_fake(uow)
    pmt_svc.set_starred_wallet_id(wallet_id=cardpay.id)

    vendor_1, vendor_wallet_1 = seed_verified_auth_vendor(uow)
    vendor_2, vendor_wallet_2 = seed_verified_auth_vendor(uow)
    vendor_3, vendor_wallet_3 = seed_verified_auth_vendor(uow)
    pmt_svc.set_wallet_balance(9000)

    with pytest.raises(pmt_svc_ex.TransactionFailedException):
        pmt_cmd.bulk_reconcile_vendors(
            vendor_wallet_ids=[vendor_wallet_1.id, vendor_wallet_2.id, vendor_wallet_3.id],
            uow=uow,
            auth_svc=auth_svc,
            pmt_svc=pmt_svc,
        )
