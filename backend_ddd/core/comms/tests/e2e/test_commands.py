import json
import os
from io import BytesIO
from json import dumps
from uuid import uuid4

import pytest
import qrcode
import requests
from core.authentication.entrypoint import view_models as auth_vm
from core.comms.entrypoint import anti_corruption as acl
from core.comms.entrypoint import commands as comms_cmd
from core.comms.entrypoint import exceptions as comms_svc_ex
from core.entrypoint.uow import FakeUnitOfWork, UnitOfWork
from dotenv import load_dotenv
from firebase_admin import messaging


def test_send_notification(mocker):
    uow = FakeUnitOfWork()
    auth_svc = acl.FakeCommunicationService()
    mocker.patch("core.comms.entrypoint.commands._send_notification_firebase", return_value=None)
    comms_cmd.send_notification(
        user_id="1",
        title="Test",
        body="Test body",
        uow=uow,
        comms_svc=auth_svc,
    )


def test_set_fcm_token(seed_verified_auth_user):
    uow = UnitOfWork()
    sender, _ = seed_verified_auth_user(uow)
    fcm_token = "some_fcm_token"
    comms_cmd.set_fcm_token(user_id=sender.id, fcm_token=fcm_token, uow=uow)

    sql = """
        select
            fcm_token
        from
            fcm_tokens
        where 
            user_id = %(user_id)s
    """
    uow.dict_cursor.execute(sql, {"user_id": sender.id})
    fetched_fcm_token = uow.dict_cursor.fetchone()["fcm_token"]

    assert fetched_fcm_token == fcm_token

    uow.close_connection()


def test_send_notification_missing_fcm_token(mocker):
    user_id = str(uuid4())
    uow = UnitOfWork()
    mocker.patch("core.comms.entrypoint.commands._send_notification_firebase", return_value=None)

    with pytest.raises(comms_svc_ex.FcmTokenNotFound):
        comms_cmd.send_notification(
            user_id=user_id,
            title="Test",
            body="Test body",
            uow=uow,
            comms_svc=acl.CommunicationService(),
        )

    uow.close_connection()


# def test_send_notification_real():
#     msg = messaging.Message(
#         notification=messaging.Notification(title="Notif title", body="Notif body"),
#         token="dPNxmPAdRVajGDbZH7x2om:APA91bG1bGo4DFbz2vaucekhtjzEpgaFMyCwt0Q-xGIbXFapjn5Uwd9HeVHNBhytnY0a6MQl-Gje4ntOnbyrNljsfFnQYBdAx9PqgNu0hSiXl0f7E2_gzWonnMbWKTjCTz7oL6KDlcJ0",
#     )

#     messaging.send(msg)


# load_dotenv()
# from core.comms.entrypoint import commands


# def test_send_email():
#     commands.send_email(
#         subject="Pytest",
#         text="Woah noice content, someone ran pytest and the email got into your inbox successfully!",
#         to="23100011@lums.edu.pk",
#     )


# def test_send_image_email():
#     data = {"qr_id": str(uuid4()), "event_id": str(uuid4())}
#     data_str = str(data)

#     qr = qrcode.QRCode(
#         version=1,
#         box_size=10,
#         border=4,
#     )

#     qr.add_data(data_str)
#     qr.make(fit=True)

#     buffer = BytesIO()
#     img = qr.make_image(fill_color="black", back_color="white")
#     img.save(buffer)
#     qr_code_bytes = buffer.getvalue()
#     buffer.close()

#     comms_cmd.send_image_email(
#         subject="Test image email",
#         text="Woho, sending an email with some images O.o!",
#         to="23100011@lums.edu.pk",
#         image_bytes=qr_code_bytes,
#     )


# def test_send_image_email_tedx():
#     data = {"qr_id": str(uuid4()), "event_id": str(uuid4())}
#     data_str = str(data)

#     qr = qrcode.QRCode(
#         version=1,
#         box_size=10,
#         border=4,
#     )

#     qr.add_data(data_str)
#     qr.make(fit=True)

#     buffer = BytesIO()
#     img = qr.make_image(fill_color="black", back_color="white")
#     img.save(buffer)
#     qr_code_bytes = buffer.getvalue()
#     buffer.close()

#     html = f"""
#     <html>
#         <head>
#             <title>TedX Confirmation Email</title>
#         </head>
#         <body>
#             <h1>Hi Abdur Rehman Shamsi!</h1>

#             <p>We're excited to confirm your registration for TedX</p>

#             <p>Please show this QR code at the venue to mark your attendance:</p>
#             <img src="cid:qr_code_image">

#             <h2>Event Details</h2>

#             <ul>
#                 <li>Date: 18th November, 2023</li>
#                 <li>Time: 9:00 AM</li>
#                 <li>Location: LUMS SDSB B3</li>
#             </ul>

#             <p>Please review the event details carefully and make any necessary arrangements.</p>

#             <p>We look forward to seeing you at the event!</p>

#             <p>Sincerely,</p>
#             <p>CardPay Team</p>
#         </body>
#     </html>
#     """

#     comms_cmd.send_image_email(
#         subject="Successful Registration Completed",
#         html=html,
#         to="huzaifa@cardpay.com.pk",
#         image_bytes=qr_code_bytes,
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


@pytest.mark.skip
def test_send_personalized_emails():
    def task(subject, text, to):
        print(f"To: {to} \n")
        print(f"Subject: {subject} \n")
        print(f"Text: {text} \n")

    auth_acl = acl.FakeAuthenticationService()
    auth_acl.set_all_emails(
        [
            auth_vm.EmailInfoDTO(email="1e", full_name="1n"),
            auth_vm.EmailInfoDTO(email="2e", full_name="2n"),
            auth_vm.EmailInfoDTO(email="3e", full_name="3n"),
            auth_vm.EmailInfoDTO(email="4e", full_name="4n"),
            auth_vm.EmailInfoDTO(email="5e", full_name="5n"),
            auth_vm.EmailInfoDTO(email="6e", full_name="6n"),
        ]
    )

    comms_cmd.send_personalized_emails(
        email_body_template="Hi {{name}}, this is a test email.",
        email_subject="Test email",
        uow=UnitOfWork(),
        auth_acl=auth_acl,
        task=task,
    )

    assert False
