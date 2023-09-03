"""
for general purpose app level queries
"""

from core.entrypoint.uow import AbstractUnitOfWork, UnitOfWork


def get_latest_force_update_version(uow: AbstractUnitOfWork):
    """get app versions (latest and force update version)"""

    sql = """
        select force_update_version, latest_version, created_at
        from version_history
        order by created_at desc
        limit 1
    """

    result = uow.cursor.execute(sql)
    row = uow.cursor.fetchall()

    version = {
        "force_update_version": row[0][0],
        "latest_version": row[0][1],
        "created_at": row[0][2],
    }

    return version
