from dataclasses import dataclass
from core.payment.domain import model as payment_mdl
from core.authentication.domain import model as auth_mdl
from datetime import datetime

@dataclass(frozen=True)
class VendorQrIdDTO:
    id: str
    full_name: str
    qr_id: str

@dataclass(frozen=True)
class TransactionWithIdsDTO:
    id: str
    amount: float
    mode: payment_mdl.TransactionMode
    transaction_type: payment_mdl.TransactionType
    status: payment_mdl.TransactionStatus
    created_at: datetime
    last_updated: datetime
    sender_id: str
    recipient_id: str
    sender_name: str
    recipient_name: str

@dataclass(frozen=True)
class UserWalletIDAndTypeDTO:
    user_wallet_id: str
    user_type: auth_mdl.UserType