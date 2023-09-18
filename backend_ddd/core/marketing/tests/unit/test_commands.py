# from ...entrypoint import commands as marketing_commands
# from ...entrypoint import queries as marketing_queries
# from ....entrypoint.uow import UnitOfWork, AbstractUnitOfWork
# from ....payment.domain.model import TransactionType, TransactionMode
# from ....payment.entrypoint import commands as payment_commands
# from ....payment.entrypoint import queries as payment_queries
# from ....authentication.tests.conftest import seed_auth_user, seed_verified_auth_user
# from ....marketing.tests.conftest import seed_starred_wallet
# from uuid import uuid4
# from ....payment.domain import model as payment_mdl
# from core.payment.entrypoint import anti_corruption as pmt_acl

# def _get_wallet_from_wallet_id(wallet_id: str, uow: AbstractUnitOfWork):
#     sql = """
#         select id, balance, qr_id
#         from wallets
#         where id = %s
#     """
#     uow.cursor.execute(sql, [wallet_id])
#     row = uow.cursor.fetchone()
#     return payment_mdl.Wallet(
#         id=row[0],
#         balance=row[1],
#         qr_id=row[2],
#     )

# def test_loyalty_points_for_p2p_push(seed_verified_auth_user):
#     uow = UnitOfWork()
#     sender = seed_verified_auth_user(uow)
#     recipient = seed_verified_auth_user(uow)
#     marketing_commands.add_weightage(
#         weightage_type="P2P_PUSH",
#         weightage_value=10,
#         uow=uow,
#     )
#     sender_wallet = _get_wallet_from_wallet_id(
#         wallet_id=sender.wallet_id, uow=uow
#     )
#     uow.transactions.add_1000_wallet(sender_wallet.id)

#     payment_commands.execute_transaction(
#         tx_id=str(uuid4()),
#         sender_wallet_id=sender.wallet_id,
#         recipient_wallet_id=recipient.wallet_id,
#         amount=100,
#         transaction_mode=TransactionMode.APP_TRANSFER,
#         transaction_type=TransactionType.P2P_PUSH,
#         uow=uow,
#         mktg_svc=pmt_acl.FakeMarketingService(),
#     )

#     fetched_sender = marketing_queries.get_marketing_user(user_id=sender.id, uow=uow)
#     assert fetched_sender.loyalty_points == 1000


# def test_loyalty_points_for_p2p_pull(seed_verified_auth_user):
#     uow = UnitOfWork()

#     recipient = seed_verified_auth_user(uow)
#     sender = seed_verified_auth_user(uow)

#     marketing_commands.add_weightage(
#         weightage_type="P2P_PULL",
#         weightage_value=10,
#         uow=uow,
#     )
#     sender_wallet = _get_wallet_from_wallet_id(
#         wallet_id=sender.wallet_id, uow=uow
#     )

#     uow.transactions.add_1000_wallet(sender_wallet.id)

#     tx_id=str(uuid4())
#     payment_commands.execute_transaction(
#         tx_id=tx_id,
#         sender_wallet_id=sender.wallet_id,
#         recipient_wallet_id=recipient.wallet_id,
#         amount=100,
#         transaction_mode=TransactionMode.APP_TRANSFER,
#         transaction_type=TransactionType.P2P_PULL,
#         uow=uow,
#         mktg_svc=pmt_acl.FakeMarketingService(),
#     )
#     payment_commands.accept_p2p_pull_transaction(
#         transaction_id=tx_id,
#         uow=uow,
#         mktg_svc=pmt_acl.FakeMarketingService(),
#     )

#     fetched_sender = marketing_queries.get_marketing_user(user_id=sender.id, uow=uow)
#     assert fetched_sender.loyalty_points == 1000


# def test_use_reference_and_add_referral_loyalty_points(seed_verified_auth_user):
#     uow = UnitOfWork()
#     referee = seed_verified_auth_user(uow)
#     referral = seed_verified_auth_user(uow)
#     marketing_commands.add_weightage(
#         weightage_type="REFERRAL",
#         weightage_value=10,
#         uow=uow,
#     )
#     marketing_commands.use_reference(
#         referee_id=referee.id,
#         referral_id=referral.id,
#         uow=uow,
#     )

