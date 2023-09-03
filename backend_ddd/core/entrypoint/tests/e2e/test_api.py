"""api tests for general purpose queries and tasks"""

from core.api.api_cardpay_app import get_latest_force_update_version
from json import loads


def test_get_latest_force_update_version(client):
    """test get_latest_force_update_version /get-latest-force-update-version"""

    response = client.get(
        "http://127.0.0.1:5000/api/v1/get-latest-force-update-version"
    )
    data = loads(response.data.decode())
    message = data["message"]
    status_code = data["status_code"]

    assert message == "App latest and force update version returned successfully"
    assert status_code == 200
