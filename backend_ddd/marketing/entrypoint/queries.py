from ...entrypoint.uow import AbstractUnitOfWork
from ..domain.model import TransactionType

def get_marketing_user(
    user_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        return uow.marketing_users.get(user_id)


def get_weightage(
    weightage_type: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        weightage_type = TransactionType[weightage_type]
        return uow.weightages.get(weightage_type)
