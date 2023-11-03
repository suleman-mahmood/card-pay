from uuid import uuid4

import pytest
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import anti_corruption as auth_acl
from core.authentication.entrypoint import commands as auth_cmd
from core.entrypoint.uow import UnitOfWork
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import queries as pmt_qry


def test_get_wallet_balance(seed_verified_auth_user, add_1000_wallet):
    uow = UnitOfWork()
    user, _ = seed_verified_auth_user(uow)

    fetched_balance = pmt_qry.get_wallet_balance(uow=uow, wallet_id=user.wallet_id)
    assert fetched_balance == 0

    add_1000_wallet(wallet_id=user.wallet_id, uow=uow)
    fetched_balance = pmt_qry.get_wallet_balance(uow=uow, wallet_id=user.wallet_id)
    assert fetched_balance == 1000

    uow.close_connection()


def test_get_wallet_id_from_unique_identifier_and_closed_loop_id(
    seed_verified_user_in_closed_loop,
):
    uow = UnitOfWork()
    user_id, closed_loop_id = seed_verified_user_in_closed_loop(uow)
    unique_identifier = uow.users.get(user_id).closed_loops[closed_loop_id].unique_identifier

    wallet_id = pmt_qry.get_wallet_id_from_unique_identifier_and_closed_loop_id(
        unique_identifier=unique_identifier,
        closed_loop_id=closed_loop_id,
        uow=uow,
    )

    assert wallet_id == user_id

    with pytest.raises(pmt_svc_ex.UserDoesNotExistException):
        pmt_qry.get_wallet_id_from_unique_identifier_and_closed_loop_id(
            unique_identifier=unique_identifier,
            closed_loop_id=str(uuid4()),
            uow=uow,
        )

    with pytest.raises(pmt_svc_ex.UserDoesNotExistException):
        pmt_qry.get_wallet_id_from_unique_identifier_and_closed_loop_id(
            unique_identifier="1234567",
            closed_loop_id=closed_loop_id,
            uow=uow,
        )

    with pytest.raises(pmt_svc_ex.UserDoesNotExistException):
        pmt_qry.get_wallet_id_from_unique_identifier_and_closed_loop_id(
            unique_identifier="1234567",
            closed_loop_id=str(uuid4()),
            uow=uow,
        )

    uow.close_connection()


def test_get_all_closed_loops_id_and_names(seed_auth_closed_loop):
    uow = UnitOfWork()
    closed_loop_id_1 = str(uuid4())
    closed_loop_id_2 = str(uuid4())
    seed_auth_closed_loop(id=closed_loop_id_1, uow=uow)
    seed_auth_closed_loop(id=closed_loop_id_2, uow=uow)

    cl_id_name_dtos = pmt_qry.get_all_closed_loops_id_and_names(uow=uow)
    cl_ids = [cl_id_name_dto.id for cl_id_name_dto in cl_id_name_dtos]

    assert len(cl_id_name_dtos) >= 2
    assert closed_loop_id_1 in cl_ids
    assert closed_loop_id_1 in cl_ids
    assert str(uuid4()) not in cl_ids

    uow.close_connection()

def test_get_all_successful_transactions_of_a_user(
    seed_5_100_transactions_against_user_ids,
):
    uow = UnitOfWork()
    user_id = str(uuid4())
    recipient_id = str(uuid4())
    seed_5_100_transactions_against_user_ids(
        sender_id=user_id,
        recipient_id=recipient_id,
        uow=uow,
    )

    tx_dtos = pmt_qry.get_all_successful_transactions_of_a_user(
        user_id=user_id,
        uow=uow,
        page_size=15,
        offset=0,
    )

    assert len(tx_dtos) == 5

    for tx_dto in tx_dtos:
        assert tx_dto.sender_id == user_id
        assert tx_dto.recipient_id == recipient_id
        assert tx_dto.amount == 100
        assert pmt_mdl.TransactionType[tx_dto.transaction_type] == pmt_mdl.TransactionType.P2P_PUSH
        assert pmt_mdl.TransactionMode[tx_dto.mode] == pmt_mdl.TransactionMode.APP_TRANSFER
        assert pmt_mdl.TransactionStatus[tx_dto.status] == pmt_mdl.TransactionStatus.SUCCESSFUL

    # Do a transaction that fails
    failed_tx_id = str(uuid4())
    with pytest.raises(pmt_svc_ex.TransactionFailedException, match="Insufficient balance"):
        pmt_cmd._execute_transaction(
            tx_id=failed_tx_id,
            amount=600,
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
            sender_wallet_id=user_id,
            recipient_wallet_id=recipient_id,
            uow=uow,
            auth_svc=pmt_acl.FakeAuthenticationService(),
        )

    tx_dtos = pmt_qry.get_all_successful_transactions_of_a_user(
        user_id=user_id,
        uow=uow,
        page_size=15,
        offset=0,
    )

    assert len(tx_dtos) == 5
    assert pmt_mdl.TransactionStatus.FAILED not in [
        pmt_mdl.TransactionStatus[tx_dto.status] for tx_dto in tx_dtos
    ]
    assert failed_tx_id not in [tx_dto.id for tx_dto in tx_dtos]

    uow.close_connection()


