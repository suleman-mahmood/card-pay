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