#     fetched_loyalty_points = marketing_queries.get_weightage(
#         weightage_type="REFERRAL",
#         uow=uow,
#     ).weightage_value
#     fetched_referee = marketing_queries.get_marketing_user(user_id=referee.id, uow=uow)
#     fetched_referral = marketing_queries.get_marketing_user(
#         user_id=referral.id, uow=uow
#     )

#     assert fetched_referee.referral_id == referral.id
#     assert fetched_referral.loyalty_points == fetched_loyalty_points


# def test_add_and_set_weightage():
#     uow = UnitOfWork()
#     marketing_commands.add_weightage(
#         weightage_type="PAYMENT_GATEWAY", weightage_value=10, uow=uow
#     )

#     marketing_commands.set_weightage(
#         weightage_type="PAYMENT_GATEWAY",
#         weightage_value=20,
#         uow=uow,
#     )

#     fetched_weightage = marketing_queries.get_weightage("PAYMENT_GATEWAY", uow)

#     assert fetched_weightage.weightage_value == 20


# def test_add_and_set_cashback_slabs():
#     uow = UnitOfWork()
#     marketing_commands.set_cashback_slabs(
#         cashback_slabs=[[0, 100, "PERCENTAGE", 0.1], [100, 200, "PERCENTAGE", 0.2]],
#         uow=uow,
#     )  # Adding cashback slabs

#     marketing_commands.set_cashback_slabs(
#         cashback_slabs=[[0, 100, "PERCENTAGE", 0.2], [100, 200, "PERCENTAGE", 0.3]],
#         uow=uow,
#     )

#     fetched_all_cashbacks = uow.cashback_slabs.get_all()
#     assert fetched_all_cashbacks.cashback_slabs[0].cashback_value == 0.2

#     marketing_commands.set_cashback_slabs(
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

#     marketing_commands.add_weightage(
#         weightage_type="PAYMENT_GATEWAY",
#         weightage_value=0.1,
#         uow=uow,
#     )
#     marketing_commands.add_weightage(
#         weightage_type="CASH_BACK",
#         weightage_value=0,
#         uow=uow,
#     )
#     marketing_commands.set_cashback_slabs(
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
#     payment_commands.execute_transaction(
#         tx_id=tx_id,
#         sender_wallet_id=pg.id,
#         recipient_wallet_id=recipient.wallet_id,
#         amount=100,
#         transaction_mode=TransactionMode.APP_TRANSFER,
#         transaction_type=TransactionType.PAYMENT_GATEWAY,
#         uow=uow,
#         mktg_svc=pmt_acl.FakeMarketingService(),
#     )
#     payment_commands.accept_payment_gateway_transaction(transaction_id=tx_id, uow=uow, mktg_svc= pmt_acl.FakeMarketingService())

#     marketing_recipient = marketing_queries.get_marketing_user(
#         user_id=recipient.id,
#         uow=uow,
#     )

#     assert marketing_recipient.loyalty_points == 10
#     assert payment_queries.get_wallet_balance(pg_wallet.id, uow) == 900
#     assert payment_queries.get_wallet_balance(recipient.wallet_id, uow) == (100 * 1.2)


# def test_add_and_set_missing_weightages_to_zero():
#     uow = UnitOfWork()
#     # p2p_push_weightage = uow.weightages.get(
#     #     weightage_type=TransactionType.P2P_PUSH
#     # )
#     # marketing_commands.add_and_set_missing_weightages_to_zero(uow=uow)
#     # updated_p2p_push_weightage = uow.weightages.get(
#     #     weightage_type=TransactionType.P2P_PUSH
#     # )

#     # assert p2p_push_weightage.weightage_value == updated_p2p_push_weightage.weightage_value

#     sql = """ delete from weightages"""
#     uow.cursor.execute(sql)
#     marketing_commands.add_and_set_missing_weightages_to_zero(uow=uow)

#     for transaction_type in TransactionType:
#         fetched_weightage = uow.weightages.get(weightage_type=transaction_type)

#         assert fetched_weightage.weightage_value == 0

#     uow.close_connection()