def test_payment_retools_get_customers_and_vendors_of_selected_closed_loop(
    seed_verified_auth_user, seed_two_verified_vendors_in_closed_loop
):
    uow = UnitOfWork()

    vendor_1, vendor_2, closed_loop_id = seed_two_verified_vendors_in_closed_loop(uow)

    customer_1, _ = seed_verified_auth_user(uow)
    customer_2, _ = seed_verified_auth_user(uow)
    for user in [customer_1, customer_2]:
        auth_cmd.register_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop_id,
            unique_identifier="1234",
            uow=uow,
            auth_svc=auth_acl.FakeAuthenticationService(),
        )

    customer_vendor_counts_dto = (
        pmt_qry.payment_retools_get_customers_and_vendors_of_selected_closed_loop(
            closed_loop_id=closed_loop_id,
            uow=uow,
        )
    )

    fetched_customer_ids = [
        customer_dto.id for customer_dto in customer_vendor_counts_dto.customers
    ]
    fetched_vendor_ids = [vendor_dto.id for vendor_dto in customer_vendor_counts_dto.vendors]

    assert customer_1.id in fetched_customer_ids
    assert customer_2.id in fetched_customer_ids
    assert vendor_1.id in fetched_vendor_ids
    assert vendor_2.id in fetched_vendor_ids
    assert customer_vendor_counts_dto.counts.customers == 2
    assert customer_vendor_counts_dto.counts.vendors == 2
    assert customer_vendor_counts_dto.counts.count == 4

    uow.close_connection()
    

def test_payment_retools_get_all_transactions_of_selected_user(
    seed_5_100_transactions_against_user_ids,
):
    uow = UnitOfWork()
    user_id = str(uuid4())
    recipient_id = str(uuid4())
    seed_5_100_transactions_against_user_ids(
        sender_id=user_id,
        recipient_id=recipient_id,
        uow=uow,
    )

    with pytest.raises(pmt_svc_ex.TransactionFailedException, match="Insufficient balance"):
        pmt_cmd._execute_transaction(
            tx_id=str(uuid4()),
            amount=600,
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
            sender_wallet_id=user_id,
            recipient_wallet_id=recipient_id,
            uow=uow,
            auth_svc=pmt_acl.FakeAuthenticationService(),
        )

    tx_dtos = pmt_qry.payment_retools_get_all_transactions_of_selected_user(
        user_id=user_id,
        uow=uow,
    )

    assert len(tx_dtos) == 6
    assert pmt_mdl.TransactionStatus.FAILED in [
        pmt_mdl.TransactionStatus[tx_dto.status] for tx_dto in tx_dtos
    ]

    for tx_dto in tx_dtos:
        assert tx_dto.sender_id == user_id
        assert tx_dto.recipient_id == recipient_id
        assert pmt_mdl.TransactionType[tx_dto.transaction_type] == pmt_mdl.TransactionType.P2P_PUSH
        assert pmt_mdl.TransactionMode[tx_dto.mode] == pmt_mdl.TransactionMode.APP_TRANSFER

    uow.close_connection()


def test_payment_retools_get_vendors_and_balance(
    seed_two_verified_vendors_in_closed_loop, add_1000_wallet
):
    uow = UnitOfWork()
    vendor_1, vendor_2, closed_loop_id = seed_two_verified_vendors_in_closed_loop(uow)

    vendor_balance_dtos = pmt_qry.payment_retools_get_vendors_and_balance(
        closed_loop_id=closed_loop_id,
        uow=uow,
    )

    assert len(vendor_balance_dtos) == 0

    add_1000_wallet(wallet_id=vendor_1.wallet_id, uow=uow)
    add_1000_wallet(wallet_id=vendor_2.wallet_id, uow=uow)

    vendor_balance_dtos = pmt_qry.payment_retools_get_vendors_and_balance(
        closed_loop_id=closed_loop_id,
        uow=uow,
    )

    print(vendor_balance_dtos)
    assert len(vendor_balance_dtos) == 2
    for vendor_balance_dto in vendor_balance_dtos:
        assert vendor_balance_dto.id in [vendor_1.id, vendor_2.id]
        assert vendor_balance_dto.balance == 1000

    uow.close_connection()


