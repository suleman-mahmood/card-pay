# """Payments micro-service commands"""

# from time import sleep
# from uuid import uuid4

# from core.entrypoint.uow import UnitOfWork
# from core.payment.entrypoint import paypro_service as pp_svc

# # Keep these commented, only for testing at certain times


# def test_get_paypro_token():
#     uow = UnitOfWork()

#     token = pp_svc._get_paypro_auth_token(uow=uow)
#     sleep(1)
#     token_2 = pp_svc._get_paypro_auth_token(uow=uow)

#     assert token == token_2


# def test_get_deposit_checkout_url():
#     uow = UnitOfWork()

#     payment_url = pp_svc.get_deposit_checkout_url(
#         amount=500,
#         transaction_id=str(uuid4()),
#         email="test@tdd.com",
#         full_name="TDD test case",
#         phone_number="03333333333",
#         uow=uow,
#     )

#     print(payment_url)

#     assert payment_url is not None
#     assert False


# # def _get_latest_failed_txn_of_user(user_id: str, uow: AbstractUnitOfWork):
# #     sql = """
# #         select id from transactions txn
# #         where (sender_wallet_id = %s or recipient_wallet_id = %s)
# #         and status = 'FAILED'::transaction_status_enum
# #         order by created_at desc
# #     """
# #     uow.cursor.execute(sql, [user_id, user_id])
# #     rows = uow.cursor.fetchone()

# #     return uow.transactions.get(transaction_id=rows[0])
