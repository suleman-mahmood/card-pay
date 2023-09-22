from dataclasses import dataclass
from core.payment.domain import model as payment_mdl
from core.authentication.domain import model as auth_mdl
from datetime import datetime
from psycopg2.extras import DictRow
from typing import List


@dataclass(frozen=True)
class VendorQrIdDTO:
    id: str
    full_name: str
    qr_id: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "VendorQrIdDTO":
        return VendorQrIdDTO(
            id=row["id"],
            full_name=row["full_name"],
            qr_id=row["qr_id"],
        )


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

    @classmethod
    def from_db_dict_row(cls, row: DictRow):
        return TransactionWithIdsDTO(
            id=row["id"],
            amount=row["amount"],
            mode=row["mode"],
            transaction_type=row["transaction_type"],
            status=row["status"],
            created_at=row["created_at"],
            last_updated=row["last_updated"],
            sender_id=row["sender_id"],
            recipient_id=row["recipient_id"],
            sender_name=row["sender_name"],
            recipient_name=row["recipient_name"],
        )


@dataclass(frozen=True)
class UserWalletIDAndTypeDTO:
    user_wallet_id: str
    user_type: auth_mdl.UserType

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "UserWalletIDAndTypeDTO":
        return UserWalletIDAndTypeDTO(
            user_wallet_id=row["user_wallet_id"],
            user_type=auth_mdl.UserType[row["user_type"]],
        )


@dataclass(frozen=True)
class ClosedLoopIdNameDTO:

    id: str
    name: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "ClosedLoopIdNameDTO":
        return ClosedLoopIdNameDTO(
            id=row["id"],
            name=row["name"],
        )


@dataclass(frozen=True)
class CustomerDTO:
    id: str
    full_name: str
    wallet_id: str
    unique_identifier: str
    closed_loop_user_id: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "CustomerDTO":
        return CustomerDTO(
            id=row["id"],
            full_name=row["full_name"],
            wallet_id=row["wallet_id"],
            unique_identifier=row["unique_identifier"],
            closed_loop_user_id=row["closed_loop_user_id"],
        )


@dataclass(frozen=True)
class VendorDTO:
    id: str
    full_name: str
    wallet_id: str
    unique_identifier: str
    closed_loop_user_id: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "VendorDTO":
        return VendorDTO(
            id=row["id"],
            full_name=row["full_name"],
            wallet_id=row["wallet_id"],
            unique_identifier=row["unique_identifier"],
            closed_loop_user_id=row["closed_loop_user_id"],
        )


@dataclass(frozen=True)
class CountsDTO:
    customers: int
    vendors: int
    count: int


@dataclass(frozen=True)
class CustomerVendorCountsDTO:
    customers: List[CustomerDTO]
    vendors: List[VendorDTO]
    counts: CountsDTO


@dataclass(frozen=True)
class VendorAndBalanceDTO:
    id: str
    full_name: str
    wallet_id: str
    balance: int

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "VendorAndBalanceDTO":
        return VendorAndBalanceDTO(
            id=row["id"],
            full_name=row["full_name"],
            wallet_id=row["wallet_id"],
            balance=row["balance"],
        )

@dataclass(frozen=True)
class VendorIdNameAndWalletIdDTO:
    id: str
    full_name: str
    wallet_id: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "VendorIdNameAndWalletIdDTO":
        return VendorIdNameAndWalletIdDTO(
            id=row["id"],
            full_name=row["full_name"],
            wallet_id=row["wallet_id"],
        )

@dataclass(frozen=True)
class TransactionWithDates:

    id: str
    amount: int
    created_at: datetime
    last_updated: datetime

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "TransactionWithDates":
        return TransactionWithDates(
            id=row["id"],
            amount=row["amount"],
            created_at=row["created_at"],
            last_updated=row["last_updated"],
        )