def test_payment_retools_get_transactions_to_be_reconciled(
    seed_5_100_transactions_against_user_ids,
):
    uow = UnitOfWork()

    customer_id = str(uuid4())
    vendor_id = str(uuid4())
    seed_5_100_transactions_against_user_ids(
        sender_id=customer_id,
        recipient_id=vendor_id,
        uow=uow,
    )

    with pytest.raises(pmt_svc_ex.TransactionFailedException, match="Insufficient balance"):
        pmt_cmd._execute_transaction(
            tx_id=str(uuid4()),
            amount=600,
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
            sender_wallet_id=customer_id,
            recipient_wallet_id=vendor_id,
            uow=uow,
            auth_svc=pmt_acl.FakeAuthenticationService(),
        )

    tx_dtos = pmt_qry.payment_retools_get_transactions_to_be_reconciled(
        vendor_id=vendor_id,
        uow=uow,
    )

    assert len(tx_dtos) == 5
    for tx_dto in tx_dtos:
        assert tx_dto.sender_id == customer_id
        assert tx_dto.recipient_id == vendor_id
        assert tx_dto.amount == 100
        assert pmt_mdl.TransactionType[tx_dto.transaction_type] == pmt_mdl.TransactionType.P2P_PUSH
        assert pmt_mdl.TransactionMode[tx_dto.mode] == pmt_mdl.TransactionMode.APP_TRANSFER
        assert pmt_mdl.TransactionStatus[tx_dto.status] == pmt_mdl.TransactionStatus.SUCCESSFUL

    uow.close_connection()


def test_payment_retools_get_vendors(
    seed_two_verified_vendors_in_closed_loop, seed_verified_auth_user
):
    uow = UnitOfWork()
    vendor_1, vendor_2, closed_loop_id = seed_two_verified_vendors_in_closed_loop(uow)

    vendor_dtos = pmt_qry.payment_retools_get_vendors(
        closed_loop_id=closed_loop_id,
        uow=uow,
    )

    user, _ = seed_verified_auth_user(uow)
    auth_cmd.register_closed_loop(
        user_id=user.id,
        closed_loop_id=closed_loop_id,
        unique_identifier="1234",
        uow=uow,
        auth_svc=auth_acl.FakeAuthenticationService(),
    )

    fetched_vendor_ids = [vendor_dto.id for vendor_dto in vendor_dtos]
    fetched_vendor_names = [vendor_dto.full_name for vendor_dto in vendor_dtos]

    assert user.id not in fetched_vendor_ids
    assert len(vendor_dtos) == 2
    assert vendor_1.id in fetched_vendor_ids
    assert vendor_2.id in fetched_vendor_ids
    assert vendor_1.full_name in fetched_vendor_names
    assert vendor_2.full_name in fetched_vendor_names

    vendor_dtos = pmt_qry.payment_retools_get_vendors(
        closed_loop_id=closed_loop_id,
        uow=uow,
    )
    assert len(vendor_dtos) == 2

    uow.close_connection()

def test_payment_retools_get_reconciliation_history(
    seed_starred_wallet, seed_5_100_transactions_against_user_ids
):
    uow = UnitOfWork()

    customer_id = str(uuid4())
    vendor_id = str(uuid4())
    seed_starred_wallet(uow)

    seed_5_100_transactions_against_user_ids(
        sender_id=customer_id,
        recipient_id=vendor_id,
        uow=uow,
    )

    reconcilation_tx_id = str(uuid4())
    pmt_cmd.payment_retools_reconcile_vendor(
        tx_id=reconcilation_tx_id,
        vendor_wallet_id=vendor_id,
        uow=uow,
        auth_svc=pmt_acl.FakeAuthenticationService(),
        pmt_svc=pmt_acl.PaymentService(),
    )

    # again do 5 transactions from customer to vendor
    for i in range(5):
        pmt_cmd._execute_transaction(
            tx_id=str(uuid4()),
            amount=100,
            transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
            transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
            sender_wallet_id=customer_id,
            recipient_wallet_id=vendor_id,
            uow=uow,
            auth_svc=pmt_acl.FakeAuthenticationService(),
        )

    reconcilation_tx_id = str(uuid4())
    pmt_cmd.payment_retools_reconcile_vendor(
        tx_id=reconcilation_tx_id,
        vendor_wallet_id=vendor_id,
        uow=uow,
        auth_svc=pmt_acl.FakeAuthenticationService(),
        pmt_svc=pmt_acl.PaymentService(),
    )

    tx_dtos = pmt_qry.payment_retools_get_reconciliation_history(
        vendor_id=vendor_id,
        uow=uow,
    )

    assert len(tx_dtos) == 2
    assert tx_dtos[0].amount == 500
    assert tx_dtos[1].amount == 500

    uow.close_connection()


