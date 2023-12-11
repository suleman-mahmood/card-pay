import logging
import os
from abc import ABCMeta
from copy import deepcopy
from dataclasses import dataclass
from functools import wraps
from typing import Dict, List, Optional, Union
from uuid import NAMESPACE_OID, uuid5

from core.api import schemas as sch
from core.api.event_codes import EventCode
from core.authentication.domain.model import UserType
from core.authentication.entrypoint import exceptions as auth_svc_ex
from core.authentication.entrypoint import queries as auth_qry
from core.entrypoint.uow import UnitOfWork
from firebase_admin import auth
from flask import request


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

        if auth_header is None:
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "NoAuthHeader",
                },
            )
            raise CustomException(
                message="No authorization header provided",
                status_code=401,
            )

        bearer, _, token = auth_header.partition(" ")

        if bearer != "Bearer" or token == "":
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "Invalidheader",
                },
            )
            raise CustomException(
                message="Unauthorized, invalid header",
                status_code=401,
            )

        try:
            uid = _get_uid_from_bearer(token)

            # Call the decorated function with the extracted information
            return f(uid=uid, *args, **kwargs)

        except auth.InvalidIdTokenError:
            # Token is invalid or expired
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "InvalidToken",
                },
            )
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
            try:
                user_type = auth_qry.get_user_type_from_user_id(user_id=kwargs["uid"], uow=uow)
                uow.close_connection()
            except auth_svc_ex.UserNotFoundException as e:
                uow.close_connection()
                logging.info(
                    {
                        "message": "Custom exception raised",
                        "endpoint": "api-decorator",
                        "exception_type": "UserNotExists",
                    },
                )
                raise CustomException(str(e))
            except Exception:
                uow.close_connection()
                logging.info(
                    {
                        "message": "Unhandled exception raised",
                        "endpoint": "api-decorator",
                    },
                )
                raise CustomException(str(e))

            if user_type not in allowed_user_types:
                logging.info(
                    {
                        "message": "Custom exception raised",
                        "endpoint": "api-decorator",
                        "exception_type": "UserNotEligible",
                    },
                )
                raise CustomException(message="User not eligible")

            return func(*args, **kwargs)

        return wrapper

    return inner_decorator


def handle_missing_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.json is None:
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "PayloadMissingInRequest",
                },
            )
            raise CustomException(message="payload missing in request")
        return func(*args, **kwargs)

    return wrapper


def validate_and_sanitize_json_payload(
    required_parameters: Dict[str, ABCMeta],
    optional_parameters: Optional[Dict[str, ABCMeta]] = None,
):
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            req = request.get_json(force=True)

            if "RETOOL_SECRET" in req.keys():
                req.pop("RETOOL_SECRET")

            if "RP_SECRET" in req.keys():
                req.pop("RP_SECRET")

            # Remove all optional parameters from the request
            if optional_parameters is not None:
                for k, _ in optional_parameters.items():
                    req.pop(k, None)

            if set(required_parameters) != set(req.keys()):
                logging.info(
                    {
                        "message": "Custom exception raised",
                        "endpoint": "api-decorator",
                        "exception_type": "InvalidJsonPayload",
                        # "json_request": req,
                        # "optional_parameters": optional_parameters,
                        # "required_parameters": required_parameters,
                    },
                )
                raise CustomException("invalid json payload, missing or extra parameters")

            for param, schema in required_parameters.items():
                # Assuming that all input strings should not contain leading or trailing whitespaces
                if isinstance(req[param], str):
                    req[param] = req[param].strip()

                try:
                    schema(req[param]).validate()
                except CustomException as e:
                    logging.info(
                        {
                            "message": "Custom exception raised",
                            "endpoint": "api-decorator",
                            "exception_type": "InvalidSchema",
                            # "param_type": param,
                            # "param_value": req[param],
                            # "schema_type": schema.__class__.__name__,
                            # "json_request": req,
                            # "optional_parameters": optional_parameters,
                            # "required_parameters": required_parameters,
                        },
                    )
                    raise e

            return func(*args, **kwargs)

        return wrapper

    return inner_decorator


def authenticate_retool_secret(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        req = request.get_json(force=True)

        if "RETOOL_SECRET" not in req.keys():
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "NoRetoolSecret",
                },
            )
            raise CustomException(
                message="retool secret missing in request",
            )

        if req["RETOOL_SECRET"] != os.environ.get("RETOOL_SECRET"):
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "InvalidRetoolSecret",
                },
            )
            raise CustomException(message="invalid retool secret")

        return func(*args, **kwargs)

    return wrapper


def authenticate_rp_secret(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        req = request.get_json(force=True)

        if "RP_SECRET" not in req.keys():
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "NoRPSecret",
                },
            )
            raise CustomException(
                message="retail pro secret missing in request",
            )

        if req["RP_SECRET"] != os.environ.get("RP_SECRET"):
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "InvalidRPSecret",
                },
            )
            raise CustomException(message="invalid retail pro secret")

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
            logging.info(
                {
                    "message": "Custom exception raised",
                    "endpoint": "api-decorator",
                    "exception_type": "UserNotVerified",
                },
            )
            raise CustomException(message="User is not verified")

        return func(*args, **kwargs)

    return wrapper
