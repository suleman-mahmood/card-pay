import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM = "cardpayteam@gmail.com"


def send_sms(content: str, to: str):
    pass


def send_email(subject: str, text: str, to: str):
    # TODO remove this in production
    return

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
