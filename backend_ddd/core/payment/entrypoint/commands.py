"""Payments micro-service commands"""
import requests
import os
import logging
import json
from datetime import datetime, timedelta
from typing import List, Tuple
from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.domain import model as mdl
from core.authentication.domain import model as auth_mdl
from core.payment.domain import exceptions as pmt_mdl_ex
from core.authentication.entrypoint.commands import PAYPRO_USER_ID
from core.payment.entrypoint.exceptions import *
from . import utils
from time import sleep
from queue import Queue
from uuid import uuid4
from core.payment.entrypoint import anti_corruption as acl
from core.payment.entrypoint import anti_corruption as pmt_acl


# please only call this from create_user
def create_wallet(user_id: str, uow: AbstractUnitOfWork):
    """Create wallet"""
    qr_id = str(uuid4())
    wallet = mdl.Wallet(id=user_id, qr_id=qr_id, balance=0)
    uow.transactions.add_wallet(wallet)


def _execute_transaction(
    tx_id: str,
    amount: int,
    transaction_mode: mdl.TransactionMode,
    transaction_type: mdl.TransactionType,
    sender_wallet_id: str,
    recipient_wallet_id: str,
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
):
    with uow:
        if not auth_svc.user_verification_status_from_user_id(
            user_id=sender_wallet_id, uow=uow
        ):
            raise NotVerifiedException("User is not verified")
        if not auth_svc.user_verification_status_from_user_id(
            user_id=recipient_wallet_id, uow=uow
        ):
            raise NotVerifiedException("User is not verified")

        txn_time = datetime.now()
        tx = uow.transactions.get_wallets_create_transaction(
            id=tx_id,
            amount=amount,
            created_at=txn_time,
            last_updated=txn_time,
            mode=transaction_mode,
            transaction_type=transaction_type,
            status=mdl.TransactionStatus.PENDING,
            sender_wallet_id=sender_wallet_id,
            recipient_wallet_id=recipient_wallet_id,
        )

        if utils.is_instant_transaction(transaction_type=transaction_type):
            try:
                tx.execute_transaction()
            except pmt_mdl_ex.TransactionNotAllowedException as e:
                uow.transactions.save(tx)
                raise TransactionFailedException(str(e))

            uow.transactions.save(tx)

        uow.transactions.save(tx)


def execute_cashback_transaction(
    recipient_wallet_id: str,
    cashback_amount: int,
    uow: AbstractUnitOfWork,
    auth_svc: pmt_acl.AbstractAuthenticationService,
    pmt_svc: acl.AbstractPaymentService,
):
    sender_wallet_id = pmt_svc.get_starred_wallet_id(uow=uow)

    _execute_transaction(
        tx_id=str(uuid4()),
        sender_wallet_id=sender_wallet_id,  # This will be a fixed cardpay wallet id
        recipient_wallet_id=recipient_wallet_id,
        amount=cashback_amount,
        transaction_mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.CASH_BACK,
        uow=uow,
        auth_svc=auth_svc,
    )


