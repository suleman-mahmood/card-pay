# from core.payment.entrypoint import commands as pmt_cmd
# from core.payment.entrypoint import queries as pmt_qry

# from core.marketing.entrypoint import queries as mktg_qry
from core.entrypoint.uow import FakeUnitOfWork
from core.marketing.entrypoint import commands as mktg_cmd

# from core.marketing.tests.conftest import seed_starred_wallet
# from uuid import uuid4
# from core.payment.domain import model as pmt_mdl
# from core.payment.entrypoint import anti_corruption as pmt_acl

# def _get_wallet_from_wallet_id(wallet_id: str, uow: AbstractUnitOfWork):
#     sql = """
#         select id, balance, qr_id
#         from wallets
#         where id = %s
#     """
#     uow.cursor.execute(sql, [wallet_id])
#     row = uow.cursor.fetchone()
#     return pmt_mdl.Wallet(
#         id=row[0],
#         balance=row[1],
#         qr_id=row[2],
#     )

# def test_loyalty_points_for_p2p_push(seed_verified_auth_user):
#     uow = UnitOfWork()
#     sender = seed_verified_auth_user(uow)
#     recipient = seed_verified_auth_user(uow)
#     mktg_cmd.add_weightage(
#         weightage_type="P2P_PUSH",
#         weightage_value=10,
#         uow=uow,
#     )
#     sender_wallet = _get_wallet_from_wallet_id(
#         wallet_id=sender.wallet_id, uow=uow
#     )
#     uow.transactions.add_1000_wallet(sender_wallet.id)

#     pmt_cmd.execute_transaction(
#         tx_id=str(uuid4()),
#         sender_wallet_id=sender.wallet_id,
#         recipient_wallet_id=recipient.wallet_id,
#         amount=100,
#         transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
#         transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
#         uow=uow,
#         mktg_svc=pmt_acl.FakeMarketingService(),
#     )

#     fetched_sender = mktg_qry.get_marketing_user(user_id=sender.id, uow=uow)
#     assert fetched_sender.loyalty_points == 1000


# def test_loyalty_points_for_p2p_pull(seed_verified_auth_user):
#     uow = UnitOfWork()

#     recipient = seed_verified_auth_user(uow)
#     sender = seed_verified_auth_user(uow)

#     mktg_cmd.add_weightage(
#         weightage_type="P2P_PULL",
#         weightage_value=10,
#         uow=uow,
#     )
#     sender_wallet = _get_wallet_from_wallet_id(
#         wallet_id=sender.wallet_id, uow=uow
#     )

#     uow.transactions.add_1000_wallet(sender_wallet.id)

#     tx_id=str(uuid4())
#     pmt_cmd.execute_transaction(
#         tx_id=tx_id,
#         sender_wallet_id=sender.wallet_id,
#         recipient_wallet_id=recipient.wallet_id,
#         amount=100,
#         transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
#         transaction_type=pmt_mdl.TransactionType.P2P_PULL,
#         uow=uow,
#         mktg_svc=pmt_acl.FakeMarketingService(),
#     )
#     pmt_cmd.accept_p2p_pull_transaction(
#         transaction_id=tx_id,
#         uow=uow,
#         mktg_svc=pmt_acl.FakeMarketingService(),
#     )

#     fetched_sender = mktg_qry.get_marketing_user(user_id=sender.id, uow=uow)
#     assert fetched_sender.loyalty_points == 1000


def test_use_reference(seed_marketing_user):
    uow = FakeUnitOfWork()

    referee = seed_marketing_user(uow)
    referral = seed_marketing_user(uow)

    mktg_cmd.add_weightage(
        weightage_type="REFERRAL",
        weightage_value=10,
        uow=uow,
    )

    mktg_cmd.use_reference(
        referee_id=referee.id,
        referral_id=referral.id,
        uow=uow,
    )

    fetched_referee = uow.marketing_users.get(id=referee.id)
    fetched_referral = uow.marketing_users.get(id=referral.id)
    assert fetched_referee.referral_id == referral.id
    assert fetched_referral.loyalty_points == 10

    # fetched_loyalty_points = mktg_qry.get_weightage(
    #     weightage_type="REFERRAL",
    #     uow=uow,
    # ).weightage_value
    # fetched_referee = mktg_qry.get_marketing_user(user_id=referee.id, uow=uow)
    # fetched_referral = mktg_qry.get_marketing_user(user_id=referral.id, uow=uow)


# def test_add_and_set_weightage():
#     uow = UnitOfWork()
#     mktg_cmd.add_weightage(
#         weightage_type="PAYMENT_GATEWAY", weightage_value=10, uow=uow
#     )

