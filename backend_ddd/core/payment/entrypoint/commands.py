"""Payments micro-service commands"""
import requests
import os
import logging
import json
from datetime import datetime, timedelta
from typing import List, Tuple
from core.entrypoint.uow import AbstractUnitOfWork
from ..domain.model import (
    Transaction,
    Wallet,
    TransactionMode,
    TransactionType,
)
from ..entrypoint.queries import get_wallet_id_from_unique_identifier
from ...payment.domain.model import TransactionType, TransactionMode
from core.marketing.entrypoint import commands as mktg_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.domain import model as auth_mdl
from core.payment.domain import exceptions as pmt_mdl_exc
from core.authentication.entrypoint.commands import PAYPRO_USER_ID
from core.payment.entrypoint.exceptions import *
from . import utils
from time import sleep
from queue import Queue
from ..entrypoint import queries as payment_qry
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

# please only call this from create_user
def create_wallet(user_id: str, uow: AbstractUnitOfWork) -> Wallet:
    """Create wallet"""
    qr_id = str(uuid4())
    wallet = Wallet(id=user_id, qr_id=qr_id)
    uow.transactions.add_wallet(wallet)

    return wallet


def execute_transaction_unique_identifier(
    sender_unique_identifier: str,
    recipient_unique_identifier: str,
    closed_loop_id: str,
    amount: int,
    transaction_mode: TransactionMode,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
) -> Transaction:
    with uow:
        sender_wallet_id = get_wallet_id_from_unique_identifier(
            unique_identifier=sender_unique_identifier,
            closed_loop_id=closed_loop_id,
            uow=uow,
        )
        recipient_wallet_id = get_wallet_id_from_unique_identifier(
            unique_identifier=recipient_unique_identifier,
            closed_loop_id=closed_loop_id,
            uow=uow,
        )

    tx = execute_transaction(
        sender_wallet_id=sender_wallet_id,
        recipient_wallet_id=recipient_wallet_id,
        amount=amount,
        transaction_mode=transaction_mode,
        transaction_type=transaction_type,
        uow=uow,
    )

    return tx


def execute_transaction(
    sender_wallet_id: str,
    recipient_wallet_id: str,
    amount: int,
    transaction_mode: TransactionMode,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
) -> Transaction:
    with uow:
        if not auth_qry.user_verification_status_from_user_id(
            user_id=sender_wallet_id, uow=uow
        ):
            raise NotVerifiedException("User is not verified")
        if not auth_qry.user_verification_status_from_user_id(
            user_id=recipient_wallet_id, uow=uow
        ):
            raise NotVerifiedException("User is not verified")

        tx = uow.transactions.get_wallets_create_transaction(
            amount=amount,
            mode=transaction_mode,
            transaction_type=transaction_type,
            sender_wallet_id=sender_wallet_id,
            recipient_wallet_id=recipient_wallet_id,
        )

        if utils.is_instant_transaction(transaction_type=transaction_type):
            try:
                tx.execute_transaction()
            except pmt_mdl_exc.TransactionNotAllowedException as e:
                uow.transactions.save(tx)
                raise TransactionFailedException(str(e))

            uow.transactions.save(tx)
            mktg_cmd.add_loyalty_points(
                sender_wallet_id=sender_wallet_id,
                recipient_wallet_id=recipient_wallet_id,
                transaction_amount=amount,
                transaction_type=transaction_type,
                uow=uow,
            )
            mktg_cmd.give_cashback(
                recipient_wallet_id=recipient_wallet_id,
                deposited_amount=amount,
                transaction_type=transaction_type,
                uow=uow,
            )

        uow.transactions.save(tx)

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
        if utils.is_instant_transaction(transaction_type=transaction_type):
            tx.execute_transaction()

        uow.transactions.save(tx)

    uow.commit_close_connection()

    queue.put(tx)


def accept_p2p_pull_transaction(
    transaction_id: str, uow: AbstractUnitOfWork
) -> Transaction:
    with uow:
        tx = uow.transactions.get(transaction_id=transaction_id)
        try:
            tx.accept_p2p_pull_transaction()
        except pmt_mdl_exc.TransactionNotAllowedException as e:
            uow.transactions.save(tx)
            raise TransactionFailedException(str(e))

        uow.transactions.save(tx)

        mktg_cmd.add_loyalty_points(
            sender_wallet_id=tx.sender_wallet.id,
            recipient_wallet_id=tx.recipient_wallet.id,
            transaction_amount=tx.amount,
            transaction_type=tx.transaction_type,
            uow=uow,
        )
        mktg_cmd.give_cashback(
            recipient_wallet_id=tx.recipient_wallet.id,
            deposited_amount=tx.amount,
            transaction_type=tx.transaction_type,
            uow=uow,
        )

    return tx


