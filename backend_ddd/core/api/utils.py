from uuid import uuid5, NAMESPACE_OID
from typing import List, Dict, Union
from functools import wraps
from firebase_admin import auth
from flask import request
from dataclasses import dataclass


from core.entrypoint.uow import UnitOfWork
from core.authentication.entrypoint import queries as authentication_queries
from core.authentication.domain.model import UserType
from core.api.event_codes import EventCode

class Tabist(Exception):
    """
    User friendly exception.

    Attributes:
        message -- message to be viewed by user
    """

    def __init__(self, message: str, status_code: int = 400):
        self.message = message

        self.status_code = status_code
        super().__init__(message)

@dataclass(frozen = True)
class Response:
    """Response object"""

    message: str
    event_code: EventCode = EventCode.DEFAULT_EVENT

    status_code: int = 200
    data: Union[Dict,List] = None


def firebaseUidToUUID(uid: str) -> str:
    return str(uuid5(NAMESPACE_OID, uid))


def authenticate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Fetch the token from the request headers
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            print("No auth header provided")
            return Response(
                message="Unauthorized",
                status_code=401,
            )
            
        # Extract the token from the Authorization header
        token = auth_header.split("Bearer ")[1]

        try:
            # Verify and decode the token
            decoded_token = auth.verify_id_token(token)

            # Extract the user ID and other information from the decoded token
            uid = firebaseUidToUUID(decoded_token["uid"])

            # Call the decorated function with the extracted information
            return f(uid = uid, *args, **kwargs)

        except auth.InvalidIdTokenError:
            # Token is invalid or expired
            print("Threw an exception when decoding the auth token")
            return Response(
                message="Unauthorized",
                status_code=401,
            )
          
    return decorated_function

def authenticate_user_type(allowed_user_types: List[UserType]):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            uow = UnitOfWork()
            user_type = authentication_queries.get_user_type_from_user_id(
                user_id=kwargs["uid"], uow=uow
            )
            uow.close_connection()
            
            if user_type not in allowed_user_types:
                return Response(
                    message="User not eligible",
                    status_code=400,
                )

            return func(*args, **kwargs)

        return wrapper

    return inner_decorator


def handle_missing_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.json is None:
            return Response(
                message="payload missing in request",
                status_code=400,
            )
        return func(*args, **kwargs)

    return wrapper

def validate_json_payload(required_parameters : List[str]):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            req = request.get_json(force=True)
            if set(required_parameters) != set(req.keys()):
                return Response(
                    message="invalid json payload, missing or extra parameters",
                    status_code=400,
                )
            return func(*args, **kwargs)
        return wrapper
    return inner_decorator