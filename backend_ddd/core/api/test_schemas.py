from core.api import schemas as sch
from core.api import utils
import pytest

def test_validate_payload():

    sample_data = {
        sch.EmailSchema: {
            "invalid_inputs": ["","    ", "123123asd", "invalidemail@", "atthedatemissing.com",123123],
            "valid_inputs": ["shaheer@gmail.com", "another.valid@email.com.pk", "26100279@lums.edu.pk"],
        },
        sch.PasswordSchema: {
            "invalid_inputs": ["","    ", "short", "no_digit",1238719],
            "valid_inputs": ["StrongP@ssw0rd", "AnotherStr0ng!Password"],
        },
        sch.PhoneNumberSchema: {
            "invalid_inputs": ["","    ", "123456789", "invalid_format",123],
            "valid_inputs": ["3123456784", "3333333333"],
        },
        sch.UserTypeSchema: {
            "invalid_inputs": ["","    ", "invalid", "userType", "invalidtype", 2],
            "valid_inputs": ["CUSTOMER", "VENDOR", "ADMIN"],
        },
        sch.NameSchema: {
            "invalid_inputs": ["","    ", "InvalidName1", "Special%Name",123],
            "valid_inputs": ["John Doe", "Alice Smith"],
        },
        sch.LocationSchema: {
            "invalid_inputs": ["","    ", [1.2,], [45.678,"Invalid"], "InvalidFormat", 123, [], [1.23,45.678,90.123], {1.23,9.42}],
            "valid_inputs": [[1.23,45.678], [0.0,0.0]],
        },
        sch.PinSchema: {
            "invalid_inputs": ["","    ", "12345", "Invalid", "0000",1234],
            "valid_inputs": ["1234", "5678"],
        },
        sch.OtpSchema: {
            "invalid_inputs": ["","    ", "12345", "Invalid", "0000",1234],
            "valid_inputs": ["1234", "5678"],
        },
        sch.UuidSchema: {
            "invalid_inputs": ["","    ", "invalid-uuid", "12345", "0000",1234],
            "valid_inputs": ["d13eab16-4b8d-4e44-a9b6-2f47eb059153", "f34c798d-6257-40e5-981c-dde83cb8625f"],
        },
        sch.AmountSchema: {
            "invalid_inputs": ["","    ", 0, 100000000, 5.5, -100],
            "valid_inputs": [100, 5000, 9999],
        },
        sch.LUMSRollNumberSchema: {
            "invalid_inputs": ["","    ", "1234567", "InvalidFormat", "LUMS12345", "lums12345"],
            "valid_inputs": ["26100266", "2610M003", "2610m003"],
        },
    }

    for schema, data in sample_data.items():
        for input in data["invalid_inputs"]:
            with pytest.raises(utils.CustomException):
                schema(input).validate()
        for input in data["valid_inputs"]:
            assert schema(input).validate()