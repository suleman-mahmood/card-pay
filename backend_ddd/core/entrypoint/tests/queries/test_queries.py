"""tests for entrypoint queries"""

from uuid import uuid4
from core.entrypoint.uow import AbstractUnitOfWork, UnitOfWork
from core.entrypoint import queries as app_queries
from core.entrypoint import view_model as app_view_model


def test_get_latest_force_update_version():
    """test get_latest_force_update_version"""
    sql = """
    insert into
        version_history (id, latest_version, force_update_version)
    values
        (%s, %s, %s)
    """
    uow = UnitOfWork()
    uow.cursor.execute(sql, (str(uuid4()), "1.0.0", "1.0.0"))
    version: app_view_model.Version = app_queries.get_latest_force_update_version(uow)
    uow.close_connection()

    assert version.latest_version == "1.0.0"
    assert version.force_update_version == "1.0.0"
