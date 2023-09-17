import firebase_admin

from firebase_admin import auth


def create_user(
    phone_email: str,
    email_verified: bool,
    phone_number: str,
    password: str,
    full_name: str,
    disabled: bool,
) -> str:
    user_record = firebase_admin.auth.create_user(
        email=phone_email,
        email_verified=email_verified,
        phone_number=phone_number,
        password=password,
        display_name=full_name,
        disabled=disabled,
    )

    return user_record.uid


def update_password(firebase_uid: str, new_password: str, new_full_name: str):
    firebase_admin.auth.update_user(
        uid=firebase_uid,
        password=new_password,
        display_name=new_full_name,
    )


def get_user(email: str) -> str:
    user_record = auth.get_user_by_email(email=email)

    return user_record.uid
