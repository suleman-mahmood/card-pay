import requests
import json
import os
from dotenv import load_dotenv
from json import dumps

# load_dotenv()
# from core.comms.entrypoint import commands


# def test_send_email():
#     commands.send_email(
#         subject="Pytest",
#         text="Woah noice content, someone ran pytest and the email got into your inbox successfully!",
#         to="23100011@lums.edu.pk",
#     )

"""
https://lifetimesms.com/otp?
api_token=xxxx&
api_secret=xxxx&
to=92xxxxxxxxxx&
from=Brand&
event_id=Approved_id&
data={"name":"Mr Anderson","ledger":"-R520,78","date":"28 February 2015"}
"""

# def test_send_otp_sms():
#     url = "https://lifetimesms.com/otp"
#     parameters = {
#         "api_token": os.environ.get("SMS_API_TOKEN"),
#         "api_secret": os.environ.get("SMS_API_SECRET"),
#         "to": "923333462677",
#         "from": "CardPay",
#         "event_id": "366",
#         "data": dumps({
#             "name": "Suleman Mahmood",
#             "code": "7236",
#         })
#     }

#     response = requests.post(url, data=parameters)
#     print(response.content)


# def test_send_sms():
#     url = "https://lifetimesms.com/otp"
#     headers = {"Content-Type": "application/json"}
#     parameters = {
#         "api_token": os.environ.get("SMS_API_TOKEN"),
#         "api_secret": os.environ.get("SMS_API_SECRET"),
#         "to": "923333462677",
#         "from": "CardPay",
#         "event_id": "xx",
#         "data": {
#             "name": "",
#             "ledger": "",
#             "date": "",
#         },
#     }

#     response = requests.post(
#         url,
#         data=parameters,
#         headers=headers,
#         timeout=30,
#         verify=False,
#     )

#     #

#     url = "https://lifetimesms.com/otp"

#     data = {"key": "value", "code": "123456", "variable": "value of variable"}

#     data = json.dumps(data)

#     parameters = {
#         "api_token": os.environ.get("SMS_API_TOKEN"),
#         "api_secret": os.environ.get("SMS_API_SECRET"),
#         "to": "923333462677",
#         "event_id": "some event id",
#         "data": data,
#     }

#     headers = {"Content-Type": "application/x-www-form-urlencoded"}

#     response = requests.post(
#         url, data=parameters, headers=headers, timeout=30, verify=False
#     )

#     print(response.text)


# def test_send_sms():
#     url = "https://lifetimesms.com/json"
#     parameters = {
#         "api_token": os.environ.get("SMS_API_TOKEN"),
#         "api_secret": os.environ.get("SMS_API_SECRET"),
#         "to": "923333462677",
#         "from": "CardPay",
#         "message": "heyo",
#     }

#     response = requests.post(url, data=parameters)
#     print(response.content)
