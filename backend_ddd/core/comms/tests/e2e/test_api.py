import pytest
from core.entrypoint.uow import UnitOfWork
from core.api import utils
from json import loads
from core.comms.entrypoint import queries as comms_qry
from core.comms.entrypoint import commands as comms_cmd
from uuid import uuid4
from core.comms.entrypoint import anti_corruption as acl

def test_set_fcm_token(client, mocker, seed_verified_auth_user):
    uow = UnitOfWork()
    user,_ = seed_verified_auth_user(uow=uow)
    uow.commit_close_connection()

    fcm_token = "firebase_fcm_token"
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user.id)
    response = client.post(
        "http://127.0.0.1:5000/api/v1/set-fcm-token",
        json={
            "fcm_token": fcm_token,
        },
        headers=headers,
    )
    assert (
        loads(response.data.decode())
        == utils.Response(
            message="fcm token set successfully",
            status_code=201,
        ).__dict__
    )

    uow = UnitOfWork()
    assert comms_qry.get_fcm_token(user_id=user.id, uow=uow) == fcm_token
    uow.close_connection()

    new_fcm_token = "new_firebase_fcm_token"
    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user.id)
    response = client.post(
        "http://127.0.0.1:5000/api/v1/set-fcm-token",
        json={
            "fcm_token": new_fcm_token,
        },
        headers=headers,
    )

    assert (
        loads(response.data.decode())
        == utils.Response(
            message="fcm token set successfully",
            status_code=201,
        ).__dict__
    )

    uow = UnitOfWork()
    assert comms_qry.get_fcm_token(user_id=user.id, uow=uow) == new_fcm_token
    uow.close_connection()



def test_send_notification(client, mocker, seed_verified_auth_user):

    uow = UnitOfWork()
    user,_ = seed_verified_auth_user(uow=uow)
    uow.commit_close_connection()

    fcm_token = "firebase_fcm_token"
    headers = {
        "Authorization": "Bearer pytest_auth_token",
        "Content-Type": "application/json",
    }

    mocker.patch("core.api.utils._get_uid_from_bearer", return_value=user.id)
    response = client.post(
        "http://127.0.0.1:5000/api/v1/set-fcm-token",
        json={
            "fcm_token": fcm_token,
        },
        headers=headers,
    )

    uow = UnitOfWork()
    mocker.patch(
        "core.comms.entrypoint.commands._send_notification_firebase", return_value=None
    )
    comms_cmd.send_notification(
        user_id=user.id,
        title="Test",
        body="Test body",
        uow=uow,
        comms_svc=acl.CommunicationService(),
    )
    uow.close_connection()


