"""payments microservices domain model"""
from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum
from datetime import datetime
from .exceptions import TransactionNotAllowedException


@dataclass
class Wallet:
    """Wallet entity"""

    id: str
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
    VOUCHER = 4
    # Direct payment to event registrations, donations, trips etc; Ends at a vendor
    VIRTUAL_POS = 5
    PAYMENT_GATEWAY = 6
    CARD_PAY = 7  # source of tokens in cardpay
    CASH_BACK = 8  # Marketing
    REFERRAL = 9  # Marketing


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
    status: TransactionStatus = TransactionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def execute_transaction(self):
        """for executing a transaction"""
        if self.amount > self.sender_wallet.balance:
            self.status = TransactionStatus.FAILED
            raise TransactionNotAllowedException(
                "Insufficient balance in sender's wallet"
            )

        if self.amount <= 0:
            self.status = TransactionStatus.FAILED
            raise TransactionNotAllowedException("Amount is zero or negative")

        if self.recipient_wallet.id == self.sender_wallet.id:
            self.status = TransactionStatus.FAILED
            raise TransactionNotAllowedException(
                "Constraint violated, sender and recipient wallets are the same"
            )

        self.sender_wallet.balance -= self.amount
        self.recipient_wallet.balance += self.amount
        self.status = TransactionStatus.SUCCESSFUL

    def accept_p2p_pull_transaction(self):
        """for accepting a p2p pull transaction"""
        if self.transaction_type != TransactionType.P2P_PULL:
            raise TransactionNotAllowedException(
                "This is not a p2p pull transaction")

        self.execute_transaction()

    def decline_p2p_pull_transaction(self):
        """for declining a p2p pull transaction"""
        if self.transaction_type != TransactionType.P2P_PULL:
            raise TransactionNotAllowedException(
                "This is not a p2p pull transaction")

        self.status = TransactionStatus.DECLINED

    def redeem_voucher(self):
        """for validating and redeeming vouchers"""
        if self.transaction_type != TransactionType.VOUCHER:
            raise TransactionNotAllowedException(
                "This is not a voucher redemption transaction"
            )

        if self.status != TransactionStatus.PENDING:
            raise TransactionNotAllowedException(
                "Constraint violated, voucher is no longer valid"
            )

        self.execute_transaction()
