from uuid import uuid5, NAMESPACE_OID
from functools import wraps
from firebase_admin import auth
from flask import request, jsonify
from typing import List

from core.entrypoint.uow import UnitOfWork
from core.authentication.entrypoint import queries as authentication_queries
from core.authentication.domain.model import UserType


def firebaseUidToUUID(uid: str) -> str:
    return str(uuid5(NAMESPACE_OID, uid))


def authenticate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Fetch the token from the request headers
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            print("No auth header provided")
            return "Unauthorized", 401

        # Extract the token from the Authorization header
        token = auth_header.split("Bearer ")[1]

        try:
            # Verify and decode the token
            decoded_token = auth.verify_id_token(token)

            # Extract the user ID and other information from the decoded token
            uid = firebaseUidToUUID(decoded_token["uid"])

            # kwargs["uid"] = uid

            # Call the decorated function with the extracted information
            return f(uid=uid, *args, **kwargs)

        except auth.InvalidIdTokenError:
            # Token is invalid or expired
            print("Threw an exception when decoding the auth token")
            return "Unauthorized", 401

    return decorated_function


def handle_exceptions_uow(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        uow = UnitOfWork()

        try:
            ret = func(uow, *args, **kwargs)
            uow.commit_close_connection()

            return ret
        except Exception as e:
            uow.close_connection()
            # TODO: add logging to include the full stack trace
            return jsonify({"success": False, "message": str(e)}), 400

    return wrapper


def authenticate_user_type(allowed_user_types: List[UserType]):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            uow = UnitOfWork()
            user_type = authentication_queries.get_user_type_from_user_id(
                user_id=kwargs["uid"], uow=uow
            )
            uow.close_connection()

            # kwargs.pop("uid")

            if user_type not in allowed_user_types:
                return (
                    jsonify({"success": False, "message": "User not eligible"}),
                    400,
                )
            return func(*args, **kwargs)

        return wrapper

    return inner_decorator


def handle_missing_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.json is None:
            return (
                jsonify({"success": False, "message": "payload missing in request"}),
                400,
            )

        return func(*args, **kwargs)

    return wrapper
