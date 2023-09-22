"""Payments micro-service commands"""
from datetime import datetime
from uuid import uuid4

from core.authentication.domain import model as auth_mdl
from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.domain import exceptions as mdl_ex
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as acl
from core.payment.entrypoint import exceptions as svc_ex
from core.payment.entrypoint import utils

PAYPRO_USER_ID = "bd85b580-9510-4596-afc4-b737eeb3d492"


# please only call this from create_user
def create_wallet(user_id: str, uow: AbstractUnitOfWork):
    """Create wallet command"""
    qr_id = str(uuid4())
    wallet = pmt_mdl.Wallet(id=user_id, qr_id=qr_id, balance=0)
    uow.transactions.add_wallet(wallet)


def _execute_transaction(
    tx_id: str,
    amount: int,
    transaction_mode: pmt_mdl.TransactionMode,
    transaction_type: pmt_mdl.TransactionType,
    sender_wallet_id: str,
    recipient_wallet_id: str,
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
):
    if not auth_svc.user_verification_status_from_user_id(user_id=sender_wallet_id, uow=uow):
        raise svc_ex.NotVerifiedException("User is not verified")
    if not auth_svc.user_verification_status_from_user_id(user_id=recipient_wallet_id, uow=uow):
        raise svc_ex.NotVerifiedException("User is not verified")

    txn_time = datetime.now()
    tx = uow.transactions.get_wallets_create_transaction(
        id=tx_id,
        amount=amount,
        created_at=txn_time,
        last_updated=txn_time,
        mode=transaction_mode,
        transaction_type=transaction_type,
        status=pmt_mdl.TransactionStatus.PENDING,
        sender_wallet_id=sender_wallet_id,
        recipient_wallet_id=recipient_wallet_id,
    )

    if utils.is_instant_transaction(transaction_type=transaction_type):
        try:
            tx.execute_transaction()
        except mdl_ex.TransactionNotAllowedException as e:
            uow.transactions.save(tx)
            raise svc_ex.TransactionFailedException(str(e))

        uow.transactions.save(tx)

    uow.transactions.save(tx)


def execute_cashback_transaction(
    recipient_wallet_id: str,
    cashback_amount: int,
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
    pmt_svc: acl.AbstractPaymentService,
):
    sender_wallet_id = pmt_svc.get_starred_wallet_id(uow=uow)

    _execute_transaction(
        tx_id=str(uuid4()),
        sender_wallet_id=sender_wallet_id,  # This will be a fixed cardpay wallet id
        recipient_wallet_id=recipient_wallet_id,
        amount=cashback_amount,
        transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.CASH_BACK,
        uow=uow,
        auth_svc=auth_svc,
    )


def execute_transaction_unique_identifier(
    tx_id: str,
    sender_unique_identifier: str,
    recipient_unique_identifier: str,
    closed_loop_id: str,
    amount: int,
    transaction_mode: pmt_mdl.TransactionMode,
    transaction_type: pmt_mdl.TransactionType,
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
    pmt_svc: acl.AbstractPaymentService,
):
    sender_wallet_id = pmt_svc.get_wallet_id_from_unique_identifier_and_closed_loop_id(
        unique_identifier=sender_unique_identifier,
        closed_loop_id=closed_loop_id,
        uow=uow,
    )
    recipient_wallet_id = pmt_svc.get_wallet_id_from_unique_identifier_and_closed_loop_id(
        unique_identifier=recipient_unique_identifier,
        closed_loop_id=closed_loop_id,
        uow=uow,
    )
    sender_wallet_id = pmt_svc.get_wallet_id_from_unique_identifier_and_closed_loop_id(
        unique_identifier=sender_unique_identifier,
        closed_loop_id=closed_loop_id,
        uow=uow,
    )
    recipient_wallet_id = pmt_svc.get_wallet_id_from_unique_identifier_and_closed_loop_id(
        unique_identifier=recipient_unique_identifier,
        closed_loop_id=closed_loop_id,
        uow=uow,
    )

    _execute_transaction(
        tx_id=tx_id,
        amount=amount,
        sender_wallet_id=sender_wallet_id,
        recipient_wallet_id=recipient_wallet_id,
        transaction_mode=transaction_mode,
        transaction_type=transaction_type,
        uow=uow,
        auth_svc=auth_svc,
    )


def accept_p2p_pull_transaction(
    transaction_id: str,
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
):
    tx = uow.transactions.get(transaction_id=transaction_id)
    try:
        tx.accept_p2p_pull_transaction()
    except mdl_ex.TransactionNotAllowedException as e:
        uow.transactions.save(tx)
        raise svc_ex.TransactionFailedException(str(e))

    uow.transactions.save(tx)
    uow.transactions.save(tx)


