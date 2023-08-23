import smtplib
import os
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from json import dumps

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
    # TODO remove this in production
    return

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


def send_promotional_sms(content: str):
    pass


def send_promotional_email(content: str):
    pass
