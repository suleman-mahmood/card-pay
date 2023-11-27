"""Payments micro-service commands"""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import requests
from core.entrypoint.uow import AbstractUnitOfWork, PaymentGatewayUnitOfWork
from core.payment.domain import exceptions as pmt_mdl_ex
from core.payment.entrypoint import commands as cmd
from core.payment.entrypoint import exceptions as ex
from core.payment.entrypoint import utils
from core.payment.entrypoint import view_models as vm

REQUEST_TIMEOUT = 10  # in seconds


def _get_paypro_auth_token() -> str:
    uow: AbstractUnitOfWork = PaymentGatewayUnitOfWork()

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
            uow.close_connection()
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

    try:
        pp_auth_res = requests.request(**config, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout as e:
        uow.close_connection()
        raise e

    pp_auth_res.raise_for_status()

    auth_token = pp_auth_res.headers.get("token")
    if auth_token is None:
        uow.close_connection()
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
    uow.commit_close_connection()

    logging.info(
        {
            "message": "PayPro new token generated and persisted in db",
            "token": auth_token,
            "metadata": pp_auth_res.json(),
        },
    )
    return auth_token


def register_customer_paypro(consumer_id: str):
    auth_token = _get_paypro_auth_token()

    config = {
        "method": "post",
        "url": f"{os.environ.get('PAYPRO_BASE_URL')}/v2/ppro/cmc",
        "headers": {
            "token": auth_token,
        },
        "data": [
            {
                "MerchantId": os.environ.get("USERNAME"),
            },
            {"ConsumerID": consumer_id, "Name": "", "Mobile": "", "Email": "", "Address": ""},
        ],
    }

    logging.info(
        {
            "message": "Trying to generate static invoice from PayPro",
            "config": config,
        },
    )

    pp_order_res = requests.post(
        config["url"],
        headers=config["headers"],
        data=json.dumps(
            config["data"],
        ),
        timeout=REQUEST_TIMEOUT,
    )

    logging.info(
        {
            "message": "PayPro Static ID Registered",
            "pp_order_res": pp_order_res.json(),
        },
    )

    response_data = pp_order_res.json()[1]

    try:
        consumer_id = response_data["FullConsumerId"]
    except KeyError as e:
        raise ex.ConsumerAlreadyExists("Consumer ID already exists")


def get_deposit_checkout_url_and_paypro_id(
    amount: int,
    transaction_id: str,
    full_name: str,
    phone_number: str,
    email: str,
    consumer_id: Optional[str],
) -> Tuple[str, str]:
    auth_token = _get_paypro_auth_token()

    pk_time = datetime.now() + timedelta(hours=5)
    hour_ahead = pk_time + timedelta(hours=1)

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
                "OrderDueDate": hour_ahead.isoformat(),
                "OrderType": "Service",
                "IssueDate": pk_time.isoformat(),
                "OrderExpireAfterSeconds": 60 * 60,
                "ReusableConsumerId": consumer_id,
                "CustomerName": full_name,
                "CustomerMobile": phone_number,
                "CustomerEmail": email,
                "CustomerAddress": "",
            },
        ],
    }
    if consumer_id is None:
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
                    "OrderDueDate": hour_ahead.isoformat(),
                    "OrderType": "Service",
                    "IssueDate": pk_time.isoformat(),
                    "OrderExpireAfterSeconds": 60 * 60,
                    "CustomerName": full_name,
                    "CustomerMobile": phone_number,
                    "CustomerEmail": email,
                    "CustomerAddress": "",
                },
            ],
        }

    logging.info(
        {
            "message": "Trying to generate deposit invoice from PayPro",
            "config": config,
        },
    )

    pp_order_res = requests.post(
        config["url"],
        headers=config["headers"],
        data=json.dumps(
            config["data"],
        ),
        timeout=REQUEST_TIMEOUT,
    )

    pp_order_res.raise_for_status()

    logging.info(
        {
            "message": "PayPro invoice generated",
            "pp_order_res": pp_order_res.json(),
        },
    )

    response_data = pp_order_res.json()[1]

    try:
        payment_url = response_data["Click2Pay"]
        paypro_id = response_data["PayProId"]
    except KeyError:
        logging.info(
            {
                "message": "PayPro invoice doesn't contain deposit checkout link",
                "pp_order_res": response_data,
            },
        )
        raise ex.PaymentUrlNotFoundException(
            "PayPro response does not contain payment url, please try again"
        )

    return payment_url, paypro_id


# TODO: Move this to payments commands
def pay_pro_callback(
    user_name: str,
    password: str,
    csv_invoice_ids: str,
    uow: AbstractUnitOfWork,
) -> Tuple[List[str], List[str]]:
    # TODO: fix this ASAP
    # user_name_mis_match = user_name != os.environ.get("PAYPRO_USERNAME")
    user_name_mis_match = False

    password_mis_match = password != os.environ.get("PAYPRO_PASSWORD")

    if user_name_mis_match or password_mis_match:
        raise ex.InvalidPayProCredentialsException("PayPro credentials are invalid")

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
        except pmt_mdl_ex.TransactionNotAllowedException as e:
            logging.info(
                {
                    "message": "Pay Pro | Callback",
                    "exception_msg": str(e),
                },
            )

    return success_invoice_ids, not_found_invoice_ids


def invoice_paid(paypro_id: str) -> bool:
    auth_token = _get_paypro_auth_token()
    config = {
        "method": "get",
        "url": f"{os.environ.get('PAYPRO_BASE_URL')}/v2/ppro/ggos",
        "data": json.dumps(
            {
                "Username": os.environ.get("USERNAME"),
                "Cpayid": paypro_id,
            }
        ),
        "headers": {
            "token": auth_token,
        },
    }

    logging.info(
        {
            "message": "Trying to get invoice status from PayPro",
            "config": config,
        },
    )

    try:
        pp_res = requests.request(**config, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise ex.PayProsCreateOrderTimedOut("PayPro's request timed out, retry again please!")

    pp_res.raise_for_status()

    logging.info(
        {
            "message": "PayPro invoice generated",
            "pp_order_res": pp_res.json(),
        },
    )

    response_data = pp_res.json()[1]

    try:
        order_status = response_data["OrderStatus"]
    except:
        raise ex.PaymentUrlNotFoundException(
            "PayPro response does not contain payment url, please try again"
        )

    return order_status == "PAID"


def invoice_range(start_date: datetime, end_date: datetime) -> List[vm.PayProOrderResponseDTO]:
    auth_token = _get_paypro_auth_token()
    config = {
        "method": "get",
        "url": f"{os.environ.get('PAYPRO_BASE_URL')}/v2/ppro/gpo",
        "data": json.dumps(
            {
                "Username": os.environ.get("USERNAME"),
                "startDate": start_date.isoformat(),
                "endDate": end_date.isoformat(),
            }
        ),
        "headers": {
            "token": auth_token,
        },
    }

    try:
        pp_res = requests.request(**config, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise ex.PayProsCreateOrderTimedOut("PayPro's request timed out, retry again please!")

    pp_res.raise_for_status()
    json_res = pp_res.json()
    result = [vm.PayProOrderResponseDTO.from_pp_api(response=order) for order in json_res]
    result = result[1:]
    return result
