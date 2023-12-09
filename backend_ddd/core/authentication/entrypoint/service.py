from backend_ddd.core.entrypoint.uow import AbstractUnitOfWork
from core.authentication.domain import model as mdl

def verify_encryption_data(
    digest: str, uow: AbstractUnitOfWork, user_id: str
) -> str:
    user = uow.users.get(user_id=user_id)
    pk = bytes(user.private_key, encoding="utf-8")
    dg = bytes(digest, encoding="utf-8")
    dd = mdl.DecryptData(private_key=pk)
    decrypted_data = dd.data_decriptor(digest=dg)
    return decrypted_data