def execute_transaction_unique_identifier(
    tx_id: str,
    sender_unique_identifier: str,
    recipient_unique_identifier: str,
    closed_loop_id: str,
    amount: int,
    transaction_mode: mdl.TransactionMode,
    transaction_type: mdl.TransactionType,
    uow: AbstractUnitOfWork,
    auth_svc: acl.AbstractAuthenticationService,
    pmt_svc: acl.AbstractPaymentService,
):
    with uow:
        sender_wallet_id = pmt_svc.get_wallet_id_from_unique_identifier(
            unique_identifier=sender_unique_identifier,
            closed_loop_id=closed_loop_id,
            uow=uow,
        )
        recipient_wallet_id = pmt_svc.get_wallet_id_from_unique_identifier(
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


# ## for testing purposes only
# #def slow_execute_transaction(
# #    sender_wallet_id: str,
# #    recipient_wallet_id: str,
# #    amount: int,
# #    transaction_mode: mdl.TransactionMode,
# #    transaction_type: mdl.TransactionType,
# #    uow: AbstractUnitOfWork,
# #    queue: Queue,
# #):
# #    with uow:
# #        # using wallet id as txn does not exist yet
# #        tx = uow.transactions.get_wallets_create_transaction(
# #            amount=amount,
# #            mode=transaction_mode,
# #            transaction_type=transaction_type,
# #            sender_wallet_id=sender_wallet_id,
# #            recipient_wallet_id=recipient_wallet_id,
# #        )
# #        sleep(1)
# #        if utils.is_instant_transaction(transaction_type=transaction_type):
# #            tx.execute_transaction()

# #        uow.transactions.save(tx)

# #    uow.commit_close_connection()

# #    queue.put(tx)


def accept_p2p_pull_transaction(
    transaction_id: str,
    uow: AbstractUnitOfWork,
    auth_svc: pmt_acl.AbstractAuthenticationService,
):
    with uow:
        tx = uow.transactions.get(transaction_id=transaction_id)
        try:
            tx.accept_p2p_pull_transaction()
        except pmt_mdl_ex.TransactionNotAllowedException as e:
            uow.transactions.save(tx)
            raise TransactionFailedException(str(e))

        uow.transactions.save(tx)


def accept_payment_gateway_transaction(
    transaction_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        tx = uow.transactions.get(transaction_id=transaction_id)
        tx.execute_transaction()
        uow.transactions.save(tx)


def decline_p2p_pull_transaction(transaction_id: str, uow: AbstractUnitOfWork):
    with uow:
        tx = uow.transactions.get(transaction_id=transaction_id)
        tx.decline_p2p_pull_transaction()
        uow.transactions.save(tx)


def generate_voucher(
    tx_id: str, sender_wallet_id: str, amount: int, uow: AbstractUnitOfWork
):
    """creates a txn object whith same sender and recipient"""

    txn_time = datetime.now()
    tx = uow.transactions.get_wallets_create_transaction(
        id=tx_id,
        amount=amount,
        mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.VOUCHER,
        sender_wallet_id=sender_wallet_id,
        recipient_wallet_id=sender_wallet_id,
        created_at=txn_time,
        last_updated=txn_time,
        status=mdl.TransactionStatus.PENDING,
    )
    uow.transactions.save(tx)


# transaction_id ~= voucher_id
def redeem_voucher(
    recipient_wallet_id: str, transaction_id: str, uow: AbstractUnitOfWork
):
    with uow:
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
) -> str:
    user = uow.users.get(user_id=user_id)

    if amount < 1000:
        raise DepositAmountTooSmallException(
            "Deposit amount is less than the minimum allowed deposit"
        )

    _execute_transaction(
        tx_id=tx_id,
        sender_wallet_id=PAYPRO_USER_ID,
        recipient_wallet_id=user_id,
        amount=amount,
        transaction_mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.PAYMENT_GATEWAY,
        uow=uow,
        auth_svc=auth_svc,
    )

    checkout_url = get_deposit_checkout_url(
        amount=amount,
        transaction_id=tx_id,
        full_name=user.full_name,
        phone_number=user.phone_number.value,
        email=user.personal_email.value,
        uow=uow,
    )

    return checkout_url


def _payment_gateway_use_cases():
    """
    Payment Gateway integration
    PayPro
    """


def get_deposit_checkout_url(
    amount: int,
    transaction_id: str,
    full_name: str,
    phone_number: str,
    email: str,
    uow: AbstractUnitOfWork,
) -> str:
    auth_token = _get_paypro_auth_token(uow=uow)

    now = datetime.now()
    date_hour_later = now + timedelta(hours=1)

    config = {
        "method": "post",
        "url": f"{os.environ.get('PAYPRO_BASE_URL')}/v2/ppro/co",
        "headers": {
            "token": auth_token,
        },
        "data": [
            {
                "MerchantId": os.environ.get("USERNAME"),
            },
            {
                "OrderNumber": transaction_id,
                "OrderAmount": amount,
                "OrderDueDate": date_hour_later.isoformat(),
                "OrderType": "Service",
                "IssueDate": now.isoformat(),
                "OrderExpireAfterSeconds": 60 * 60,
                "CustomerName": full_name,
                "CustomerMobile": phone_number,
                "CustomerEmail": email,
                "CustomerAddress": "",
            },
        ],
    }

    # pp_order_res = requests.request(**config)
    pp_order_res = requests.post(
        config["url"],
        headers=config["headers"],
        data=json.dumps(
            config["data"],
        ),
    )
    pp_order_res.raise_for_status()

    response_data = pp_order_res.json()[1]

    try:
        payment_url = response_data["Click2Pay"]
    except:
        raise PaymentUrlNotFoundException(
            "PayPro response does not contain payment url, please try again"
        )

    return payment_url


def _get_paypro_auth_token(uow: AbstractUnitOfWork) -> str:
    with uow:
        sql = """
           select token, last_updated
           from payment_gateway_tokens
           where id = %s
           for update
       """
        uow.cursor.execute(
            sql,
            [os.environ.get("CLIENT_ID")],
        )
        row = uow.cursor.fetchone()

    if row is not None:
        last_updated: datetime = row[1]
        now = datetime.now()
        time_difference = now - last_updated

        token_validity = os.environ.get("TOKEN_VALIDITY")
        if token_validity is None:
            token_validity = 5 * 60 * 1000

        if time_difference < timedelta(milliseconds=float(token_validity)):
            logging.info(
                {
                    "message": "Using an already generated token from database",
                    "token": row[0],
                    "time_difference (mins:secs)": _get_min_sec_repr_of_timedelta(
                        time_difference
                    ),
                },
            )
            return row[0]

    # Generate new token

    config = {
        "method": "post",
        "url": f"{os.environ.get('PAYPRO_BASE_URL')}/v2/ppro/auth",
        "headers": {},
        "data": {
            "clientid": os.environ.get("CLIENT_ID"),
            "clientsecret": os.environ.get("CLIENT_SECRET"),
        },
    }

    pp_auth_res = requests.request(**config)
    pp_auth_res.raise_for_status()

    auth_token = pp_auth_res.headers.get("token")
    if auth_token is None:
        raise Exception("No auth token returned from PayPro's api")

    with uow:
        sql = """
           insert into payment_gateway_tokens (id, token, last_updated)
           values (%s, %s, %s)
           on conflict (id) do update set
               id = excluded.id,
               token = excluded.token,
               last_updated = excluded.last_updated
       """
        uow.cursor.execute(
            sql,
            [
                os.environ.get("CLIENT_ID"),
                auth_token,
                datetime.now(),
            ],
        )

    logging.info(
        {
            "message": "PayPro new token generated and persisted in db",
            "token": auth_token,
            "metadata": pp_auth_res.json(),
        },
    )

    return auth_token


def pay_pro_callback(
    user_name: str,
    password: str,
    csv_invoice_ids: str,
    uow: AbstractUnitOfWork,
) -> Tuple[List[str], List[str]]:
    if user_name != os.environ.get("PAYPRO_USERNAME") or password != os.environ.get(
        "PAYPRO_PASSWORD"
    ):
        raise InvalidPayProCredentialsException("PayPro credentials are invalid")

    invoice_ids = csv_invoice_ids.split(",")
    invoice_ids = [id.strip() for id in invoice_ids]

    if len(invoice_ids) == 1 and invoice_ids[0] == "":
        return [], []

    not_found_invoice_ids = []
    success_invoice_ids = []

    for id in invoice_ids:
        try:
            accept_payment_gateway_transaction(
                transaction_id=id,
                uow=uow,
            )
            success_invoice_ids.append(id)
        except pmt_mdl_ex.TransactionNotFoundException:
            not_found_invoice_ids.append(id)

    return success_invoice_ids, not_found_invoice_ids


def _get_min_sec_repr_of_timedelta(td: timedelta):
    total_seconds = int(td.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)

    return f"{minutes}:{seconds:02d}"


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
        transaction_mode=mdl.TransactionMode.APP_TRANSFER,
        transaction_type=mdl.TransactionType.RECONCILIATION,
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
        raise InvalidQRVersionException("Invalid QR version")

    user_info = pmt_svc.get_user_wallet_id_and_type_from_qr_id(
        qr_id=recipient_qr_id,
        uow=uow,
    )

    transaction_type = mdl.TransactionType.VIRTUAL_POS

    if user_info is None:
        raise InvalidQRCodeException("Invalid QR code")

    elif user_info.user_type == auth_mdl.UserType.VENDOR:
        transaction_type = mdl.TransactionType.VIRTUAL_POS

    elif user_info.user_type == auth_mdl.UserType.CUSTOMER:
        transaction_type = mdl.TransactionType.P2P_PUSH

    else:
        raise InvalidUserTypeException("Invalid user type")

    _execute_transaction(
        tx_id=tx_id,
        amount=amount,
        sender_wallet_id=sender_wallet_id,
        recipient_wallet_id=user_info.user_wallet_id,
        transaction_mode=mdl.TransactionMode.QR,
        transaction_type=transaction_type,
        uow=uow,
        auth_svc=auth_svc,
    )
