"""payments microservices domain model"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from core.payment.domain import exceptions as ex

TX_UPPER_LIMIT = 10000


@dataclass
class Wallet:
    """Wallet entity"""

    id: str
    qr_id: str
    balance: int


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
    RECONCILIATION = 10  # reconciliation to cardpay by vendors
    EVENT_REGISTRATION_FEE = 11  # payment from a user to an event organizer


@dataclass
class Transaction:
    """
    Transaction entity - Aggregate root
    -> Transactions are sent over wallet ids
    """

    id: str
    paypro_id: str
    amount: int
    created_at: datetime
    last_updated: datetime

    mode: TransactionMode
    transaction_type: TransactionType
    status: TransactionStatus
    recipient_wallet: Wallet
    sender_wallet: Wallet

    def execute_transaction(self):
        """for executing a transaction"""

        if self.status == TransactionStatus.SUCCESSFUL:
            raise ex.TransactionNotAllowedException("Transaction is already executed")

        if self.amount > self.sender_wallet.balance:
            self.status = TransactionStatus.FAILED
            raise ex.TransactionNotAllowedException("Insufficient balance in sender's wallet")

        if (
            self.transaction_type != TransactionType.RECONCILIATION
            and self.amount >= TX_UPPER_LIMIT
        ):
            self.status = TransactionStatus.FAILED
            raise ex.TransactionNotAllowedException(
                f"Amount is greater than or equal to {TX_UPPER_LIMIT}"
            )

        if not isinstance(self.amount, int):
            self.status = TransactionStatus.FAILED
            raise ex.TransactionNotAllowedException("Constraint violated, amount is not an integer")

        if self.amount <= 0:
            self.status = TransactionStatus.FAILED
            raise ex.TransactionNotAllowedException("Amount is zero or negative")

        if self.recipient_wallet.id == self.sender_wallet.id:
            self.status = TransactionStatus.FAILED
            raise ex.TransactionNotAllowedException(
                "Constraint violated, sender and recipient wallets are the same"
            )

        self.sender_wallet.balance -= self.amount
        self.recipient_wallet.balance += self.amount
        self.status = TransactionStatus.SUCCESSFUL
        self.last_updated = datetime.now()

    def accept_p2p_pull_transaction(self):
        """for accepting a p2p pull transaction"""
        if self.transaction_type != TransactionType.P2P_PULL:
            raise ex.TransactionNotAllowedException("This is not a p2p pull transaction")

        self.execute_transaction()

    def decline_p2p_pull_transaction(self):
        """for declining a p2p pull transaction"""
        if self.transaction_type != TransactionType.P2P_PULL:
            raise ex.TransactionNotAllowedException("This is not a p2p pull transaction")

        self.status = TransactionStatus.DECLINED
        self.last_updated = datetime.now()

    def redeem_voucher(self):
        """for validating and redeeming vouchers"""
        if self.transaction_type != TransactionType.VOUCHER:
            raise ex.TransactionNotAllowedException("This is not a voucher redemption transaction")

        if self.status != TransactionStatus.PENDING:
            raise ex.TransactionNotAllowedException(
                "Constraint violated, voucher is no longer valid"
            )

        self.execute_transaction()

    def add_paypro_id(self, paypro_id: str):
        self.paypro_id = paypro_id
