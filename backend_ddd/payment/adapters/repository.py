"""payments microservices repository"""

from abc import ABC, abstractmethod
from typing import Dict
from ..domain.model import (
    Transaction,
    Wallet,
    TransactionMode,
    TransactionStatus,
    TransactionType,
)
from ..domain.exceptions import TransactionNotFoundException


class TransactionAbstractRepository(ABC):
    """Transaction Abstract Repository"""

    @abstractmethod
    def add(self, transaction: Transaction):
        pass

    @abstractmethod
    def add_wallet(self, wallet: Wallet):
        pass

    @abstractmethod
    def get(self, transaction_id: str) -> Transaction:
        pass

    @abstractmethod
    def get_wallets_create_transaction(
        self,
        amount: int,
        mode: TransactionMode,
        transaction_type=TransactionStatus,
        sender_wallet_id=str,
        recipient_wallet_id=str,
    ) -> Transaction:
        pass

    @abstractmethod
    def get_with_different_recipient(
        self, transaction_id: str, recipient_wallet_id: str
    ) -> Transaction:
        pass

    @abstractmethod
    def save(self, transaction: Transaction):
        pass


class FakeTransactionRepository(TransactionAbstractRepository):
    """Fake Transaction Repository"""

    def __init__(self):
        self.transactions: Dict[str, Transaction] = {}
        self.wallets: Dict[str, Wallet] = {}

    def add(self, transaction: Transaction):
        self.transactions[transaction.id] = transaction
        self.wallets[transaction.sender_wallet.id] = transaction.sender_wallet
        self.wallets[transaction.recipient_wallet.id] = transaction.recipient_wallet

    def add_wallet(self, wallet: Wallet):
        self.wallets[wallet.id] = wallet

    def get(self, transaction_id: str) -> Transaction:
        tx = self.transactions[transaction_id]
        tx.sender_wallet = self.wallets[tx.sender_wallet.id]
        tx.recipient_wallet = self.wallets[tx.recipient_wallet.id]
        return tx

    def get_wallets_create_transaction(
        self,
        amount: int,
        mode: TransactionMode,
        transaction_type=TransactionStatus,
        sender_wallet_id=str,
        recipient_wallet_id=str,
    ) -> Transaction:
        sender_wallet = self.wallets[sender_wallet_id]
        recipient_wallet = self.wallets[recipient_wallet_id]
        return Transaction(
            amount=amount,
            mode=mode,
            transaction_type=transaction_type,
            recipient_wallet=recipient_wallet,
            sender_wallet=sender_wallet,
        )

    def get_with_different_recipient(
        self, transaction_id: str, recipient_wallet_id: str
    ) -> Transaction:
        tx = self.transactions[transaction_id]
        tx.sender_wallet = self.wallets[tx.sender_wallet.id]
        tx.recipient_wallet = self.wallets[recipient_wallet_id]
        return tx

    # only for test
    def add_1000_wallet(self, wallet: Wallet):
        wallet.balance += 1000
        self.wallets[wallet.id] = wallet

    def save(self, transaction: Transaction):
        self.transactions[transaction.id] = transaction
        self.wallets[transaction.sender_wallet.id] = transaction.sender_wallet
        self.wallets[transaction.recipient_wallet.id] = transaction.recipient_wallet


