from core.entrypoint.uow import AbstractUnitOfWork
from core.marketing.domain import model as mdl
from core.payment.domain import model as pmt_mdl


def get_marketing_user(
    user_id: str,
    uow: AbstractUnitOfWork,
):
    return uow.marketing_users.get(user_id)


def get_weightage(
    weightage_type: str,
    uow: AbstractUnitOfWork,
):
    weightage_type = pmt_mdl.TransactionType[weightage_type]
    return uow.weightages.get(weightage_type)


def get_all_cashbacks(uow: AbstractUnitOfWork) -> mdl.AllCashbacks:
    all_cashbacks = uow.cashback_slabs.get_all()
    all_cashbacks.handle_invalid_slabs()

    return all_cashbacks