def accept_payment_gateway_transaction(
    transaction_id: str, uow: AbstractUnitOfWork
) -> Transaction:
    with uow:
        tx = uow.transactions.get(transaction_id=transaction_id)
        tx.execute_transaction()
        uow.transactions.save(tx)

        mktg_cmd.add_loyalty_points(
            sender_wallet_id=tx.sender_wallet.id,
            recipient_wallet_id=tx.recipient_wallet.id,
            transaction_amount=tx.amount,
            transaction_type=tx.transaction_type,
            uow=uow,
        )
        mktg_cmd.give_cashback(
            recipient_wallet_id=tx.recipient_wallet.id,
            deposited_amount=tx.amount,
            transaction_type=tx.transaction_type,
            uow=uow,
        )

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


def create_deposit_request(
    user_id: str,
    amount: int,
    uow: AbstractUnitOfWork,
) -> str:
    with uow:
        user = uow.users.get(user_id=user_id)

    if amount < 1000:
        raise DepositAmountTooSmallException(
            "Deposit amount is less than the minimum allowed deposit"
        )

    tx = execute_transaction(
        sender_wallet_id=PAYPRO_USER_ID,
        recipient_wallet_id=user_id,
        amount=amount,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.PAYMENT_GATEWAY,
        uow=uow,
    )

    checkout_url = get_deposit_checkout_url(
        amount=amount,
        transaction_id=tx.id,
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
    # TODO: remove in production
    # return "123"

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
    # TODO: remove in production
    # return "123"

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
    user_name: str, password: str, csv_invoice_ids: str, uow: AbstractUnitOfWork
) -> Tuple[List[str], List[str]]:
    if user_name != os.environ.get("PAYPRO_USERNAME") and password != os.environ.get(
        "PAYPRO_PASSWORD"
    ):
        raise InvalidPayProCredentialsException("PayPro credentials are invalid")

    invoice_ids = csv_invoice_ids.split(",")
    not_found_invoice_ids = []
    success_invoice_ids = []

    for id in invoice_ids:
        try:
            accept_payment_gateway_transaction(transaction_id=id, uow=uow)
            success_invoice_ids.append(id)
        except pmt_mdl_exc.TransactionNotFoundException:
            not_found_invoice_ids.append(id)

    return success_invoice_ids, not_found_invoice_ids


def _get_min_sec_repr_of_timedelta(td: timedelta):
    total_seconds = int(td.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)

    return f"{minutes}:{seconds:02d}"


def payment_retools_reconcile_vendor(
    uow: AbstractUnitOfWork,
    vendor_wallet_id: str,
):
    vendor_balance = payment_qry.get_wallet_balance(
        wallet_id=vendor_wallet_id,
        uow=uow,
    )
    card_pay_wallet_id = payment_qry.get_starred_wallet_id(
        uow=uow,
    )[0]

    execute_transaction(
        sender_wallet_id=vendor_wallet_id,
        recipient_wallet_id=card_pay_wallet_id,
        amount=vendor_balance,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.RECONCILIATION,
        uow=uow,
    )

    return


def execute_qr_transaction(
    sender_wallet_id: str,
    recipient_qr_id: str,
    amount: int,
    version: int,
    uow: AbstractUnitOfWork,
) -> Transaction:
    
    if version != 1:
        raise InvalidQRVersionException("Invalid QR version")

    user_info = payment_qry.get_user_wallet_id_and_type_from_qr_id(
        qr_id=recipient_qr_id,
        uow=uow,
    )

    transaction_type = TransactionType.VIRTUAL_POS

    if user_info is None:
        raise InvalidQRCodeException("Invalid QR code")

    elif user_info.user_type == auth_mdl.UserType.VENDOR:
        transaction_type = TransactionType.VIRTUAL_POS

    elif user_info.user_type == auth_mdl.UserType.CUSTOMER:
        transaction_type = TransactionType.P2P_PUSH

    else:
        raise InvalidUserTypeException("Invalid user type")

    tx = execute_transaction(
        sender_wallet_id=sender_wallet_id,
        recipient_wallet_id=user_info.user_wallet_id,
        amount=amount,
        transaction_mode=TransactionMode.QR,
        transaction_type=transaction_type,
        uow=uow,
    )

    return tx
