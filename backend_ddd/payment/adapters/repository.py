"""payments microservices repository"""

from abc import ABC, abstractmethod
from ..domain.model import Transaction, Wallet, TransactionMode, TransactionStatus


class TransactionAbstractRepository(ABC):
    """Transaction Abstract Repository"""

    @abstractmethod
    def add(self, transaction: Transaction):
        pass

    def add_wallet(self, wallet: Wallet):
        pass

    @abstractmethod
    def get(self, transaction_id: str) -> Transaction:
        pass

    @abstractmethod
    def get_by_wallet_ids(
        self,
        amount: int,
        mode: TransactionMode,
        transaction_type=TransactionStatus,
        sender_wallet_id=str,
        recipient_wallet_id=str,
    ) -> Transaction:
        pass

    @abstractmethod
    def save(self, transaction: Transaction):
        pass


class FakeTransactionRepository(TransactionAbstractRepository):
    """Fake Transaction Repository"""

    def __init__(self):
        self.transactions = {}
        self.wallets = {}

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

    def get_by_wallet_ids(
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

    # only for test
    def add_1000_wallet(self, wallet: Wallet):
        wallet.balance += 1000
        self.wallets[wallet.id] = wallet

    def save(self, transaction: Transaction):
        self.transactions[transaction.id] = transaction
        self.wallets[transaction.sender_wallet.id] = transaction.sender_wallet
        self.wallets[transaction.recipient_wallet.id] = transaction.recipient_wallet
