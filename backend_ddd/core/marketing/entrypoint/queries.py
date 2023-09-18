from core.entrypoint.uow import AbstractUnitOfWork
from core.marketing.domain import model as mdl


def get_marketing_user(
    user_id: str,
    uow: AbstractUnitOfWork,
):
    return uow.marketing_users.get(user_id)


def get_weightage(
    weightage_type: str,
    uow: AbstractUnitOfWork,
):
    weightage_type = mdl.TransactionType[weightage_type]
    return uow.weightages.get(weightage_type)


def get_all_cashbacks(uow: AbstractUnitOfWork) -> mdl.AllCashbacks:
    return uow.cashback_slabs.get_all()
