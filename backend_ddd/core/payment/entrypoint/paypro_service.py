"""Payments micro-service commands"""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Tuple

import requests
from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.domain import exceptions as pmt_mdl_ex
from core.payment.entrypoint import commands as cmd
from core.payment.entrypoint import utils
from core.payment.entrypoint.exceptions import *


def _get_paypro_auth_token(uow: AbstractUnitOfWork) -> str:
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
                    "time_difference (mins:secs)": utils.get_min_sec_repr_of_timedelta(
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


def get_deposit_checkout_url(
    amount: int,
    transaction_id: str,
    full_name: str,
    phone_number: str,
    email: str,
    uow: AbstractUnitOfWork,
) -> str:
    auth_token = _get_paypro_auth_token(uow=uow)

    now = datetime.now(tz=None)
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
            cmd.accept_payment_gateway_transaction(
                transaction_id=id,
                uow=uow,
            )
            success_invoice_ids.append(id)
        except pmt_mdl_ex.TransactionNotFoundException:
            not_found_invoice_ids.append(id)

    return success_invoice_ids, not_found_invoice_ids
