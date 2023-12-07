from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from core.authentication.domain import model as auth_mdl
from core.payment.domain import model as payment_mdl
from psycopg2.extras import DictRow


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
    paypro_id: str
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
            paypro_id=row["paypro_id"],
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


@dataclass(frozen=True)
class DailySuccessfulDepositsDTO:
    day: datetime
    successful_deposit_count: int
    total_amount: int
    avg_amount: int
    heros: List[str]

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "DailySuccessfulDepositsDTO":
        return DailySuccessfulDepositsDTO(
            day=row["day"],
            successful_deposit_count=row["successful_deposit_count"],
            total_amount=row["total_amount"],
            avg_amount=row["avg_amount"],
            heros=row["heros"],
        )


@dataclass(frozen=True)
class DailyPendingDepositsDTO:
    day: datetime
    pending_deposit_count: int
    total_amount: int
    avg_amount: int
    heros: List[str]

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "DailyPendingDepositsDTO":
        return DailyPendingDepositsDTO(
            day=row["day"],
            pending_deposit_count=row["pending_deposit_count"],
            total_amount=row["total_amount"],
            avg_amount=row["avg_amount"],
            heros=row["pending_heros"],
        )


@dataclass(frozen=True)
class DailyTransactionsDTO:
    day: datetime
    transaction_count: int
    total_amount: int
    avg_amount: int

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "DailyTransactionsDTO":
        return DailyTransactionsDTO(
            day=row["day"],
            transaction_count=row["transaction_count"],
            total_amount=row["total_amount"],
            avg_amount=row["avg_amount"],
        )


@dataclass(frozen=True)
class MonthlyTransactionsDTO:
    month: datetime
    transaction_count: int
    total_amount: int
    avg_amount: int

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "MonthlyTransactionsDTO":
        return MonthlyTransactionsDTO(
            month=row["month"],
            transaction_count=row["transaction_count"],
            total_amount=row["total_amount"],
            avg_amount=row["avg_amount"],
        )


@dataclass(frozen=True)
class DepositTransactionDTO:
    id: str
    paypro_id: str
    amount: float
    mode: payment_mdl.TransactionMode
    transaction_type: payment_mdl.TransactionType
    status: payment_mdl.TransactionStatus
    created_at: datetime
    last_updated: datetime

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "DepositTransactionDTO":
        return DepositTransactionDTO(
            id=row["id"],
            paypro_id=row["paypro_id"],
            amount=row["amount"],
            mode=payment_mdl.TransactionMode[row["mode"]],
            transaction_type=payment_mdl.TransactionType[row["transaction_type"]],
            status=payment_mdl.TransactionStatus[row["status"]],
            created_at=row["created_at"],
            last_updated=row["last_updated"],
        )


@dataclass(frozen=True)
class PayProAndTxIDsDTO:
    tx_id: str
    paypro_id: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "PayProAndTxIDsDTO":
        return PayProAndTxIDsDTO(
            tx_id=row["id"],
            paypro_id=row["paypro_id"],
        )


@dataclass(frozen=True)
class PayProOrderResponseDTO:
    tx_id: str
    paypro_id: str
    tx_status: str
    amount: int

    @classmethod
    def from_pp_api(cls, response: Dict) -> "PayProOrderResponseDTO":
        return PayProOrderResponseDTO(
            tx_id=response.get("OrderId", ""),
            paypro_id=response.get("PayProId", ""),
            tx_status=response.get("TransactionStatus", ""),
            amount=response.get("Amount Paid", 0),
        )


@dataclass(frozen=True)
class DepositRequest:
    tx_id: str
    created_at: str
    last_updated: str
    amount: int
    recipient_name: str
    sender_name: str
    status: str
    paypro_id: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "DepositRequest":
        return DepositRequest(
            tx_id=row["id"],
            created_at=row["created_at"],
            last_updated=row["last_updated"],
            amount=row["amount"],
            recipient_name=row["recipient_name"],
            sender_name=row["sender_name"],
            status=row["status"],
            paypro_id=row["paypro_id"],
        )


@dataclass(frozen=True)
class DailyUserCheckpoints:
    day: str
    total_users: int
    phone_verified_users: int
    lums_registered_users: int
    lums_verified_users: int
    signup_success_users: int
    pending_deposit_users: int
    successful_deposit_users: int
    percentage_acquisition: float

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "DailyUserCheckpoints":
        return DailyUserCheckpoints(
            day=row["day"],
            total_users=row["total_users"],
            phone_verified_users=row["phone_verified_users"],
            lums_registered_users=row["lums_registered_users"],
            lums_verified_users=row["lums_verified_users"],
            signup_success_users=row["signup_success_users"],
            pending_deposit_users=row["pending_deposit_users"],
            successful_deposit_users=row["successful_deposit_users"],
            percentage_acquisition=row["percentage_acquisition"],
        )


@dataclass(frozen=True)
class AmountWithIdDTO:
    id: str
    amount: int

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "AmountWithIdDTO":
        return AmountWithIdDTO(
            id=row["id"],
            amount=row["amount"],
        )