class TransactionRepository(TransactionAbstractRepository):
    """Transaction Repository"""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, transaction: Transaction):
        # updating transactions
        sql = """
            insert into transactions (id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id, created_at, last_updated)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            sql,
            [
                transaction.id,
                transaction.amount,
                transaction.mode.name,
                transaction.transaction_type.name,
                transaction.status.name,
                transaction.sender_wallet.id,
                transaction.recipient_wallet.id,
                transaction.created_at,
                transaction.last_updated,
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

    def add_wallet(self, wallet: Wallet):
        sql = """
            insert into wallets (id, balance)
            values (%s, %s)
        """
        self.cursor.execute(
            sql,
            [
                wallet.id,
                wallet.balance,
            ],
        )

    def get(self, transaction_id: str) -> Transaction:
        sql = """
            select id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id, created_at, last_updated
            from transactions
            where id=%s 
            for update
        """
        self.cursor.execute(sql, [transaction_id])
        transaction_row = self.cursor.fetchone()

        if transaction_row is None:
            raise TransactionNotFoundException(
                f"no transaction object found for id {transaction_id}"
            )

        sql = """
            select id, balance
            from wallets
            where id=%s
            for update
        """

        self.cursor.execute(sql, [transaction_row[5]])
        sender_wallet_row = self.cursor.fetchone()

        self.cursor.execute(sql, [transaction_row[6]])
        recipient_wallet_row = self.cursor.fetchone()

        return Transaction(
            id=transaction_row[0],
            amount=transaction_row[1],
            mode=TransactionMode[transaction_row[2]],
            transaction_type=TransactionType[transaction_row[3]],
            status=TransactionStatus[transaction_row[4]],
            sender_wallet=Wallet(id=transaction_row[5], balance=sender_wallet_row[1]),
            recipient_wallet=Wallet(
                id=transaction_row[6], balance=recipient_wallet_row[1]
            ),
            created_at=transaction_row[7],
            last_updated=transaction_row[8],
        )

    def get_wallets_create_transaction(
        self,
        amount: int,
        mode: TransactionMode,
        transaction_type=TransactionStatus,
        sender_wallet_id=str,
        recipient_wallet_id=str,
    ) -> Transaction:
        sql = """
            select id, balance 
            from wallets
            where id=%s
            for update
        """
        print(sender_wallet_id)
        self.cursor.execute(sql, [sender_wallet_id])
        sender_wallet_row = self.cursor.fetchone()
        print(sender_wallet_row)
        print(recipient_wallet_id)
        self.cursor.execute(sql, [recipient_wallet_id])
        recipient_wallet_row = self.cursor.fetchone()
        print(recipient_wallet_row)

        return Transaction(
            amount=amount,
            mode=mode,
            transaction_type=transaction_type,
            recipient_wallet=Wallet(
                id=recipient_wallet_id, balance=recipient_wallet_row[1]
            ),
            sender_wallet=Wallet(id=sender_wallet_id, balance=sender_wallet_row[1]),
        )

    def get_with_different_recipient(
        self, transaction_id: str, recipient_wallet_id: str
    ) -> Transaction:
        # as voucher has same recipient and sender wallet, we need to change the recipient wallet
        sql = """
            select id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id, created_at, last_updated
            from transactions
            where id=%s 
            for update
        """
        self.cursor.execute(sql, [transaction_id])
        transaction_row = self.cursor.fetchone()

        if transaction_row is None:
            raise TransactionNotFoundException(
                f"no transaction object found for id {transaction_id}"
            )

        sql = """
            select id, balance
            from wallets
            where id=%s
            for update
        """

        self.cursor.execute(sql, [transaction_row[5]])
        sender_wallet_row = self.cursor.fetchone()

        self.cursor.execute(sql, recipient_wallet_id)
        recipient_wallet_row = self.cursor.fetchone()

        return Transaction(
            id=transaction_row[0],
            amount=transaction_row[1],
            mode=TransactionMode[transaction_row[2]],
            transaction_type=TransactionStatus[transaction_row[3]],
            status=TransactionStatus[transaction_row[4]],
            sender_wallet=Wallet(id=transaction_row[5], balance=sender_wallet_row[1]),
            recipient_wallet=Wallet(
                id=recipient_wallet_id, balance=recipient_wallet_row[1]
            ),
            created_at=transaction_row[7],
            last_updated=transaction_row[8],
        )

    def save(self, transaction: Transaction):
        sql = """
            insert into transactions (id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id, created_at, last_updated)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            on conflict (id) do update set
                amount = excluded.amount,
                mode = excluded.mode,
                transaction_type = excluded.transaction_type,
                status = excluded.status,
                sender_wallet_id = excluded.sender_wallet_id,
                recipient_wallet_id = excluded.recipient_wallet_id,
                created_at = excluded.created_at,
                last_updated = excluded.last_updated
        """
        self.cursor.execute(
            sql,
            [
                transaction.id,
                transaction.amount,
                transaction.mode.name,
                transaction.transaction_type.name,
                transaction.status.name,
                transaction.sender_wallet.id,
                transaction.recipient_wallet.id,
                transaction.created_at,
                transaction.last_updated,
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

    def add_1000_wallet(self, wallet: Wallet):
        # update wallet balance
        sql = """
            update wallets
            set balance = %s
            where id=%s
        """
        self.cursor.execute(
            sql,
            [
                1000,
                wallet.id,
            ],
        )
