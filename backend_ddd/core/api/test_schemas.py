import pytest
from core.api import schemas as sch
from core.api import utils


def test_validate_payload():
    sample_data = {
        sch.EmailSchema: {
            "invalid_inputs": [
                "",
                "    ",
                "123123asd",
                "invalidemail@",
                "atthedatemissing.com",
                123123,
            ],
            "valid_inputs": [
                "shaheer@gmail.com",
                "another.valid@email.com.pk",
                "26100279@lums.edu.pk",
            ],
        },
        sch.PasswordSchema: {
            "invalid_inputs": ["", "    ", "short", 1238719],
            "valid_inputs": [
                "StrongP@ssw0rd",
                "AnotherStr0ng!Password",
                "no_digit",
                "!!@#%$^)(*$)%*#anypassword",
            ],
        },
        sch.PhoneNumberSchema: {
            "invalid_inputs": ["", "    ", "123456789", "invalid_format", 123],
            "valid_inputs": ["3123456784", "3333333333"],
        },
        sch.UserTypeSchema: {
            "invalid_inputs": ["", "    ", "invalid", "userType", "invalidtype", 2],
            "valid_inputs": ["CUSTOMER", "VENDOR", "ADMIN"],
        },
        sch.UserNameSchema: {
            "invalid_inputs": [
                "",
                "    ",
                "InvalidName1",
                "Special%Name",
                123,
                "FiRst NaMe",
                "Ab Kh",
                "Noone has a name this long lmao",
                "ajeeboghareebgiganticassfirstname lastname",
            ],
            "valid_inputs": [
                "John Doe",
                "Alice Smith",
                "Shaheer   Ahmad",
                "shaheer ahmad",
                " shaheer ahmad",
                "shaheer ahmad ",
                "Ali Khan",
                "Abdur Rehman Shamsi",
                "Three worded name",
                "Four Worded Name okay",
                "whothehell gives fivewordednames totheir children",
                "Muneeb Ur Rehman",
                "Shams ud din",
            ],
        },
        sch.LocationSchema: {
            "invalid_inputs": [
                "",
                "    ",
                [
                    1.2,
                ],
                [45.678, "Invalid"],
                "InvalidFormat",
                123,
                [],
                [1.23, 45.678, 90.123],
                {1.23, 9.42},
            ],
            "valid_inputs": [[1.23, 45.678], [0.0, 0.0]],
        },
        sch.PinSchema: {
            "invalid_inputs": ["", "    ", "12345", "Invalid", "0000", 1234],
            "valid_inputs": ["1234", "5678"],
        },
        sch.OtpSchema: {
            "invalid_inputs": ["", "    ", "12345", "Invalid", "0000", 1234],
            "valid_inputs": ["1234", "5678"],
        },
        sch.UuidSchema: {
            "invalid_inputs": ["", "    ", "invalid-uuid", "12345", "0000", 1234],
            "valid_inputs": [
                "d13eab16-4b8d-4e44-a9b6-2f47eb059153",
                "f34c798d-6257-40e5-981c-dde83cb8625f",
            ],
        },
        sch.AmountSchema: {
            "invalid_inputs": ["", "    ", 0, 100000000, 5.5, -100],
            "valid_inputs": [100, 5000, 9999],
        },
        sch.LUMSRollNumberSchema: {
            "invalid_inputs": [
                "",
                "    ",
                "1234567",
                "InvalidFormat",
                "LUMS12345",
                "lums12345",
            ],
            "valid_inputs": ["26100266", "2610M003", "2610m003", "10010023"],
        },
        sch.WeightageTypeSchema: {
            "invalid_inputs": [
                "",
                "    ",
                "Invalid",
                "weightageType",
                "invalidtype",
                2,
            ],
            "valid_inputs": [
                "POS",
                "P2P_PUSH",
                "P2P_PULL",
                "VOUCHER",
                "VIRTUAL_POS",
                "PAYMENT_GATEWAY",
                "CARD_PAY",
                "CASH_BACK",
                "REFERRAL",
                "RECONCILIATION",
            ],
        },
        sch.WeightageValueSchema: {
            "invalid_inputs": ["", "    ", -100, [123]],
            "valid_inputs": [0, 0.5, 1, 10, 50],
        },
        sch.AllCashbackSlabsSchema: {
            "invalid_inputs": [
                "",
                "     ",
                "[[1,PERCENTAGE,0.05]]",
                "[[1,2,5]]",
                "[]",
                123,
            ],
            "valid_inputs": [
                """[[1,2,"PERCENTAGE",0.05],[1,2,"ABSOLUTE",5]]""",
                """[  [0  ,  100,  "PERCENTAGE",   0.05], [150,123,"PERCENTAGE"  ,0.2]  ]""",
            ],
        },
        sch.DescriptionSchema: {
            "invalid_inputs": [123],
            "valid_inputs": ["This is a description", "Another description"],
        },
        sch.URLSchema: {
            "invalid_inputs": [123123, "", "     "],
            "valid_inputs": ["Anystring will work (except empty) for now"],
        },
        sch.ClosedLoopOrVendorNameSchema: {
            "invalid_inputs": ["", "    ", "Special%Name", 123],
            "valid_inputs": [
                "KFC",
                "LUMS",
                "LAHORE UNIVERSIRTY OF MANAGEMENT SCIENCES",
                "the bunker",
                "Lahore  University Of   Management Sciences",
                "IBA",
                "Microsoft",
            ],
        },
        sch.VerificationTypeSchema: {
            "invalid_inputs": [
                "",
                "    ",
                "Invalid",
                "verificationType",
                "invalidtype",
                2,
            ],
            "valid_inputs": ["NONE", "ROLLNUMBER", "EMAIL", "MEMBERSHIP_ID"],
        },
        sch.RegexSchema: {
            # empty strings are valid
            "invalid_inputs": ["[A-1]", "++", " [A-Z]\\", 2],
            "valid_inputs": [
                "",
                "^[A-Z]{1,15}[a-z]{0,15}(/s*[A-Z]{1}[a-z]{1,15}){0,4}$",
                "^[A-Z]{1,15}[a-z]{0,15}(/s*[A-Z]{1}[a-z]{1,15}){0,4}$",
            ],
        },
        sch.TimestampSchema: {
            "invalid_inputs": ["", "    ", "Invalid", "timestamp", "invalidtype", 2],
            "valid_inputs": [
                "2023-09-07 19:03:29.928044",
                "2023-09-07 19:03:29.912769",
            ],
        },
    }

    for schema, data in sample_data.items():
        for input in data["invalid_inputs"]:
            with pytest.raises(utils.CustomException):
                schema(input).validate()
        for input in data["valid_inputs"]:
            schema(input).validate()


@pytest.mark.parametrize(
    "input",
    [
        ("26100266"),
        ("2610M003"),
        ("2610m003"),
        ("10010023"),
        ("someone.last"),
        ("asdasdas"),
        ("small"),
        ("ls.lx"),
        ("boi_name"),
        ("a_sv"),
    ],
)
def test_valid_lums_rollnumber_or_faculty_schema(input):
    schema = sch.LUMSRollNumberOrFacultySchema
    schema(input).validate()


@pytest.mark.parametrize(
    "input",
    [
        (""),
        ("    "),
        ("1234567"),
        ("inv"),
        ("someoe.lastname2"),
        ("LUMS12345sad"),
        ("lums12345asda"),
        ("1slamus01"),
        ("1_a"),
        ("a_b"),
    ],
)
def test_invalid_lums_rollnumber_or_faculty_schema(input):
    schema = sch.LUMSRollNumberOrFacultySchema
    with pytest.raises(utils.CustomException):
        schema(input).validate()
