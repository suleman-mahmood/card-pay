from dataclasses import dataclass, field
from typing import List
from enum import Enum
from datetime import datetime
from .exceptions import TransactionNotAllowedException
from uuid import uuid4

"""
Use cases
"""


@dataclass
class Wallet:
    """Wallet entity"""

    id: str = field(default_factory=lambda: str(uuid4()))
    balance: int = 0


class TransactionStatus(str, Enum):
    """Transaction status enum"""

    PENDING = 1
    FAILED = 2
    SUCCESSFUL = 3
    EXPIRED = 4
    DECLINED = 5


class TransactionMode(str, Enum):
    """Transaction mode enum"""

    QR = 1
    RFID = 2
    NFC = 3
    BARCODE = 4
    APP_TRANSFER = 5


class TransactionType(str, Enum):
    """Transaction type enum"""

    POS = 1

    # Ends at another customer's wallet
    P2P_PUSH = 2
    P2P_PULL = 3

    # Direct payment to event registrations, donations, trips etc; Ends at a vendor
    VIRTUAL_POS = 4

    PAYMENT_GATEWAY = 5

    CARD_PAY = 6  # source of tokens in cardpay


@dataclass
class Transaction:
    """
    Transaction entity - Aggregate root
    -> Transactions are sent over wallet ids
    """

    amount: int
    mode: TransactionMode
    transaction_type: TransactionType

    recipient_wallet: Wallet
    sender_wallet: Wallet

    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    status: TransactionStatus = TransactionStatus.PENDING

    def make_transaction(self):
        if self.amount > self.sender_wallet.balance:
            self.status = TransactionStatus.FAILED
            raise TransactionNotAllowedException(
                "Insufficient balance in sender's wallet"
            )

        if self.recipient_wallet.id == self.sender_wallet.id:
            self.status = TransactionStatus.FAILED
            raise TransactionNotAllowedException(
                "Constraint violated, sender and recipient wallets are the same"
            )

        self.sender_wallet.balance -= self.amount
        self.recipient_wallet.balance += self.amount
        self.status = TransactionStatus.SUCCESSFUL

    def accept_p2p_pull_transaction(self):
        if self.transaction_type != TransactionType.P2P_PULL:
            raise TransactionNotAllowedException("This is not a p2p pull transaction")

        self.make_transaction()

    def decline_p2p_pull_transaction(self):
        if self.transaction_type != TransactionType.P2P_PULL:
            raise TransactionNotAllowedException("This is not a p2p pull transaction")

        self.status = TransactionStatus.DECLINED
