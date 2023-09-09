from abc import ABC, abstractmethod
from core.api import utils
from typing import List
from dataclasses import dataclass
from core.payment.domain.model import TX_UPPER_LIMIT
import re

class AbstractSchema(ABC):
    value: any

    @abstractmethod
    def validate(self):
        pass

@dataclass()
class EmailSchema(AbstractSchema): 
    value: str

    def validate(self):
        if not isinstance(self.value,str):
            raise utils.CustomException("Email passed is not a string")

        if not re.match(r"^[a-zA-Z0-9.a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$", self.value):
            raise utils.CustomException("Invalid Email Passed")

@dataclass()
class PasswordSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value, str):
            raise utils.CustomException("Password passed is not a string")
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+=-]{8,}$", self.value):
            raise utils.CustomException("Invalid Password Passed")


@dataclass()
class PhoneNumberSchema(AbstractSchema):
    value: str


    def validate(self):
        if not isinstance(self.value,str):
            raise utils.CustomException("Phone Number passed is not a string")

        if not re.match(r"^3[0-9]{9}$", self.value):
            raise utils.CustomException("Invalid Phone Number Passed")


@dataclass()
class UserTypeSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value,str):
            raise utils.CustomException("User Type passed is not a string")

        if not re.match(r"^(CUSTOMER|VENDOR|ADMIN|PAYMENT_GATEWAY|CARDPAY)$", self.value):
            raise utils.CustomException("Invalid User Type Passed")

@dataclass()
class NameSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value,str):
            raise utils.CustomException("Name passed is not a string")

        if not re.match(r"^\s*([A-Za-z]{1,}([\.,] |[-']| ))+[A-Za-z]+\.?\s*$", self.value):
            raise utils.CustomException("Invalid Name Passed")


@dataclass()
class LocationSchema(AbstractSchema):
    value: List[float]

    def validate(self):
        if not isinstance(self.value,list):
            raise utils.CustomException("Passed Location is not a tuple")

        if len(self.value) != 2:
            raise utils.CustomException("one or two location coordinates missing")

        if not isinstance(self.value[0],float) or not isinstance(self.value[1],float):
            raise utils.CustomException("Invalid Location Passed")


@dataclass()
class PinSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value,str):
            raise utils.CustomException("Pin passed is not a string")

        if not re.match(r"^[0-9]{4}$", self.value) or self.value == "0000" :
            raise utils.CustomException("Invalid Pin Passed")

@dataclass()
class OtpSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value,str):
            raise utils.CustomException("OTP passed is not a string")

        if not re.match(r"^[0-9]{4}$", self.value) or self.value == "0000" :
            raise utils.CustomException("Invalid Otp Passed")

@dataclass()
class UuidSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value,str):
            raise utils.CustomException("UUID passed is not a string")

        if not re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$", self.value) :
            raise utils.CustomException("Invalid Uuid Passed")

@dataclass()
class AmountSchema(AbstractSchema):
    value: int

    def validate(self):
        if not isinstance(self.value,int):
            raise utils.CustomException("Amount passed is not an integer")

        if self.value<=0:
            raise utils.CustomException("Amount is zero or negative")

        if self.value>=TX_UPPER_LIMIT:
            raise utils.CustomException(f"Amount is greater than or equal to {TX_UPPER_LIMIT}")

@dataclass()
class LUMSRollNumberSchema(AbstractSchema):
    value: str

    def validate(self):
        if not isinstance(self.value,str):
            raise utils.CustomException("Roll number passed is not a string")

        if not (re.match(r"^2[0-9]{7}$",self.value) or re.match(r"^2[0-9]{3}M[0-9]{3}",self.value) or re.match(r"^2[0-9]{3}m[0-9]{3}",self.value)):
            raise utils.CustomException("Invalid Roll Number Passed")
