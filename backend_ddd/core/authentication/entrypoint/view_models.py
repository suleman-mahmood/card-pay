from dataclasses import dataclass
from datetime import datetime

from psycopg2.extras import DictRow


@dataclass(frozen=True)
class SignedUpDailyUsersDTO:
    day: datetime
    user_count: int

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "SignedUpDailyUsersDTO":
        return SignedUpDailyUsersDTO(
            day=row["day"],
            user_count=row["user_count"],
        )


@dataclass(frozen=True)
class EmailInfoDTO:
    email: str
    full_name: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "EmailInfoDTO":
        return EmailInfoDTO(
            email=row["personal_email"],
            full_name=row["full_name"],
        )


@dataclass(frozen=True)
class UserIdNameDTO:
    id: str
    full_name: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "UserIdNameDTO":
        return UserIdNameDTO(
            id=row["id"],
            full_name=row["full_name"],
        )


@dataclass(frozen=True)
class PhoneNumberWithIdDTO:
    id: str
    phone_number: str

    @classmethod
    def from_db_dict_row(cls, row: DictRow) -> "PhoneNumberWithIdDTO":
        return PhoneNumberWithIdDTO(
            id=row["id"],
            phone_number=row["phone_number"],
        )
