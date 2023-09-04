"""
for general purpose app level queries
"""

from core.entrypoint.uow import AbstractUnitOfWork, UnitOfWork
from core.entrypoint import view_model as app_view_model


def get_latest_force_update_version(uow: AbstractUnitOfWork):
    """get app versions (latest and force update version)"""

    sql = """
        select id, latest_version, force_update_version, created_at
        from version_history
        order by created_at desc
        limit 1
    """

    result = uow.cursor.execute(sql)
    row = uow.cursor.fetchone()

    version = app_view_model.Version(
        id=row[0],
        latest_version=row[1],
        force_update_version=row[2],
        created_at=row[3],
    )

    return version
