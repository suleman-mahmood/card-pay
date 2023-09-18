from core.entrypoint.uow import AbstractUnitOfWork
from core.payment.domain import model as pmt_mdl
from core.marketing.domain import model as mdl
from core.marketing.domain import exceptions as mktg_ex


def use_reference(
    referee_id: str,
    referral_id: str,
    uow: AbstractUnitOfWork,
):
    referee = uow.marketing_users.get(referee_id)
    referral = uow.marketing_users.get(referral_id)
    weightage = uow.weightages.get(pmt_mdl.TransactionType.REFERRAL)

    referee.use_reference(referral.id)
    referral.add_referral_loyalty_points(
        weightage=weightage, referee_verified=referee.marketing_user_verified
    )

    uow.marketing_users.save(referee)
    uow.marketing_users.save(referral)


def add_loyalty_points(
    sender_wallet_id: str,
    recipient_wallet_id: str,
    transaction_amount: int,
    transaction_type: pmt_mdl.TransactionType,
    uow: AbstractUnitOfWork,
):
    # different recipient on Payment Gateway transaction
    if transaction_type == pmt_mdl.TransactionType.PAYMENT_GATEWAY:
        user_id = recipient_wallet_id
    else:
        user_id = sender_wallet_id

    user = uow.marketing_users.get(user_id)
    weightage = uow.weightages.get(transaction_type)

    user.add_loyalty_points(transaction_type, transaction_amount, weightage)

    uow.marketing_users.save(user)


def add_weightage(
    weightage_type: str,
    weightage_value: float,
    uow: AbstractUnitOfWork,
):
    weightage_type = pmt_mdl.TransactionType[weightage_type]

    weightage = mdl.Weightage(
        weightage_type=weightage_type, weightage_value=weightage_value
    )
    uow.weightages.save(weightage)


def set_weightage(
    weightage_type: str,
    weightage_value: float,
    uow: AbstractUnitOfWork,
):
    weightage_type = pmt_mdl.TransactionType[weightage_type]

    weightage = uow.weightages.get(weightage_type)

    weightage.set_weightage(weightage_value)

    uow.weightages.save(weightage)


def set_cashback_slabs(
    cashback_slabs: list,
    uow: AbstractUnitOfWork,
):
    slab_list = [
        mdl.CashbackSlab(
            start_amount=slab[0],
            end_amount=slab[1],
            cashback_type=mdl.CashbackType[slab[2]],
            cashback_value=slab[3],
        )
        for slab in cashback_slabs
    ]

    all_cashbacks = mdl.AllCashbacks(cashback_slabs=slab_list)

    all_cashbacks.handle_invalid_slabs()

    uow.cashback_slabs.save_all(all_cashbacks)


def add_and_set_missing_weightages_to_zero(
    uow: AbstractUnitOfWork,
):
    for transaction_type in pmt_mdl.TransactionType:
        try:
            uow.weightages.get(transaction_type)
        except mktg_ex.WeightageNotFoundException:
            add_weightage(
                weightage_type=transaction_type.name,
                weightage_value=0,
                uow=uow,
            )
