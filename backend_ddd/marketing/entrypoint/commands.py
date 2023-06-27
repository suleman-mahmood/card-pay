
from ..entrypoint.queries import get_user_id_from_wallet_id
from ...entrypoint.uow import UnitOfWork, AbstractUnitOfWork
from ...payment.entrypoint import commands as payment_commands
from ..domain.model import Weightage, CashbackSlab, CashbackType
from ...payment.domain.model import TransactionType, TransactionMode

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


def add_loyalty_points(
    user_id: str,
    transaction_amount: int,
    transaction_type: TransactionType,
    uow: AbstractUnitOfWork,
):
    user = uow.marketing_users.get(user_id)
    weightage = uow.weightages.get(transaction_type)

    user.add_loyalty_points(transaction_type, transaction_amount, weightage)

    uow.marketing_users.save(user)


def give_cashback(
    sender_wallet_id: str,
    recipient_wallet_id: str,
    deposited_amount: int,
    uow: AbstractUnitOfWork,
):

    user_id = get_user_id_from_wallet_id(
        wallet_id=recipient_wallet_id, uow=uow)
    user = uow.marketing_users.get(user_id)
    amount = user.calculate_cashback(
        deposit_amount=deposited_amount,
        cashback_slabs=uow.cashback_slabs.get_all(),
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

        # [[0,500,PERCENTGAE,7.6],[500,600,"PERCENTGAE",7.6],[600,670,"PERCENTGAE",7.6]]

        if len(cashback_slabs) == 0:
            raise ValueError("Cashback slabs cannot be empty")

        first_slab_start_amount = cashback_slabs[0][0]
        if first_slab_start_amount != 0:
            cashback_slabs.insert(
                0, [0, first_slab_start_amount, "PERCENTAGE", 0])

        # catering for the last index
        if cashback_slabs[-1][1] <= cashback_slabs[-1][0]:
            raise ValueError(
                "ending amount should be greater than starting amount")

        # catering for the last index
        if cashback_slabs[-1][3] < 0:
            raise ValueError("Cashback value cannot be negative")

        for i in range(len(cashback_slabs) - 1):
            if cashback_slabs[i][1] <= cashback_slabs[i][0]:
                raise ValueError(
                    "ending amount should be greater than starting amount")

            if cashback_slabs[i][1] != cashback_slabs[i+1][0]:
                raise ValueError("Slabs should be continuous")

            if cashback_slabs[i][3] < 0:
                raise ValueError("Cashback value cannot be negative")

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

        uow.cashback_slabs.save_all(slab_list)