#     mktg_cmd.set_weightage(
#         weightage_type="PAYMENT_GATEWAY",
#         weightage_value=20,
#         uow=uow,
#     )

#     fetched_weightage = mktg_qry.get_weightage("PAYMENT_GATEWAY", uow)

#     assert fetched_weightage.weightage_value == 20


# def test_add_and_set_cashback_slabs():
#     uow = UnitOfWork()
#     mktg_cmd.set_cashback_slabs(
#         cashback_slabs=[[0, 100, "PERCENTAGE", 0.1], [100, 200, "PERCENTAGE", 0.2]],
#         uow=uow,
#     )  # Adding cashback slabs

#     mktg_cmd.set_cashback_slabs(
#         cashback_slabs=[[0, 100, "PERCENTAGE", 0.2], [100, 200, "PERCENTAGE", 0.3]],
#         uow=uow,
#     )

#     fetched_all_cashbacks = uow.cashback_slabs.get_all()
#     assert fetched_all_cashbacks.cashback_slabs[0].cashback_value == 0.2

#     mktg_cmd.set_cashback_slabs(
#         cashback_slabs=[[20, 100, "PERCENTAGE", 0.2], [100, 200, "PERCENTAGE", 0.3]],
#         uow=uow,
#     )

#     fetched_all_cashbacks = uow.cashback_slabs.get_all()
#     fetched_cashback_slabs = fetched_all_cashbacks.cashback_slabs
#     assert fetched_cashback_slabs[0].start_amount == 0
#     assert fetched_cashback_slabs[0].end_amount == 20


# def test_cashback(seed_verified_auth_user, seed_starred_wallet, mocker):
#     uow = UnitOfWork()
#     seed_starred_wallet(uow)

#     mktg_cmd.add_weightage(
#         weightage_type="PAYMENT_GATEWAY",
#         weightage_value=0.1,
#         uow=uow,
#     )
#     mktg_cmd.add_weightage(
#         weightage_type="CASH_BACK",
#         weightage_value=0,
#         uow=uow,
#     )
#     mktg_cmd.set_cashback_slabs(
#         cashback_slabs=[[0, 100, "PERCENTAGE", 0.1], [100, 200, "PERCENTAGE", 0.2]],
#         uow=uow,
#     )

#     recipient = seed_verified_auth_user(uow)
#     pg = seed_verified_auth_user(uow)
#     pg_wallet = _get_wallet_from_wallet_id(
#         wallet_id=pg.wallet_id, uow=uow
#     )

#     uow.transactions.add_1000_wallet(wallet_id=pg_wallet.id)
#     recipient_wallet = _get_wallet_from_wallet_id(
#         wallet_id=recipient.wallet_id, uow=uow
#     )
#     assert recipient_wallet.balance == 0

#     tx_id = str(uuid4())
#     pmt_cmd.execute_transaction(
#         tx_id=tx_id,
#         sender_wallet_id=pg.id,
#         recipient_wallet_id=recipient.wallet_id,
#         amount=100,
#         transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
#         transaction_type=pmt_mdl.TransactionType.PAYMENT_GATEWAY,
#         uow=uow,
#         mktg_svc=pmt_acl.FakeMarketingService(),
#     )
#     pmt_cmd.accept_payment_gateway_transaction(transaction_id=tx_id, uow=uow, mktg_svc= pmt_acl.FakeMarketingService())

#     marketing_recipient = mktg_qry.get_marketing_user(
#         user_id=recipient.id,
#         uow=uow,
#     )

#     assert marketing_recipient.loyalty_points == 10
#     assert pmt_qry.get_wallet_balance(pg_wallet.id, uow) == 900
#     assert pmt_qry.get_wallet_balance(recipient.wallet_id, uow) == (100 * 1.2)


# def test_add_and_set_missing_weightages_to_zero():
#     uow = UnitOfWork()
#     # p2p_push_weightage = uow.weightages.get(
#     #     weightage_type=pmt_mdl.TransactionType.P2P_PUSH
#     # )
#     # mktg_cmd.add_and_set_missing_weightages_to_zero(uow=uow)
#     # updated_p2p_push_weightage = uow.weightages.get(
#     #     weightage_type=pmt_mdl.TransactionType.P2P_PUSH
#     # )

#     # assert p2p_push_weightage.weightage_value == updated_p2p_push_weightage.weightage_value

#     sql = """ delete from weightages"""
#     uow.cursor.execute(sql)
#     mktg_cmd.add_and_set_missing_weightages_to_zero(uow=uow)

#     for transaction_type in pmt_mdl.TransactionType:
#         fetched_weightage = uow.weightages.get(weightage_type=transaction_type)

#         assert fetched_weightage.weightage_value == 0

#     uow.close_connection()
