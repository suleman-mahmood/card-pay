"""api tests for general purpose queries and tasks"""

from json import loads
from uuid import uuid4

from core.entrypoint.uow import UnitOfWork
from core.api.api_cardpay_app import get_latest_force_update_version


def test_get_latest_force_update_version(client):
    """test get_latest_force_update_version /get-latest-force-update-version"""

    sql = """
    insert into
        version_history (id, latest_version, force_update_version)
    values
        (%s, %s, %s)
    """
    uow = UnitOfWork()
    uow.cursor.execute(sql, (str(uuid4()), "1.0.0", "1.0.0"))
    uow.commit_close_connection()

    response = client.get(
        "http://127.0.0.1:5000/api/v1/get-latest-force-update-version"
    )
    data = loads(response.data.decode())
    message = data["message"]
    status_code = data["status_code"]

    assert message == "App latest and force update version returned successfully"
    assert status_code == 200
