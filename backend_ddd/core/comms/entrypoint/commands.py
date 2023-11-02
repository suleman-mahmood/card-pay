import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from json import dumps
from typing import Dict

import firebase_admin
import requests
from core.comms.entrypoint import anti_corruption as acl
from core.entrypoint.uow import AbstractUnitOfWork
from dotenv import load_dotenv
from firebase_admin import messaging

load_dotenv()

EMAIL_FROM = "cardpayteam@gmail.com"

EVENT_ID = "366"
SMS_SENDER_FROM = "CardPay"

"""
Example:
https://lifetimesms.com/otp?api_token=xxxx&api_secret=xxxx&to=92xxxxxxxxxx&from=Brand&event_id=Approved_id&data={"name":"Mr Anderson","ledger":"-R520,78","date":"28 February 2015"}
"""


def send_otp_sms(full_name: str, to: str, otp_code: str):
    url = "https://lifetimesms.com/otp"
    parameters = {
        "api_token": os.environ.get("SMS_API_TOKEN"),
        "api_secret": os.environ.get("SMS_API_SECRET"),
        "to": to,  # 92xxxxxxxxxx (10 x); 923333462677
        "from": SMS_SENDER_FROM,
        "event_id": EVENT_ID,
        "data": dumps(
            {
                "name": full_name,
                "code": otp_code,
            }
        ),
    }

    requests.post(url, data=parameters)


def send_marketing_sms(content: str, to: str):
    url = "https://lifetimesms.com/json"
    parameters = {
        "api_token": os.environ.get("SMS_API_TOKEN"),
        "api_secret": os.environ.get("SMS_API_SECRET"),
        "to": to,  # 92xxxxxxxxxx (10 x); 923333462677
        "from": SMS_SENDER_FROM,
        "message": content,
    }

    response = requests.post(url, data=parameters)
    print(response.content)


def send_email(subject: str, text: str, to: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to

    part = MIMEText(text, "plain")

    msg.attach(part)

    server = smtplib.SMTP_SSL("email-smtp.ap-south-1.amazonaws.com", 465)
    server.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASSWORD"))
    server.sendmail(EMAIL_FROM, to, msg.as_string())
    server.quit()


def send_image_email(subject: str, html: str, to: str, image_bytes: bytes):
    msg = MIMEMultipart("related")

    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to

    msgAlternative = MIMEMultipart("alternative")
    msg.attach(msgAlternative)

    msgAlternative.attach(MIMEText(html, "html"))

    image = MIMEImage(image_bytes)
    image.add_header("Content-ID", "<qr_code_image>")
    msg.attach(image)

    server = smtplib.SMTP_SSL("email-smtp.ap-south-1.amazonaws.com", 465)

    if os.environ.get("EMAIL_USER") is None or os.environ.get("EMAIL_PASSWORD") is None:
        return

    server.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASSWORD"))
    server.sendmail(EMAIL_FROM, to, msg.as_string())
    server.quit()


def send_promotional_sms(content: str):
    pass


def send_promotional_email(content: str):
    pass


def set_fcm_token(
    user_id: str,
    fcm_token: str,
    uow: AbstractUnitOfWork,
):
    """Set fcm token"""
    sql = """
        insert into fcm_tokens (user_id, fcm_token)
            values (%(user_id)s, %(fcm_token)s)
        on conflict (user_id) do update
            set fcm_token = %(fcm_token)s
    """
    uow.dict_cursor.execute(sql, {"user_id": user_id, "fcm_token": fcm_token})


def _send_notification_firebase(
    fcm_token: str,
    title: str,
    body: str,
):
    msg = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=fcm_token,
    )

    messaging.send(msg)


def send_notification(
    user_id: str,
    title: str,
    body: str,
    uow: AbstractUnitOfWork,
    comms_svc: acl.AbstractCommunicationService,
):
    """Send notification"""
    fcm_token = comms_svc.get_fcm_token(user_id=user_id, uow=uow)

    _send_notification_firebase(
        title=title,
        body=body,
        fcm_token=fcm_token,
    )
