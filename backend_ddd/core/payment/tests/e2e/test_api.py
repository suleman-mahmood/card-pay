import pytest
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import commands as auth_cmd
from core.authentication.entrypoint import queries as auth_qry
from core.payment.entrypoint import queries as pmt_qry
from core.entrypoint.uow import UnitOfWork
from json import loads
from core.api import utils

import os

# def test_execute_p2p_push_api(seed_api_customer, mocker, client):
    
#     sender_id = seed_api_customer(mocker, client)
#     recipient_id = seed_api_customer(mocker, client)

#     SECRET_KEY = os.environ["RETOOL_SECRET"]
#     client.post(
#         "http://127.0.0.1:5000/api/v1/create-closed-loop",
#         json={
#             "name": "LUMS",
#             "logo_url": "sample/url",
#             "description": "Harvard of Pakistan",
#             "verification_type": "ROLLNUMBER",
#             "regex": "[0-9]{8}",
#             "RETOOL_SECRET": SECRET_KEY
#         }
#     )

#     uow = UnitOfWork()
#     closed_loop_id = auth_qry._get_latest_closed_loop_id(
#         uow
#     )
#     uow.close_connection()

#     headers = {
#         "Authorization": "Bearer pytest_auth_token",
#         "Content-Type": "application/json",
#     }

#     mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
#     mocker.patch("core.comms.entrypoint.commands.send_email", return_value=None)
#     client.post(
#         "http://127.0.0.1:5000/api/v1/register-closed-loop",
#         json = {
#             "closed_loop_id": closed_loop_id,
#             "unique_identifier":"26100279"
#         },
#         headers = headers
#     )

#     mocker.patch("core.api.utils._get_uid_from_bearer", return_value=recipient_id)
#     client.post(
#         "http://127.0.0.1:5000/api/v1/register-closed-loop",
#         json = {
#             "closed_loop_id": closed_loop_id,
#             "unique_identifier":"26100290"
#         },
#         headers = headers
#     )

#     uow = UnitOfWork()
#     sender = uow.users.get(user_id=sender_id)
#     recipient = uow.users.get(user_id=recipient_id)
#     uow.close_connection()


#     otp = sender.closed_loops[closed_loop_id].unique_identifier_otp
#     mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
#     client.post(
#         "http://127.0.0.1:5000/api/v1/verify-closed-loop",
#         json = {
#             "closed_loop_id": closed_loop_id,
#             "unique_identifier_otp":otp,
#         },
#         headers = headers
#     )

#     otp = recipient.closed_loops[closed_loop_id].unique_identifier_otp
#     mocker.patch("core.api.utils._get_uid_from_bearer", return_value=recipient_id)
#     client.post(
#         "http://127.0.0.1:5000/api/v1/verify-closed-loop",
#         json = {
#             "closed_loop_id": closed_loop_id,
#             "unique_identifier_otp":otp,
#         },
#         headers = headers
#     )
    
#     uow = UnitOfWork()
#     recipient_unique_identifier = auth_qry.get_unique_identifier_from_user_id(
#         user_id=recipient_id, uow=uow
#     )
#     uow.transactions.add_1000_wallet(wallet_id=sender_id)
#     uow.commit_close_connection()
    
#     mocker.patch("core.api.utils._get_uid_from_bearer", return_value=sender_id)
#     headers = {
#         "Authorization": "Bearer pytest_auth_token",
#         "Content-Type": "application/json",
#     }

#     respnonse = client.post(
#         "http://127.0.0.1:5000/api/v1/execute-p2p-push-transaction",
#         json={
#             "recipient_unique_identifier": recipient_unique_identifier,
#             "amount": 100,
#             "closed_loop_id": closed_loop_id
#         },
#         headers=headers
#     )

#     assert loads(respnonse.data.decode()) == utils.Response(
#             message="p2p push transaction executed successfully",
#             status_code=201,
#         ).__dict__