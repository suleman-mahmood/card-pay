from core.entrypoint.uow import AbstractUnitOfWork
from core.authentication.domain import model as mdl

def decrypt_data(
    digest: bytes, uow: AbstractUnitOfWork, user_id: str
) -> str:
    user = uow.users.get(user_id=user_id)
    pk = bytes(user.private_key, encoding="utf-8")
    dd = mdl.DataDecrypter(private_key=pk)
    return dd.decrypt_data(digest=digest)