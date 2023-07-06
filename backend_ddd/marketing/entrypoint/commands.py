
from ...payment.entrypoint.queries import get_user_id_from_wallet_id
from ...entrypoint.uow import AbstractUnitOfWork
from ...payment.entrypoint import commands as payment_commands
from ..domain.model import Weightage, CashbackSlab, CashbackType, AllCashbacks
from ...payment.domain.model import TransactionType
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
            weightage=weightage,
            referee_verified=referee.marketing_user_verified
        )

        uow.marketing_users.save(referee)
        uow.marketing_users.save(referral)


def add_loyalty_points_to_user(
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
    sender_user_id = get_user_id_from_wallet_id(
        wallet_id=sender_wallet_id, uow=uow)
    recipient_user_id = get_user_id_from_wallet_id(
        wallet_id=recipient_wallet_id, uow=uow)

    # selecting loyalty points recipient based on transaction type
    if transaction_type == TransactionType.PAYMENT_GATEWAY:
        add_loyalty_points_to_user(
            user_id=recipient_user_id,
            transaction_amount=transaction_amount,
            transaction_type=transaction_type,
            uow=uow,
        )
    elif transaction_type == TransactionType.P2P_PUSH or transaction_type == TransactionType.P2P_PULL:
        add_loyalty_points_to_user(
            user_id=sender_user_id,
            transaction_amount=transaction_amount,
            transaction_type=transaction_type,
            uow=uow,
        )


def give_cashback(
    sender_wallet_id: str,
    recipient_wallet_id: str,
    deposited_amount: int,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
):
    if transaction_type != TransactionType.PAYMENT_GATEWAY:
        return

    recipient_user_id = get_user_id_from_wallet_id(
        wallet_id=recipient_wallet_id, uow=uow)
    recipient = uow.marketing_users.get(recipient_user_id)
    amount = recipient.calculate_cashback(
        deposit_amount=deposited_amount,
        transaction_type=transaction_type,
        all_cashbacks=uow.cashback_slabs.get_all(),
    )
    payment_commands.execute_cashback_transaction(
        sender_wallet_id=sender_wallet_id,  # This will be a fixed cardpay wallet id
        recipient_wallet_id=recipient_wallet_id,
        amount=amount,
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
            weightage_type=weightage_type,
            weightage_value=weightage_value
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
        slab_list = []
        for slab in cashback_slabs:
            slab_list.append(
                CashbackSlab(
                    start_amount=slab[0],
                    end_amount=slab[1],
                    cashback_type=CashbackType[slab[2]],
                    cashback_value=slab[3],
                )
            )

        uow.cashback_slabs.save_all(AllCashbacks(
            cashback_slabs=slab_list
        )
        )
