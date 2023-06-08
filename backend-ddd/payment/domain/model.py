from dataclasses import dataclass, field
from typing import List
from enum import Enum
from datetime import datetime
from .exceptions import TransactionNotAllowedException
from uuid import uuid4

"""
Use cases
"""


# This will be moved to marketing domain
# referral_roll_number: Optional[str] = None


class UserType(str, Enum):
    """User type enum"""

    CUSTOMER = 1  # Student, Faculty, Staff, etc.
    VENDOR = 2  # Shopkeeper, Society, Student Council etc.
    ADMIN = 3  # Admin of the closed loop system


# This can goto authentication domain
@dataclass
class User:
    """
    -> User entity - Aggregate root
    -> User manages transactions
    """

    # Unique identifiers for the user
    id: str
    qr_code: str
    pin: str
    wallet_id: str
    user_type: UserType  # Previously role
    phone_number: str = ""
    email: str = ""  # Personal email
    full_name: str = ""


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

    # def p2p_transaction(self, user: User):
    #     if user.user_type != UserType.CUSTOMER:
    #         raise TransactionNotAllowedException(
    #             "p2p is only allowed for user type customer"
    #         )
