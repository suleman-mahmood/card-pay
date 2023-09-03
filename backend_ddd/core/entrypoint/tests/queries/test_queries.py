"""tests for entrypoint queries"""

from core.entrypoint.uow import AbstractUnitOfWork, UnitOfWork
from core.entrypoint import queries as app_queries


def test_get_latest_force_update_version():
    """test get_latest_force_update_version"""

    uow = UnitOfWork()
    result = app_queries.get_latest_force_update_version(uow)
    result_keys = result.keys()

    assert "force_update_version" in result_keys
    assert "latest_version" in result_keys
    assert "created_at" in result_keys