def test_get_user_wallet_id_and_type_from_qr_id(seed_verified_auth_user):
    uow = UnitOfWork()
    user, wallet = seed_verified_auth_user(uow)

    qr_id = wallet.qr_id

    user_id_and_type_dto = pmt_qry.get_user_wallet_id_and_type_from_qr_id(
        qr_id=qr_id,
        uow=uow,
    )

    assert user_id_and_type_dto.user_wallet_id == user.id
    assert user_id_and_type_dto.user_type == auth_mdl.UserType.CUSTOMER
    assert pmt_qry.get_user_wallet_id_and_type_from_qr_id(qr_id=str(uuid4()), uow=uow) is None

    uow.close_connection()


def test_get_all_vendor_id_name_and_qr_id_of_a_closed_loop(
    seed_two_verified_vendors_in_closed_loop, get_qr_id_from_user_id
):
    uow = UnitOfWork()
    vendor_1, vendor_2, closed_loop_id = seed_two_verified_vendors_in_closed_loop(uow)

    vendor_id_name_qr_id_dtos = pmt_qry.get_all_vendor_id_name_and_qr_id_of_a_closed_loop(
        closed_loop_id=closed_loop_id,
        uow=uow,
    )

    assert len(vendor_id_name_qr_id_dtos) == 2

    for i in range(2):
        assert vendor_id_name_qr_id_dtos[i].id in [vendor_1.id, vendor_2.id]
        assert vendor_id_name_qr_id_dtos[i].full_name in [
            vendor_1.full_name,
            vendor_2.full_name,
        ]
        assert vendor_id_name_qr_id_dtos[i].qr_id in [
            get_qr_id_from_user_id(vendor_1.id, uow),
            get_qr_id_from_user_id(vendor_2.id, uow),
        ]

    uow.close_connection()

def test_get_tx_balance_and_get_tx_recipient(seed_verified_auth_user, add_1000_wallet):
    uow = UnitOfWork()
    sender, _ = seed_verified_auth_user(uow)
    recipient, _ = seed_verified_auth_user(uow)

    add_1000_wallet(wallet_id=sender.id, uow=uow)
    tx_id = str(uuid4())
    pmt_cmd._execute_transaction(
        tx_id=tx_id,
        amount=100,
        transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
        sender_wallet_id=sender.id,
        recipient_wallet_id=recipient.id,
        uow=uow,
        auth_svc=pmt_acl.FakeAuthenticationService(),
    )

    assert (
        pmt_qry.get_tx_balance(
            tx_id=tx_id,
            uow=uow,
        )
        == 100
    )

    assert (
        pmt_qry.get_tx_recipient(
            tx_id=tx_id,
            uow=uow,
        )
        == recipient.id
    )
    uow.close_connection()



def test_get_last_deposit_transaction(seed_verified_auth_user, add_1000_wallet):
    uow = UnitOfWork()

    pg, _ = seed_verified_auth_user(uow)
    recipient, _ = seed_verified_auth_user(uow)
    add_1000_wallet(wallet_id=pg.id, uow=uow)

    tx_id = str(uuid4())
    pmt_cmd._execute_transaction(
        tx_id=tx_id,
        amount=100,
        transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
        sender_wallet_id=pg.id,
        recipient_wallet_id=recipient.id,
        uow=uow,
        auth_svc=pmt_acl.AuthenticationService(),
    )

    pp_tx_id = str(uuid4())
    tx = uow.transactions.get(transaction_id=tx_id)
    tx.add_paypro_id(paypro_id=pp_tx_id)
    uow.transactions.save(transaction=tx)

    tx = pmt_qry.get_last_deposit_transaction(user_id=recipient.id, uow=uow)

    assert tx.amount == 100
    assert tx.paypro_id == pp_tx_id
    assert tx.id == tx_id
    assert tx.status == pmt_mdl.TransactionStatus.PENDING
    assert tx.transaction_type == pmt_mdl.TransactionType.PAYMENT_GATEWAY

    uow.close_connection()
