"""payments microservices repository"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict

from core.payment.domain import exceptions as ex
from core.payment.domain import model as mdl


class TransactionAbstractRepository(ABC):
    """Transaction Abstract Repository"""

    @abstractmethod
    def add(self, transaction: mdl.Transaction):
        pass

    @abstractmethod
    def add_wallet(self, wallet: mdl.Wallet):
        pass

    @abstractmethod
    def get(self, transaction_id: str) -> mdl.Transaction:
        pass

    @abstractmethod
    def get_wallets_create_transaction(
        self,
        id: str,
        amount: int,
        created_at: datetime,
        last_updated: datetime,
        mode: mdl.TransactionMode,
        transaction_type: mdl.TransactionType,
        status: mdl.TransactionStatus,
        sender_wallet_id: str,
        recipient_wallet_id: str,
    ) -> mdl.Transaction:
        pass

    @abstractmethod
    def get_with_different_recipient(
        self, transaction_id: str, recipient_wallet_id: str
    ) -> mdl.Transaction:
        pass

    @abstractmethod
    def save(self, transaction: mdl.Transaction):
        pass


class FakeTransactionRepository(TransactionAbstractRepository):
    """Fake Transaction Repository"""

    def __init__(self):
        self.transactions: Dict[str, mdl.Transaction] = {}
        self.wallets: Dict[str, mdl.Wallet] = {}

    def add(self, transaction: mdl.Transaction):
        self.transactions[transaction.id] = transaction
        self.wallets[transaction.sender_wallet.id] = transaction.sender_wallet
        self.wallets[transaction.recipient_wallet.id] = transaction.recipient_wallet

    def add_wallet(self, wallet: mdl.Wallet):
        self.wallets[wallet.id] = wallet

    def get(self, transaction_id: str) -> mdl.Transaction:
        tx = self.transactions[transaction_id]
        tx.sender_wallet = self.wallets[tx.sender_wallet.id]
        tx.recipient_wallet = self.wallets[tx.recipient_wallet.id]
        return tx

    def get_wallets_create_transaction(
        self,
        id: str,
        amount: int,
        created_at: datetime,
        last_updated: datetime,
        mode: mdl.TransactionMode,
        transaction_type: mdl.TransactionType,
        status: mdl.TransactionStatus,
        sender_wallet_id: str,
        recipient_wallet_id: str,
    ) -> mdl.Transaction:
        sender_wallet = self.wallets[str(sender_wallet_id)]
        recipient_wallet = self.wallets[str(recipient_wallet_id)]
        return mdl.Transaction(
            amount=amount,
            paypro_id="",
            mode=mode,
            transaction_type=transaction_type,
            status=status,
            recipient_wallet=recipient_wallet,
            sender_wallet=sender_wallet,
            id=id,
            created_at=created_at,
            last_updated=last_updated,
        )

    def get_with_different_recipient(
        self, transaction_id: str, recipient_wallet_id: str
    ) -> mdl.Transaction:
        tx = self.transactions[transaction_id]
        tx.sender_wallet = self.wallets[tx.sender_wallet.id]
        tx.recipient_wallet = self.wallets[recipient_wallet_id]
        return tx

    def get_wallet(self, wallet_id: str):
        return self.wallets[wallet_id]

    def save(self, transaction: mdl.Transaction):
        self.transactions[transaction.id] = transaction
        self.wallets[transaction.sender_wallet.id] = transaction.sender_wallet
        self.wallets[transaction.recipient_wallet.id] = transaction.recipient_wallet


class TransactionRepository(TransactionAbstractRepository):
    """Transaction Repository"""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, transaction: mdl.Transaction):
        # updating transactions
        sql = """
            insert into transactions (id, paypro_id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id, created_at, last_updated, ghost)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            sql,
            [
                transaction.id,
                transaction.paypro_id,
                transaction.amount,
                transaction.mode.name,
                transaction.transaction_type.name,
                transaction.status.name,
                transaction.sender_wallet.id,
                transaction.recipient_wallet.id,
                transaction.created_at,
                transaction.last_updated,
                transaction.ghost,
            ],
        )
        # updating wallets
        sql = """
            update wallets
            set balance = %s
            where id=%s
        """
        self.cursor.execute(
            sql,
            [
                transaction.sender_wallet.balance,
                transaction.sender_wallet.id,
            ],
        )
        self.cursor.execute(
            sql,
            [
                transaction.recipient_wallet.balance,
                transaction.recipient_wallet.id,
            ],
        )

    def add_wallet(self, wallet: mdl.Wallet):
        sql = """
            insert into wallets (id, balance, qr_id)
            values (%s, %s, %s)
        """
        self.cursor.execute(
            sql,
            [
                wallet.id,
                wallet.balance,
                wallet.qr_id,
            ],
        )

    def get(self, transaction_id: str) -> mdl.Transaction:
        sql = """
            select id, paypro_id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id, created_at, last_updated, ghost
            from transactions
            where id=%s 
            for update
        """
        self.cursor.execute(sql, [transaction_id])
        transaction_row = self.cursor.fetchone()

        if transaction_row is None:
            raise ex.TransactionNotFoundException(
                f"no transaction object found for id {transaction_id}"
            )

        sql = """
            select id, balance, qr_id
            from wallets
            where id=%s
            for update
        """

        self.cursor.execute(sql, [transaction_row[6]])
        sender_wallet_row = self.cursor.fetchone()

        self.cursor.execute(sql, [transaction_row[7]])
        recipient_wallet_row = self.cursor.fetchone()

        return mdl.Transaction(
            id=transaction_row[0],
            paypro_id=transaction_row[1],
            amount=transaction_row[2],
            mode=mdl.TransactionMode[transaction_row[3]],
            transaction_type=mdl.TransactionType[transaction_row[4]],
            status=mdl.TransactionStatus[transaction_row[5]],
            sender_wallet=mdl.Wallet(
                id=transaction_row[6],
                balance=sender_wallet_row[1],
                qr_id=sender_wallet_row[2],
            ),
            recipient_wallet=mdl.Wallet(
                id=transaction_row[7],
                balance=recipient_wallet_row[1],
                qr_id=recipient_wallet_row[2],
            ),
            created_at=transaction_row[8],
            last_updated=transaction_row[9],
            ghost=transaction_row[10],
        )

    def get_wallets_create_transaction(
        self,
        id: str,
        amount: int,
        created_at: datetime,
        last_updated: datetime,
        mode: mdl.TransactionMode,
        transaction_type: mdl.TransactionType,
        status: mdl.TransactionStatus,
        sender_wallet_id: str,
        recipient_wallet_id: str,
    ) -> mdl.Transaction:
        sql = """
            select id, balance, qr_id
            from wallets
            where id=%s
            for update
        """
        self.cursor.execute(sql, [sender_wallet_id])
        sender_wallet_row = self.cursor.fetchone()
        self.cursor.execute(sql, [recipient_wallet_id])
        recipient_wallet_row = self.cursor.fetchone()

        return mdl.Transaction(
            amount=amount,
            paypro_id="",
            mode=mode,
            transaction_type=transaction_type,
            status=status,
            recipient_wallet=mdl.Wallet(
                id=recipient_wallet_id,
                balance=recipient_wallet_row[1],
                qr_id=recipient_wallet_row[2],
            ),
            sender_wallet=mdl.Wallet(
                id=sender_wallet_id,
                balance=sender_wallet_row[1],
                qr_id=sender_wallet_row[2],
            ),
            id=id,
            created_at=created_at,
            last_updated=last_updated,
        )

    def get_with_different_recipient(
        self, transaction_id: str, recipient_wallet_id: str
    ) -> mdl.Transaction:
        # as voucher has same recipient and sender wallet, we need to change the recipient wallet
        sql = """
            select id, paypro_id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id, created_at, last_updated, ghost
            from transactions
            where id=%s 
            for update
        """
        self.cursor.execute(sql, [transaction_id])
        transaction_row = self.cursor.fetchone()

        if transaction_row is None:
            raise ex.TransactionNotFoundException(
                f"no transaction object found for id {transaction_id}"
            )

        sql = """
            select id, balance, qr_id
            from wallets
            where id=%s
            for update
        """

        self.cursor.execute(sql, [transaction_row[6]])
        sender_wallet_row = self.cursor.fetchone()
        self.cursor.execute(sql, [recipient_wallet_id])
        recipient_wallet_row = self.cursor.fetchone()

        return mdl.Transaction(
            id=transaction_row[0],
            paypro_id=transaction_row[1],
            amount=transaction_row[2],
            mode=mdl.TransactionMode[transaction_row[3]],
            transaction_type=mdl.TransactionType[transaction_row[4]],
            status=mdl.TransactionStatus[transaction_row[5]],
            sender_wallet=mdl.Wallet(
                id=transaction_row[6],
                balance=sender_wallet_row[1],
                qr_id=sender_wallet_row[2],
            ),
            recipient_wallet=mdl.Wallet(
                id=recipient_wallet_id,
                balance=recipient_wallet_row[1],
                qr_id=recipient_wallet_row[2],
            ),
            created_at=transaction_row[8],
            last_updated=transaction_row[9],
            ghost=transaction_row[10],
        )

    def save(self, transaction: mdl.Transaction):
        sql = """
            insert into transactions (id, paypro_id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id, created_at, last_updated, ghost)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            on conflict (id) do update set
                paypro_id = excluded.paypro_id,
                amount = excluded.amount,
                mode = excluded.mode,
                transaction_type = excluded.transaction_type,
                status = excluded.status,
                sender_wallet_id = excluded.sender_wallet_id,
                recipient_wallet_id = excluded.recipient_wallet_id,
                created_at = excluded.created_at,
                last_updated = excluded.last_updated,
                ghost = excluded.ghost
        """
        self.cursor.execute(
            sql,
            [
                transaction.id,
                transaction.paypro_id,
                transaction.amount,
                transaction.mode.name,
                transaction.transaction_type.name,
                transaction.status.name,
                transaction.sender_wallet.id,
                transaction.recipient_wallet.id,
                transaction.created_at,
                transaction.last_updated,
                transaction.ghost,
            ],
        )
        # updating wallets
        sql = """
            update wallets
            set balance = %s
            where id=%s
        """
        self.cursor.execute(
            sql,
            [
                transaction.sender_wallet.balance,
                transaction.sender_wallet.id,
            ],
        )
        self.cursor.execute(
            sql,
            [
                transaction.recipient_wallet.balance,
                transaction.recipient_wallet.id,
            ],
        )


