from ...entrypoint import commands as marketing_commands
from ....entrypoint.uow import FakeUnitOfWork, UnitOfWork, AbstractUnitOfWork
from ....payment.domain.model import TransactionType, TransactionMode, Wallet
from ....payment.entrypoint import commands as payment_commands
from ....payment.entrypoint import queries as payment_queries
from ....authentication.tests.conftest import seed_auth_user, seed_verified_auth_user
from ....authentication.entrypoint import commands as auth_commands
from ...domain.model import User, Weightage, CashbackSlab, CashbackType, AllCashbacks

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

def get_wallet_balance(
    wallet_id: str,
    uow: AbstractUnitOfWork,
):
    with uow:
        sql = """
            select balance
            from wallets
            where id = %s
            """
        uow.cursor.execute(
            sql,
            [
                wallet_id
            ]
        )
        row = uow.cursor.fetchone()
        return row[0]

def test_loyalty_points_for_p2p_push(seed_verified_auth_user):
    uow = UnitOfWork()
    sender = seed_verified_auth_user(uow)
    recipient = seed_verified_auth_user(uow)
    marketing_commands.add_weightage(
        weightage_type="P2P_PUSH",
        weightage_value=10,
        uow=uow,
    )
    with uow:
        sender_wallet = payment_queries.get_wallet_from_wallet_id(
            wallet_id=sender.wallet_id, uow=uow
        )
        uow.transactions.add_1000_wallet(sender_wallet)
    
    payment_commands.execute_transaction(
        sender_wallet_id=sender.wallet_id,
        recipient_wallet_id=recipient.wallet_id,
        amount=100,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PUSH,
        uow=uow,
    )

    fetched_sender = get_marketing_user(user_id=sender.id, uow=uow)
    assert fetched_sender.loyalty_points == 1000

def test_loyalty_points_for_p2p_pull(seed_verified_auth_user):
    uow = UnitOfWork()
    requester = seed_verified_auth_user(uow)
    requestee = seed_verified_auth_user(uow)
    marketing_commands.add_weightage(
        weightage_type="P2P_PULL",
        weightage_value=10,
        uow=uow,
    )
    with uow:
        requestee_wallet = payment_queries.get_wallet_from_wallet_id(
            wallet_id=requestee.wallet_id, uow=uow
        )
        uow.transactions.add_1000_wallet(requestee_wallet)
    tx = payment_commands.execute_transaction(
        sender_wallet_id=requestee.wallet_id,
        recipient_wallet_id=requester.wallet_id,
        amount=100,
        transaction_mode=TransactionMode.APP_TRANSFER,
        transaction_type=TransactionType.P2P_PULL,
        uow=uow,
    )
    payment_commands.accept_p2p_pull_transaction(
        transaction_id=tx.id,
        uow=uow,
    )

    fetched_requestee = get_marketing_user(user_id=requestee.id, uow=uow)
    assert fetched_requestee.loyalty_points == 1000

def test_use_reference_and_add_referral_loyalty_points(seed_verified_auth_user):

    uow = UnitOfWork()
    referee = seed_verified_auth_user(uow)
    referral = seed_verified_auth_user(uow)
    marketing_commands.add_weightage(
        weightage_type="REFERRAL",
        weightage_value=10,
        uow=uow,
    )
    marketing_commands.use_reference(
        referee_id=referee.id,
        referral_id=referral.id,
        uow=uow,
    )

    fetched_loyalty_points = get_weightage(
        weightage_type="REFERRAL", uow=uow,).weightage_value
    fetched_referee = get_marketing_user(user_id=referee.id, uow=uow)
    fetched_referral = get_marketing_user(user_id=referral.id, uow=uow)

    assert fetched_referee.referral_id == referral.id
    assert fetched_referral.loyalty_points == fetched_loyalty_points


def test_add_and_set_weightage():
    uow = UnitOfWork()
    marketing_commands.add_weightage(
        weightage_type="PAYMENT_GATEWAY",
        weightage_value=10,
        uow=uow
    )
   
    marketing_commands.set_weightage(
        weightage_type="PAYMENT_GATEWAY",
        weightage_value=20,
        uow=uow,
    )

    fetched_weightage = get_weightage("PAYMENT_GATEWAY",uow)

    assert fetched_weightage.weightage_value == 20


def test_add_and_set_cashback_slabs():

    uow = UnitOfWork()
    marketing_commands.set_cashback_slabs(
        cashback_slabs=[[0, 100, "PERCENTAGE", 0.1],
                        [100, 200, "PERCENTAGE", 0.2]],
        uow=uow,
    )  # Adding cashback slabs

    marketing_commands.set_cashback_slabs(
        cashback_slabs=[[0, 100, "PERCENTAGE", 0.2],
                        [100, 200, "PERCENTAGE", 0.3]],
        uow=uow,
    )

    with uow:
        fetched_all_cashbacks = uow.cashback_slabs.get_all()
        assert fetched_all_cashbacks.cashback_slabs[0].cashback_value == 0.2


    marketing_commands.set_cashback_slabs(
        cashback_slabs=[[20, 100, "PERCENTAGE", 0.2], [100, 200, "PERCENTAGE", 0.3]],
        uow=uow,
    )



    with uow:
        fetched_all_cashbacks = uow.cashback_slabs.get_all()
        fetched_cashback_slabs = fetched_all_cashbacks.cashback_slabs
        assert fetched_cashback_slabs[0].start_amount == 0
        assert fetched_cashback_slabs[0].end_amount == 20

def test_cashback(seed_verified_auth_user):
    uow = UnitOfWork()
    marketing_commands.add_weightage(
        weightage_type="PAYMENT_GATEWAY",
        weightage_value=0.1,
        uow=uow,
    )
    

    marketing_commands.set_cashback_slabs(
        cashback_slabs=[[0, 100, "PERCENTAGE", 0.1],
                        [100, 200, "PERCENTAGE", 0.2]],
        uow=uow,
    )
    recipient = seed_verified_auth_user(uow)
    pg = seed_verified_auth_user(uow)

    with uow:
        pg_wallet = payment_queries.get_wallet_from_wallet_id(wallet_id = pg.wallet_id, uow = uow)
        uow.transactions.add_1000_wallet(wallet = pg_wallet)
    
    payment_commands.execute_transaction(
        sender_wallet_id = pg.wallet_id,
        recipient_wallet_id = recipient.wallet_id,
        amount = 100,
        transaction_mode = TransactionMode.APP_TRANSFER,
        transaction_type = TransactionType.PAYMENT_GATEWAY,
        uow = uow,
    )

    marketing_recipient = get_marketing_user(
        user_id = recipient.id,
        uow = uow,
    )

    assert marketing_recipient.loyalty_points == 10
    assert get_wallet_balance(pg_wallet.id, uow) == 900
    assert get_wallet_balance(recipient.wallet_id, uow) == (100*1.2)
