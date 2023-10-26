import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from core.api import utils
from core.payment.domain.model import TX_UPPER_LIMIT


class AbstractSchema(ABC):
    value: any

    @abstractmethod
    def validate(self):
        pass


@dataclass()
class EmailSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Email passed is not a string")

        if not re.match(
            r"^[a-zA-Z0-9.a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", self.value
        ):
            raise utils.CustomException("Invalid Email Passed")


@dataclass()
class PasswordSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Password passed is not a string")

        if len(self.value) < 8:
            raise utils.CustomException("Password is less than 8 characters")

        if re.match(r"^( )*$", self.value):
            raise utils.CustomException("Password passed is empty")


@dataclass()
class PhoneNumberSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Phone Number passed is not a string")

        if not re.match(r"^3[0-9]{9}$", self.value):
            raise utils.CustomException("Invalid Phone Number Passed")


@dataclass()
class UserTypeSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("User Type passed is not a string")

        if not re.match(
            r"^(CUSTOMER|VENDOR|ADMIN|PAYMENT_GATEWAY|CARDPAY)$", self.value
        ):
            raise utils.CustomException("Invalid User Type Passed")


@dataclass()
class UserNameSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Name passed is not a string")

        if any(char.isdigit() for char in self.value):
            raise utils.CustomException("Name cannot contain digits")

        if re.match(r"^( )*$", self.value):
            raise utils.CustomException("Name passed is empty")

        if len(self.value) > 50:
            raise utils.CustomException("Name passed is too long")

        if len(self.value.split(" ")) < 2:
            raise utils.CustomException("Last Name is missing")


@dataclass()
class LocationSchema(AbstractSchema):
    value: List[float]

    def validate(self):
        if not isinstance(self.value, list):
            raise utils.CustomException("Passed Location is not a tuple")

        if len(self.value) != 2:
            raise utils.CustomException("one or two location coordinates missing")

        if not isinstance(self.value[0], float) or not isinstance(self.value[1], float):
            raise utils.CustomException("Invalid Location Passed")


@dataclass()
class PinSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Pin passed is not a string")

        if self.value == "0000":
            raise utils.CustomException("Pin cannot be 0000, please use another pin.")

        if len(self.value) < 4:
            raise utils.CustomException("Pin cannot be less than 4 digits")

        if not re.match(r"^[0-9]{4}$", self.value):
            raise utils.CustomException("Pin can only contain digits")


@dataclass()
class OtpSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("OTP passed is not a string")

        if self.value == "0000":
            raise utils.CustomException("OTP cannot be 0000, please pass a valid OTP.")

        if len(self.value) < 4:
            raise utils.CustomException("OTP cannot be less than 4 digits")

        if not re.match(r"^[0-9]{4}$", self.value):
            raise utils.CustomException("OTP can only contain digits")


@dataclass()
class UuidSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("UUID passed is not a string")

        if not re.match(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$",
            self.value,
        ):
            raise utils.CustomException("Invalid Uuid Passed")


@dataclass()
class AmountSchema(AbstractSchema):
    value: int

    def validate(self):
        if not isinstance(self.value, int):
            raise utils.CustomException("Amount passed is not an integer")

        if self.value <= 0:
            raise utils.CustomException("Amount is zero or negative")

        if self.value >= TX_UPPER_LIMIT:
            raise utils.CustomException(
                f"Amount is greater than or equal to {TX_UPPER_LIMIT}"
            )


@dataclass()
class LUMSRollNumberSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Roll number passed is not a string")

        if not re.match(r"^[2|1][0-9]{3}[M|m|0-9][0-9]{3}", self.value):
            raise utils.CustomException("Invalid Roll Number Passed")


@dataclass()
class LUMSRollNumberOrFacultySchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Roll number passed is not a string")

        if not re.match(
            r"^[2|1][0-9]{3}[M|m|0-9][0-9]{3}|[A-Za-z\.\_]{4,}$", self.value
        ):
            raise utils.CustomException("Invalid Roll Number Passed")


@dataclass()
class LUMSReferralRollNumberSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Referral roll number passed is not a string")

        # Referral can be an empty string when no one is referred
        if self.value == "":
            return

        if not (
            re.match(r"^2[0-9]{7}$", self.value)
            or re.match(r"^2[0-9]{3}M[0-9]{3}", self.value)
            or re.match(r"^2[0-9]{3}m[0-9]{3}", self.value)
        ):
            raise utils.CustomException("Invalid Roll Number Passed")


@dataclass()
class WeightageTypeSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Weightage Type passed is not a string")

        # TODO: Change this once the weightage type is restricted to a subset of Transaction Types
        if not re.match(
            r"^(POS|P2P_PUSH|P2P_PULL|VOUCHER|VIRTUAL_POS|PAYMENT_GATEWAY|CARD_PAY|CASH_BACK|REFERRAL|RECONCILIATION)$",
            self.value,
        ):
            raise utils.CustomException("Invalid Weightage Type Passed")