class RetailProTransactionAbstractRepository(ABC):
    """RetailPro Abstract Repository"""

    @abstractmethod
    def add(self, rp_transaction: mdl.RetailProTransactions):
        pass

    @abstractmethod
    def get(self, rp_transaction_id: str) -> mdl.RetailProTransactions:
        pass

    @abstractmethod
    def save(self, rp_transaction: mdl.RetailProTransactions):
        pass

class FakeRetailProTransactionRepository(RetailProTransactionAbstractRepository):
    """Fake Retail Pro Transaction Repository"""

    def __init__(self):
        self.rp_transactions: Dict[str, mdl.RetailProTransactions] = {}

    def add(self, rp_transaction: mdl.RetailProTransactions):
        self.rp_transactions[rp_transaction.tx_id] = rp_transaction

    def get(self, rp_transaction_id: str) -> mdl.RetailProTransactions:
        return self.rp_transactions[rp_transaction_id]

    def save(self, rp_transaction: mdl.RetailProTransactions):
        self.rp_transactions[rp_transaction.tx_id] = rp_transaction

class RetailProTransactionRepository(RetailProTransactionAbstractRepository):
    """Retail Pro Transaction Repository"""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, rp_transaction: mdl.RetailProTransactions):
        # updating retail pro transactions
        sql = """
            insert into rp_transactions (tx_id, document_id)
            values (%s, %s)
        """
        self.cursor.execute(
            sql,
            [
                rp_transaction.tx_id,
                rp_transaction.document_id
            ],
        )

    def get(self, rp_transaction_id: str) -> mdl.RetailProTransactions:
        sql = """
            select tx_id, document_id
            from rp_transactions
            where tx_id=%s 
            for update
        """
        self.cursor.execute(sql, [rp_transaction_id])
        rp_transaction_row = self.cursor.fetchone()

        if rp_transaction_row is None:
            raise ex.RetailProTransactionNotFoundException(
                f"no retail pro transaction object found for id {rp_transaction_id}"
            )

        return mdl.RetailProTransactions(
            tx_id=rp_transaction_row[0],
            document_id=rp_transaction_row[1]
        )

    def save(self, rp_transaction: mdl.RetailProTransactions):
        sql = """
            insert into rp_transactions (tx_id, document_id)
            values (%s, %s)
            on conflict (tx_id) do update set
                document_id = excluded.document_id
        """
        self.cursor.execute(
            sql,
            [
                rp_transaction.tx_id,
                rp_transaction.document_id
            ],
        )
