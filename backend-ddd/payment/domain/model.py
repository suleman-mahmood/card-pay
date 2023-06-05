from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


class ClosedLoopState(str, Enum):
    UN_VERIFIED = 1
    PENDING = 2
    VERIFIED = 3


@dataclass
class ClosedLoop:
    """Closed loop model"""

    closed_loop_id: str
    closed_loop_name: str
    status: ClosedLoopState = ClosedLoopState.UN_VERIFIED


@dataclass
class User:
    """User model"""

    user_id: str
    full_name: str = ""
    phone_number: str = ""

    email: str = ""
    personal_email: str = ""

    loops: List[ClosedLoop] = False

    roll_number: Optional[str] = None
    referral_roll_number: Optional[str] = None

    pin: str = ""
    role: str = ""


@dataclass(frozen=True)
class Transaction:
    transaction_id: str


@dataclass
class Wallet:
    """Wallet model"""

    wallet_id: str
    balance: int = 0

    email: str = ""
    personal_email: str = ""

    pending_deposits: bool = False
    pin: str = ""
    role: str = ""

    transactions: List[Transaction] = field(default_factory=list)
