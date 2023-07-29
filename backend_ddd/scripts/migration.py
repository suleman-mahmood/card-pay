import firebase_admin
from firebase_admin import credentials, firestore
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime
from random import randint
from dataclasses import dataclass
from enum import Enum
from psycopg2.extensions import adapt, register_adapter, AsIs
from uuid import uuid5, NAMESPACE_OID, uuid4


load_dotenv()


def _generate_4_digit_otp() -> str:
    """Generate 4 digit OTP"""
    return str(randint(1000, 9999))


@dataclass
class Location:
    """Location value object"""

    latitude: float
    longitude: float


def adapt_point(point: Location):
    lat = adapt(point.latitude)
    lng = adapt(point.longitude)
    return AsIs("'(%s, %s)'" % (lat, lng))


def firebaseUidToUUID(uid: str) -> str:
    return str(uuid5(NAMESPACE_OID, uid))


class UserType(str, Enum):
    """User type enum"""

    CUSTOMER = 1  # Student, Faculty, Staff, etc.
    VENDOR = 2  # Shopkeeper, Society, Student Council etc.
    ADMIN = 3  # Admin of the closed loop system
    PAYMENT_GATEWAY = 4  # Payment gateway
    CARDPAY = 5  # Cardpay


class TransactionStatus(str, Enum):
    """Transaction status enum"""

    PENDING = 1
    FAILED = 2
    SUCCESSFUL = 3
    EXPIRED = 4
    DECLINED = 5


class TransactionMode(str, Enum):
    """Transaction mode enum"""

    QR = 1
    RFID = 2
    NFC = 3
    BARCODE = 4
    APP_TRANSFER = 5


class TransactionType(str, Enum):
    """Transaction type enum"""

    POS = 1
    # Ends at another customer's wallet
    P2P_PUSH = 2
    P2P_PULL = 3
    VOUCHER = 4
    # Direct payment to event registrations, donations, trips etc; Ends at a vendor
    VIRTUAL_POS = 5
    PAYMENT_GATEWAY = 6
    CARD_PAY = 7  # source of tokens in cardpay
    CASH_BACK = 8  # Marketing
    REFERRAL = 9  # Marketing


cred = credentials.Certificate("../api/credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# PostgreSQL configuration
connection = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    port=os.environ.get("DB_PORT"),
)
register_adapter(Location, adapt_point)

cursor = connection.cursor()

pg_id = str(uuid4())
sql = """
    insert into wallets (id, balance, created_at)
    values (%(id)s, %(balance)s, %(created_at)s)
    on conflict (id)
    do nothing;

    insert into users (id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at)
    values (%(id)s, %(personal_email)s, %(phone_number)s, %(user_type)s, %(pin)s, %(full_name)s, %(wallet_id)s, %(is_active)s, %(is_phone_number_verified)s, %(otp)s, %(otp_generated_at)s, %(location)s, %(created_at)s)
    on conflict (id)
    do nothing;
"""
cursor.execute(
    sql,
    {
        "balance": 1000000000,
        "id": pg_id,
        "personal_email": "paypro@payment.gateway",
        "phone_number": "03333333333",
        "user_type": UserType.PAYMENT_GATEWAY.name,
        "pin": _generate_4_digit_otp(),
        "full_name": "PayPro Payment Gateway",
        "wallet_id": pg_id,
        "is_active": True,
        "is_phone_number_verified": True,
        "otp": _generate_4_digit_otp(),
        "otp_generated_at": datetime.now(),
        "location": Location(latitude=0, longitude=0),
        "created_at": datetime(year=2023, month=1, day=1),
    },
)

"""
Migrating users and wallets
"""

docs = db.collection("users").stream()
count = 0

for doc in docs:
    doc_data = doc.to_dict()
    doc_id = doc.id

    user_type = UserType.CUSTOMER

    if doc_data["role"] == "vendor":
        user_type = UserType.VENDOR
    elif doc_data["role"] == "admin":
        user_type = UserType.CARDPAY
    elif doc_data["role"] == "student":
        user_type = UserType.CUSTOMER
    else:
        print("Woah a new type found!!!")

    sql = """
        insert into wallets (id, balance, created_at)
        values (%(id)s, %(balance)s, %(created_at)s)
        on conflict (id)
        do nothing;

        insert into users (id, personal_email, phone_number, user_type, pin, full_name, wallet_id, is_active, is_phone_number_verified, otp, otp_generated_at, location, created_at)
        values (%(id)s, %(personal_email)s, %(phone_number)s, %(user_type)s, %(pin)s, %(full_name)s, %(wallet_id)s, %(is_active)s, %(is_phone_number_verified)s, %(otp)s, %(otp_generated_at)s, %(location)s, %(created_at)s)
        on conflict (id)
        do nothing;
    """
    cursor.execute(
        sql,
        {
            "balance": doc_data["balance"],
            "id": firebaseUidToUUID(doc_data["id"]),
            "personal_email": doc_data["email"],
            "phone_number": doc_data["phoneNumber"],
            "user_type": user_type.name,
            "pin": doc_data["pin"],
            "full_name": doc_data["fullName"],
            "wallet_id": firebaseUidToUUID(doc_data["id"]),
            "is_active": True,
            "is_phone_number_verified": False,
            "otp": _generate_4_digit_otp(),
            "otp_generated_at": datetime.now(),
            "location": Location(latitude=0, longitude=0),
            "created_at": datetime(year=2023, month=1, day=1),
        },
    )
    if count % 10 == 0:
        print(count)
    count += 1

"""
Migrating users and wallets
"""

docs = db.collection("transactions").stream()
count = 0

for doc in docs:
    doc_data = doc.to_dict()
    doc_id = doc.id

    timestamp = doc_data["timestamp"]
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    sql = """
        insert into transactions (id, amount, mode, transaction_type, status, sender_wallet_id, recipient_wallet_id, created_at, last_updated)
        values (%(id)s, %(amount)s, %(mode)s, %(transaction_type)s, %(status)s, %(sender_wallet_id)s, %(recipient_wallet_id)s, %(created_at)s, %(last_updated)s);
    """
    try:
        cursor.execute(
            sql,
            {
                "id": firebaseUidToUUID(doc_data["id"]),
                "amount": doc_data["amount"],
                "mode": TransactionMode.APP_TRANSFER.name,
                "transaction_type": TransactionType.POS.name,
                "status": TransactionStatus.SUCCESSFUL.name,
                "sender_wallet_id": firebaseUidToUUID(doc_data["senderId"])
                if doc_data["senderId"] != "PayPro"
                else pg_id,
                "recipient_wallet_id": firebaseUidToUUID(doc_data["recipientId"])
                if doc_data["recipientId"] != "PayPro"
                else pg_id,
                "created_at": timestamp,
                "last_updated": timestamp,
            },
        )
    except Exception as e:
        print(e)
        print(doc_data["senderId"])
        print(doc_data["recipientId"])
        break

    if count % 10 == 0:
        print(count)
    count += 1

connection.commit()
cursor.close()
connection.close()
