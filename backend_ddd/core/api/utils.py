from uuid import uuid5, NAMESPACE_OID
from typing import List, Dict, Union
from functools import wraps
from firebase_admin import auth
from flask import request
from dataclasses import dataclass
import os


from core.entrypoint.uow import UnitOfWork
from core.authentication.entrypoint import queries as auth_qry
from core.authentication.domain.model import UserType
from core.api.event_codes import EventCode


@dataclass(frozen=True)
class Response:
    """Response object"""

    message: str
    status_code: int

    event_code: EventCode = EventCode.DEFAULT_EVENT
    data: Union[Dict, List] = None


@dataclass
class CustomException(Exception):
    message: str
    status_code: int = 400
    event_code: EventCode = EventCode.DEFAULT_EVENT


def firebaseUidToUUID(uid: str) -> str:
    return str(uuid5(NAMESPACE_OID, uid))


def authenticate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Fetch the token from the request headers
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise CustomException(
                message="Unauthorized, no header provided",
                status_code=401,
            )

        # Extract the token from the Authorization header
        token = auth_header.split("Bearer ")[1]

        try:
            uid = _get_uid_from_bearer(token)

            # Call the decorated function with the extracted information
            return f(uid=uid, *args, **kwargs)

        except auth.InvalidIdTokenError:
            # Token is invalid or expired
            raise CustomException(
                message="Unauthorized, invalid token",
                status_code=401,
            )

    return decorated_function


def authenticate_user_type(allowed_user_types: List[UserType]):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            uow = UnitOfWork()
            user_type = auth_qry.get_user_type_from_user_id(
                user_id=kwargs["uid"], uow=uow
            )
            uow.close_connection()

            if user_type not in allowed_user_types:
                raise CustomException(message="User not eligible")

            return func(*args, **kwargs)

        return wrapper

    return inner_decorator


def handle_missing_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.json is None:
            raise CustomException(message="payload missing in request")
        return func(*args, **kwargs)

    return wrapper


def validate_json_payload(required_parameters: List[str]):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            req = request.get_json(force=True)
            if "RETOOL_SECRET" in req.keys():
                req.pop("RETOOL_SECRET")
            if set(required_parameters) != set(req.keys()):
                raise CustomException(
                    "invalid json payload, missing or extra parameters"
                )
            return func(*args, **kwargs)

        return wrapper

    return inner_decorator


def authenticate_retool_secret(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        req = request.get_json(force=True)

        if "RETOOL_SECRET" not in req.keys():
            raise CustomException(
                message="retool secret missing in request",
            )

        if req["RETOOL_SECRET"] != os.environ.get("RETOOL_SECRET"):
            raise CustomException(message="invalid retool secret")

        return func(*args, **kwargs)

    return wrapper


def _get_uid_from_bearer(token: str) -> str:
    # Verify and decode the token
    decoded_token = auth.verify_id_token(token)

    # Extract the user ID and other information from the decoded token
    return firebaseUidToUUID(decoded_token["uid"])


def user_verified(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs["uid"]
        uow = UnitOfWork()
        phone_number_verified = auth_qry.user_verification_status_from_user_id(
            user_id=user_id, uow=uow
        )
        uow.close_connection()

        if not phone_number_verified:
            raise CustomException(message="User is not verified")

        return func(*args, **kwargs)

    return wrapper
