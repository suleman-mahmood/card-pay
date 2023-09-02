import pytest

from core.authentication.entrypoint import commands as auth_cmd
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import queries as pmt_qry
from core.payment.domain import model as pmt_mdl
from core.marketing.entrypoint import commands as mkt_cmd
from core.authentication.tests.conftest import *
from core.entrypoint.uow import UnitOfWork

def test_get_all_successful_transactions_of_a_user(seed_verified_auth_user, seed_auth_closed_loop):
    uow = UnitOfWork()
    
    user_1 = seed_verified_auth_user(uow)
    user_2 = seed_verified_auth_user(uow)

    closed_loop = seed_auth_closed_loop(uow)

    user_1 = auth_cmd.register_closed_loop(
        user_id=user_1.id,
        closed_loop_id=closed_loop.id,
        unique_identifier="26100279",
        uow = uow
    )
    auth_cmd.verify_closed_loop(
        user_id=user_1.id,
        closed_loop_id=closed_loop.id,
        unique_identifier_otp=user_1.closed_loops[closed_loop.id].unique_identifier_otp,
        uow = uow
    )

    user_2 = auth_cmd.register_closed_loop(
        user_id=user_2.id,
        closed_loop_id=closed_loop.id,
        unique_identifier="25110542",
        uow = uow
    )
    auth_cmd.verify_closed_loop(
        user_id=user_2.id,
        closed_loop_id=closed_loop.id,
        unique_identifier_otp=user_2.closed_loops[closed_loop.id].unique_identifier_otp,
        uow = uow
    )
    
    mkt_cmd.add_and_set_missing_weightages_to_zero(uow=uow)

    uow.transactions.add_1000_wallet(wallet_id=user_1.id)

    tx_1 = pmt_cmd.execute_transaction_unique_identifier(
        sender_unique_identifier="26100279",
        recipient_unique_identifier="25110542",
        closed_loop_id=closed_loop.id,
        amount=100,
        transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
        uow=uow,
    )

    tx_2 = pmt_cmd.execute_transaction_unique_identifier(
        sender_unique_identifier="25110542",
        recipient_unique_identifier="26100279",
        closed_loop_id=closed_loop.id,
        amount=100,
        transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.P2P_PULL,
        uow=uow,
    )

    assert len(pmt_qry.get_all_successful_transactions_of_a_user(user_id=user_1.id, page_size=50, offset=0, uow=uow)) == 1 

    pmt_cmd.accept_p2p_pull_transaction(
        transaction_id=tx_2.id,
        uow=uow,
    )
    assert len(pmt_qry.get_all_successful_transactions_of_a_user(user_id=user_1.id, page_size=50, offset=0, uow=uow)) == 2 

    uow.close_connection()


