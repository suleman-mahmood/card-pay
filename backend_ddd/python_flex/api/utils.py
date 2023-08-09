from uuid import uuid5, NAMESPACE_OID
from functools import wraps
from firebase_admin import auth
from flask import request, jsonify

from python_flex.entrypoint.uow import UnitOfWork

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

            # Call the decorated function with the extracted information
            return f(uid, *args, **kwargs)

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
            return jsonify({"success": False, "message": str(e)}), 400

    return wrapper


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