def accept_payment_gateway_transaction(
    transaction_id: str,
    uow: AbstractUnitOfWork,
):
    tx = uow.transactions.get(transaction_id=transaction_id)
    tx.execute_transaction()
    uow.transactions.save(tx)
    tx = uow.transactions.get(transaction_id=transaction_id)
    tx.execute_transaction()
    uow.transactions.save(tx)


def decline_p2p_pull_transaction(transaction_id: str, uow: AbstractUnitOfWork):
    tx = uow.transactions.get(transaction_id=transaction_id)
    tx.decline_p2p_pull_transaction()
    uow.transactions.save(tx)
    tx = uow.transactions.get(transaction_id=transaction_id)
    tx.decline_p2p_pull_transaction()
    uow.transactions.save(tx)


def generate_voucher(tx_id: str, sender_wallet_id: str, amount: int, uow: AbstractUnitOfWork):
    """creates a txn object whith same sender and recipient"""

    txn_time = datetime.now()
    tx = uow.transactions.get_wallets_create_transaction(
        id=tx_id,
        amount=amount,
        mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.VOUCHER,
        sender_wallet_id=sender_wallet_id,
        recipient_wallet_id=sender_wallet_id,
        created_at=txn_time,
        last_updated=txn_time,
        status=pmt_mdl.TransactionStatus.PENDING,
    )
    uow.transactions.save(tx)


# transaction_id ~= voucher_id
def redeem_voucher(recipient_wallet_id: str, transaction_id: str, uow: AbstractUnitOfWork):
    tx = uow.transactions.get_with_different_recipient(
        transaction_id=transaction_id, recipient_wallet_id=recipient_wallet_id
    )
    tx.redeem_voucher()
    uow.transactions.save(tx)


def create_deposit_request(
    tx_id: str,
    user_id: str,
    amount: int,
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
    pp_svc: acl.AbstractPayproService,
) -> str:
    user = uow.users.get(user_id=user_id)

    if amount < 1000:
        raise svc_ex.DepositAmountTooSmallException(
            "Deposit amount is less than the minimum allowed deposit"
        )

    _execute_transaction(
        tx_id=tx_id,
        sender_wallet_id=PAYPRO_USER_ID,
        recipient_wallet_id=user_id,
        amount=amount,
        transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
        uow=uow,
        auth_svc=auth_svc,
    )

    checkout_url = pp_svc.get_deposit_checkout_url(
        amount=amount,
        transaction_id=tx_id,
        full_name=user.full_name,
        phone_number=user.phone_number.value,
        email=user.personal_email.value,
        uow=uow,
    )

    return checkout_url


def payment_retools_reconcile_vendor(
    tx_id: str,
    uow: AbstractUnitOfWork,
    vendor_wallet_id: str,
    auth_svc: acl.AbstractAuthenticationService,
    pmt_svc: acl.AbstractPaymentService,
):
    vendor_balance = pmt_svc.get_wallet_balance(
        wallet_id=vendor_wallet_id,
        uow=uow,
    )
    card_pay_wallet_id = pmt_svc.get_starred_wallet_id(
        uow=uow,
    )

    _execute_transaction(
        tx_id=tx_id,
        sender_wallet_id=vendor_wallet_id,
        recipient_wallet_id=card_pay_wallet_id,
        amount=vendor_balance,
        transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.RECONCILIATION,
        uow=uow,
        auth_svc=auth_svc,
    )


def execute_qr_transaction(
    tx_id: str,
    amount: int,
    sender_wallet_id: str,
    recipient_qr_id: str,
    version: int,
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
    pmt_svc: acl.AbstractPaymentService,
):
    if version != 1:
        raise svc_ex.InvalidQRVersionException("Invalid QR version")

    user_info = pmt_svc.get_user_wallet_id_and_type_from_qr_id(
        qr_id=recipient_qr_id,
        uow=uow,
    )

    transaction_type = pmt_mdl.TransactionType.VIRTUAL_POS

    if user_info is None:
        raise svc_ex.InvalidQRCodeException("Invalid QR code")

    elif user_info.user_type == auth_mdl.UserType.VENDOR:
        transaction_type = pmt_mdl.TransactionType.VIRTUAL_POS

    elif user_info.user_type == auth_mdl.UserType.CUSTOMER:
        transaction_type = pmt_mdl.TransactionType.P2P_PUSH

    else:
        raise svc_ex.InvalidUserTypeException("Invalid user type")

    _execute_transaction(
        tx_id=tx_id,
        amount=amount,
        sender_wallet_id=sender_wallet_id,
        recipient_wallet_id=user_info.user_wallet_id,
        transaction_mode=pmt_mdl.TransactionMode.QR,
        transaction_type=transaction_type,
        uow=uow,
        auth_svc=auth_svc,
    )