@dataclass()
class WeightageValueSchema(AbstractSchema):
    value: float or int  # float incase of percentage weightage type, int incase of absolute

    def validate(self):
        if not isinstance(self.value, (float, int)):
            raise utils.CustomException(
                "Weightage Value passed is not a float or integer"
            )

        if self.value < 0:
            raise utils.CustomException(
                "Negative weightage value passed, weightage value cannot be negative"
            )


@dataclass()
class AllCashbackSlabsSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Cashback Slabs passed is not a string")

        if not re.match(
            r"""^\[\s*(\[\s*(\d+)\s*,\s*(\d+)\s*,\s*("PERCENTAGE"|"ABSOLUTE")\s*,\s*(\d+(\.\d+)?|\d+)\s*\])(\s*,\s*(\[\s*(\d+)\s*,\s*(\d+)\s*,\s*("PERCENTAGE"|"ABSOLUTE")\s*,\s*(\d+(\.\d+)?|\d+)\s*\]))*\s*\]$""",
            self.value,
        ):
            raise utils.CustomException("Invalid Cashback Slabs Passed")


@dataclass()
class DescriptionSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Description passed is not a string")


@dataclass()
class URLSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Url passed is not a string")

        if re.match(r"^( )*$", self.value):
            raise utils.CustomException("Url passed is empty")
        # TODO: Implement Later


@dataclass()
class ClosedLoopOrVendorNameSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Name passed is not a string")

        if not re.match(r"^[A-Za-z]{1,15}(\s*[A-Za-z]{1,15}){0,4}$", self.value):
            raise utils.CustomException("Invalid Name Passed")


@dataclass()
class VerificationTypeSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Verification Type passed is not a string")

        if not re.match(r"^(NONE|ROLLNUMBER|EMAIL|MEMBERSHIP_ID)$", self.value):
            raise utils.CustomException("Invalid Verification Type Passed")


@dataclass()
class RegexSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Regex passed is not a string")

        try:
            re.compile(self.value)
        except re.error:
            raise utils.CustomException("Invalid Regex Passed")


@dataclass()
class FloatSchema(AbstractSchema):
    value: float

    def validate(self):
        if not isinstance(self.value, float):
            raise utils.CustomException("Value passed is not a float")


@dataclass()
class TimestampSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Timestamp passed is not a string")

        if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$", self.value):
            raise utils.CustomException("Invalid Timestamp Passed")


@dataclass()
class VersionSchema(AbstractSchema):
    value: int

    def validate(self):
        if not isinstance(self.value, int):
            raise utils.CustomException("Version passed is not an integer")

        if self.value < 0:
            raise utils.CustomException("Version passed is negative")


@dataclass()
class FcmTokenSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Fcm Token passed is not a string")

        if len(self.value) <= 0:
            raise utils.CustomException("Fcm Token passed is empty")


@dataclass()
class EventNameSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Name passed is not a string")

        if re.match(r"^( )*$", self.value):
            raise utils.CustomException("Name passed is empty")

        if len(self.value) > 50:
            raise utils.CustomException("Name passed is too long")


@dataclass()
class EventCapacitySchema(AbstractSchema):
    value: int

    def validate(self):
        if not isinstance(self.value, int):
            raise utils.CustomException("Event passed is not an integer")

        if self.value <= 0:
            raise utils.CustomException("Event is zero or negative")


@dataclass()
class EventTimestampSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Timestamp passed is not a string")

        # TODO: Fix this later


@dataclass()
class EventFormSchema(AbstractSchema):
    value: dict

    def validate(self):
        if not isinstance(self.value, dict):
            raise utils.CustomException("EventFormSchema is not an object/dictionary")

        if not isinstance(self.value["fields"], list):
            raise utils.CustomException("EventFormSchema is not an object/dictionary")


@dataclass()
class EventFormDataSchema(AbstractSchema):
    value: dict

    def validate(self):
        try:
            [["question", "answer"] for x in self.value["fields"]]
        except KeyError:
            raise utils.CustomException(
                "EventFormDataSchema is not an object/dictionary"
            )

        if any(
            [
                not isinstance(v["question"], str)
                or not isinstance(v["answer"], (str, int, bool, float))
                for v in self.value["fields"]
            ]
        ):
            raise utils.CustomException(
                "EventFormDataSchema is not an object/dictionary"
            )

        if not isinstance(self.value, dict):
            raise utils.CustomException(
                "EventFormDataSchema is not an object/dictionary"
            )


@dataclass()
class StringSchema(AbstractSchema):
    value: dict

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("StringSchema is not a string")
