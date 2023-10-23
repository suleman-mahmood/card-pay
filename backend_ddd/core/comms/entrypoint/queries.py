from core.entrypoint.uow import AbstractUnitOfWork
from core.comms.entrypoint import exceptions as comms_svc_ex

def get_fcm_token(user_id: str, uow: AbstractUnitOfWork) -> str:
    sql = """
        select fcm_token
        from fcm_tokens
        where user_id = %(user_id)s
    """
    uow.dict_cursor.execute(sql, {"user_id": user_id})
    row = uow.dict_cursor.fetchone()
    if row is None:
        raise comms_svc_ex.FcmTokenNotFound("No FCM token found for this user")
    
    return row["fcm_token"]
