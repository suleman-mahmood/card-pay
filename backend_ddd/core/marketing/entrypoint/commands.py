from ...payment.entrypoint import queries as payment_queries
from ...entrypoint.uow import AbstractUnitOfWork
from ...payment.entrypoint import commands as payment_commands
from ..domain.model import Weightage, CashbackSlab, CashbackType, AllCashbacks
from ...payment.domain.model import TransactionType, TransactionMode
from core.marketing.domain import exceptions as mktg_ex
from uuid import uuid4

# Every transaction will check if its a cashback transaction then it'll call the marketing command which will again call the transaction command.


def use_reference(
    referee_id: str,
    referral_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        referee = uow.marketing_users.get(referee_id)
        referral = uow.marketing_users.get(referral_id)
        weightage = uow.weightages.get(TransactionType.REFERRAL)

        referee.use_reference(referral.id)
        referral.add_referral_loyalty_points(
            weightage=weightage, referee_verified=referee.marketing_user_verified
        )

        uow.marketing_users.save(referee)
        uow.marketing_users.save(referral)


def _add_loyalty_points_to_user(
    user_id: str,
    transaction_amount: int,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
):
    """Only called by add_loyalty_points()"""

    user = uow.marketing_users.get(user_id)
    weightage = uow.weightages.get(transaction_type)

    user.add_loyalty_points(transaction_type, transaction_amount, weightage)

    uow.marketing_users.save(user)


def add_loyalty_points(
    sender_wallet_id: str,
    recipient_wallet_id: str,
    transaction_amount: int,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
):
    # different recipient on Payment Gateway transaction
    if transaction_type == TransactionType.PAYMENT_GATEWAY:
        user_id = recipient_wallet_id
    else:
        user_id = sender_wallet_id

    _add_loyalty_points_to_user(
        user_id=user_id,
        transaction_amount=transaction_amount,
        transaction_type=transaction_type,
        uow=uow,
    )


def give_cashback(
    recipient_wallet_id: str,
    deposited_amount: int,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
):
    if transaction_type != TransactionType.PAYMENT_GATEWAY:
        return

    sender_wallet_id = payment_queries.get_starred_wallet_id(uow=uow)
    recipient_user_id = recipient_wallet_id
    recipient = uow.marketing_users.get(recipient_user_id)
    amount = recipient.calculate_cashback(
        deposit_amount=deposited_amount,
        transaction_type=transaction_type,
        all_cashbacks=uow.cashback_slabs.get_all(),
    )
    payment_commands.execute_transaction(
        tx_id=str(uuid4()),
        sender_wallet_id=sender_wallet_id,  # This will be a fixed cardpay wallet id
        recipient_wallet_id=recipient_wallet_id,
        amount=amount,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.CASH_BACK,
        uow=uow,
    )


def add_weightage(
    weightage_type: str,
    weightage_value: float,
    uow: AbstractUnitOfWork,
):
    weightage_type = TransactionType[weightage_type]

    with uow:
        weightage = Weightage(
            weightage_type=weightage_type, weightage_value=weightage_value
        )
        uow.weightages.save(weightage)


def set_weightage(
    weightage_type: str,
    weightage_value: float,
    uow: AbstractUnitOfWork,
):
    weightage_type = TransactionType[weightage_type]

    with uow:
        weightage = uow.weightages.get(weightage_type)

        weightage.set_weightage(weightage_value)

        uow.weightages.save(weightage)


def set_cashback_slabs(
    cashback_slabs: list,
    uow: AbstractUnitOfWork,
):
    with uow:
        slab_list = [
            CashbackSlab(
                start_amount=slab[0],
                end_amount=slab[1],
                cashback_type=CashbackType[slab[2]],
                cashback_value=slab[3],
            )
            for slab in cashback_slabs
        ]

        all_cashbacks = AllCashbacks(cashback_slabs=slab_list)
        
        all_cashbacks.handle_invalid_slabs()
        
        uow.cashback_slabs.save_all(all_cashbacks)


def add_and_set_missing_weightages_to_zero(
    uow: AbstractUnitOfWork,
):
   with uow:
       
         for transaction_type in TransactionType:
              try:
                uow.weightages.get(transaction_type)
              except mktg_ex.WeightageNotFoundException:
                add_weightage(
                    weightage_type=transaction_type.name,
                    weightage_value=0,
                    uow=uow,
                )