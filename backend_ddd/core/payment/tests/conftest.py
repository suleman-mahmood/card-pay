from datetime import datetime
from uuid import uuid4

import pytest
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import anti_corruption as auth_acl
from core.authentication.entrypoint import commands as auth_cmd
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import commands as pmt_cmd
import rsa


@pytest.fixture
def seed_wallet():
    def _seed_wallet() -> pmt_mdl.Wallet:
        return pmt_mdl.Wallet(id=str(uuid4()), qr_id=str(uuid4()), balance=0)

    return _seed_wallet


@pytest.fixture
def seed_txn(seed_wallet):
    def _seed_txn(
        tx_id=str(uuid4()),
        amount=100,
        created_at=datetime.now(),
        last_updated=datetime.now(),
        mode=pmt_mdl.TransactionMode.APP_TRANSFER,
        transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
        status=pmt_mdl.TransactionStatus.SUCCESSFUL,
        recipient_wallet=seed_wallet(),
        sender_wallet=seed_wallet(),
    ) -> pmt_mdl.Transaction:
        return pmt_mdl.Transaction(
            id=tx_id,
            paypro_id="",
            amount=amount,
            created_at=created_at,
            last_updated=last_updated,
            mode=mode,
            transaction_type=transaction_type,
            status=status,
            recipient_wallet=recipient_wallet,
            sender_wallet=sender_wallet,
        )

    return _seed_txn


# Fixtures for query tests


@pytest.fixture
def seed_5_100_transactions_against_user_ids(add_1000_wallet):
    def fixture_factory(sender_id, recipient_id, uow):
        """mega setup function for 5 transactions against 2 users each of 100 amount"""
        (public_key, private_key) = rsa.newkeys(512)
        public_key_str = public_key.save_pkcs1().decode("utf-8")
        private_key_str = private_key.save_pkcs1().decode("utf-8")
        sender = auth_mdl.User(
            id=sender_id,
            personal_email=auth_mdl.PersonalEmail(value="mlkmoaz@gmail.com"),
            phone_number=auth_mdl.PhoneNumber(value="03034952255"),
            user_type=auth_mdl.UserType.CUSTOMER,
            pin="0000",
            full_name="Malik Muhammad Moaz",
            location=auth_mdl.Location(latitude=13.2311, longitude=98.4888),
            wallet_id=sender_id,
            public_key=public_key_str,
            private_key=private_key_str
        )
        wallet: pmt_mdl.Wallet = pmt_mdl.Wallet(id=sender_id, qr_id=str(uuid4()), balance=0)
        uow.transactions.add_wallet(
            wallet=wallet,
        )
        uow.users.add(sender)

        (public_key_recipient, private_key_recipient) = rsa.newkeys(512)
        public_key_str_recipient = public_key_recipient.save_pkcs1().decode("utf-8")
        private_key_str_recipient = private_key_recipient.save_pkcs1().decode("utf-8")
        recipient = auth_mdl.User(
            id=recipient_id,
            personal_email=auth_mdl.PersonalEmail(value="mlkmoaz@gmail.com"),
            phone_number=auth_mdl.PhoneNumber(value="03034952255"),
            user_type=auth_mdl.UserType.CUSTOMER,
            pin="0000",
            full_name="Malik Muhammad Moaz",
            location=auth_mdl.Location(latitude=13.2311, longitude=98.4888),
            wallet_id=recipient_id,
            public_key=public_key_recipient,
            private_key=private_key_recipient
        )
        wallet: pmt_mdl.Wallet = pmt_mdl.Wallet(id=recipient_id, qr_id=str(uuid4()), balance=0)
        uow.transactions.add_wallet(
            wallet=wallet,
        )
        uow.users.add(recipient)

        add_1000_wallet(wallet_id=sender_id, uow=uow)

        for i in range(5):
            pmt_cmd._execute_transaction(
                tx_id=str(uuid4()),
                amount=100,
                transaction_mode=pmt_mdl.TransactionMode.APP_TRANSFER,
                transaction_type=pmt_mdl.TransactionType.P2P_PUSH,
                sender_wallet_id=sender_id,
                recipient_wallet_id=recipient_id,
                uow=uow,
                auth_svc=pmt_acl.FakeAuthenticationService(),
            )

    return fixture_factory


@pytest.fixture
def seed_two_verified_vendors_in_closed_loop(seed_verified_auth_vendor, seed_auth_closed_loop):
    def fixture_factory(uow):
        vendor_1, _ = seed_verified_auth_vendor(uow)
        vendor_2, _ = seed_verified_auth_vendor(uow)

        closed_loop_id = str(uuid4())
        seed_auth_closed_loop(id=closed_loop_id, uow=uow)

        for user_id in [vendor_1.id, vendor_2.id]:
            auth_cmd.register_closed_loop(
                user_id=user_id,
                closed_loop_id=closed_loop_id,
                unique_identifier="1234",
                uow=uow,
                auth_svc=auth_acl.FakeAuthenticationService(),
            )
            auth_cmd.verify_closed_loop(
                user_id=user_id,
                closed_loop_id=closed_loop_id,
                unique_identifier_otp=uow.users.get(user_id)
                .closed_loops[closed_loop_id]
                .unique_identifier_otp,
                ignore_migration=True,
                uow=uow,
                auth_svc=auth_acl.FakeAuthenticationService(),
            )

        return vendor_1, vendor_2, closed_loop_id

    return fixture_factory


@pytest.fixture
def get_qr_id_from_user_id():
    def fixture_factory(user_id, uow):
        sql = """
            SELECT qr_id
            FROM wallets
            WHERE id = %(user_id)s
        """
        uow.dict_cursor.execute(sql, {"user_id": user_id})
        qr_id = uow.dict_cursor.fetchone()["qr_id"]
        return qr_id

    return fixture_factory


@pytest.fixture
def seed_verified_user_in_closed_loop(seed_verified_auth_user, seed_auth_closed_loop):
    def fixture_factory(uow):
        user, _ = seed_verified_auth_user(uow)
        closed_loop_id = str(uuid4())
        seed_auth_closed_loop(id=closed_loop_id, uow=uow)

        auth_cmd.register_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop_id,
            unique_identifier="26100255",
            uow=uow,
            auth_svc=auth_acl.FakeAuthenticationService(),
        )

        fetched_user = uow.users.get(user.id)

        auth_cmd.verify_closed_loop(
            user_id=user.id,
            closed_loop_id=closed_loop_id,
            unique_identifier_otp=fetched_user.closed_loops[closed_loop_id].unique_identifier_otp,
            ignore_migration=True,
            uow=uow,
            auth_svc=auth_acl.FakeAuthenticationService(),
        )

        return user.id, closed_loop_id

    return fixture_factory
