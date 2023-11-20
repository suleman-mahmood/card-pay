import logging
from datetime import datetime, timedelta
from uuid import uuid4

from core.api import schemas as sch
from core.api import utils
from core.authentication.domain import model as auth_mdl
from core.authentication.entrypoint import queries as auth_qry
from core.entrypoint.uow import UnitOfWork
from core.event.adapters import exceptions as event_repo_exc
from core.event.domain import exceptions as event_mdl_exc
from core.event.domain import model as event_mdl
from core.event.entrypoint import anti_corruption as event_acl
from core.event.entrypoint import commands as event_cmd
from core.event.entrypoint import exceptions as event_svc_ex
from core.event.entrypoint import queries as event_qry
from core.event.entrypoint import services as event_svc
from core.payment.domain import model as pmt_mdl
from core.payment.entrypoint import anti_corruption as pmt_acl
from core.payment.entrypoint import commands as pmt_cmd
from core.payment.entrypoint import exceptions as pmt_svc_ex
from core.payment.entrypoint import queries as pmt_qry
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

vendor_app = Blueprint("vendor_app", __name__, url_prefix="/api/v1/vendor-app")

cors = CORS(
    vendor_app,
    resources={"/*": {"origins": "*"}},
)


@vendor_app.route("/get-vendor-transactions-to-be-reconciled", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(
    allowed_user_types=[
        auth_mdl.UserType.VENDOR,
        auth_mdl.UserType.EVENT_ORGANIZER,
    ]
)
@utils.user_verified
def get_vendor_transactions_to_be_reconciled(uid):
    uow = UnitOfWork()
    transactions = pmt_qry.payment_retools_get_transactions_to_be_reconciled(
        vendor_id=uid,
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="All transactions returned successfully",
        status_code=200,
        data=transactions,
    ).__dict__


@vendor_app.route("/get-vendor-balance", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(
    allowed_user_types=[
        auth_mdl.UserType.VENDOR,
        auth_mdl.UserType.EVENT_ORGANIZER,
    ]
)
@utils.user_verified
def get_vendor_balance(uid):
    uow = UnitOfWork()
    balance = auth_qry.get_user_balance(
        user_id=uid,
        uow=uow,
    )
    uow.close_connection()

    return utils.Response(
        message="Vendor balance returned successfully",
        status_code=200,
        data={
            "balance": balance,
        },
    ).__dict__


@vendor_app.route("/get-vendor", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(
    allowed_user_types=[
        auth_mdl.UserType.VENDOR,
        auth_mdl.UserType.EVENT_ORGANIZER,
    ]
)
@utils.user_verified
def get_vendor(uid):
    uow = UnitOfWork()
    user = auth_qry.get_user_from_user_id(user_id=uid, uow=uow)
    uow.close_connection()

    return utils.Response(
        message="User returned successfully",
        status_code=200,
        data=user.__dict__,
    ).__dict__


@vendor_app.route("/get-vendor-previous-reconciliation-txn-id", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(
    allowed_user_types=[
        auth_mdl.UserType.VENDOR,
        auth_mdl.UserType.EVENT_ORGANIZER,
    ]
)
@utils.user_verified
def get_vendor_previous_reconciliation_txn_id(uid):
    uow = UnitOfWork()
    try:
        previous_reconciliation_txn_id = pmt_qry.get_vendor_previous_reconciliation_txn_id(
            vendor_id=uid,
            reconciled_txn_id=request.args.get("reconciled_txn_id"),
            uow=uow,
        )
    except pmt_svc_ex.NoPreviousReconciliationFound as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    uow.close_connection()

    return utils.Response(
        message="previous reconciliation txn id returned successfully",
        status_code=200,
        data={
            "previous_reconciliation_txn_id": previous_reconciliation_txn_id,
        },
    ).__dict__


@vendor_app.route("/get-vendor-next-reconciliation-txn-id", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(
    allowed_user_types=[
        auth_mdl.UserType.VENDOR,
        auth_mdl.UserType.EVENT_ORGANIZER,
    ]
)
@utils.user_verified
def get_vendor_next_reconciliation_txn_id(uid):
    uow = UnitOfWork()

    try:
        next_reconciliation_txn_id = pmt_qry.get_vendor_next_reconciliation_txn_id(
            vendor_id=uid,
            reconciled_txn_id=request.args.get("reconciled_txn_id"),
            uow=uow,
        )
    except pmt_svc_ex.NoNextReconciliationFound as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    uow.close_connection()

    return utils.Response(
        message="next reconciliation txn id returned successfully",
        status_code=200,
        data={
            "next_reconciliation_txn_id": next_reconciliation_txn_id,
        },
    ).__dict__


@vendor_app.route("/get-vendor-latest-reconciliation-txn-id", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(
    allowed_user_types=[
        auth_mdl.UserType.VENDOR,
        auth_mdl.UserType.EVENT_ORGANIZER,
    ]
)
@utils.user_verified
def get_vendor_latest_reconciliation_txn_id(uid):
    uow = UnitOfWork()
    try:
        latest_reconciliation_txn_id = pmt_qry.get_vendor_latest_reconciliation_txn_id(
            vendor_id=uid,
            uow=uow,
        )
    except pmt_svc_ex.NoLatestReconciliationFound as e:
        uow.close_connection()
        raise (utils.CustomException(str(e)))

    uow.close_connection()
    return utils.Response(
        message="Latest reconciliation txn id returned successfully",
        status_code=200,
        data={
            "latest_reconciliation_txn_id": latest_reconciliation_txn_id,
        },
    ).__dict__


@vendor_app.route("/get-vendor-reconciled-transactions", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(
    allowed_user_types=[
        auth_mdl.UserType.VENDOR,
        auth_mdl.UserType.EVENT_ORGANIZER,
    ]
)
@utils.user_verified
def get_vendor_reconciled_transactions(uid):
    uow = UnitOfWork()
    transactions = pmt_qry.payment_retools_get_reconciled_transactions(
        vendor_id=uid,
        reconciliation_txn_id=request.args.get("reconciled_txn_id"),
        uow=uow,
    )

    uow.close_connection()

    return utils.Response(
        message="Reconciled Transactions returned successfully",
        status_code=200,
        data=transactions,
    ).__dict__


""" 
    --- --- --- --- --- --- --- --- --- --- --- ---
    Events
    --- --- --- --- --- --- --- --- --- --- --- ---
"""


@vendor_app.route("/get-live-events", methods=["GET"])
def get_live_events():
    closed_loop_id = request.args.get("closed_loop_id")
    uow = UnitOfWork()

    try:
        events = event_qry.get_live_events(
            closed_loop_id=closed_loop_id,
            uow=uow,
            event_type=event_mdl.EventType.EXTERNAL,
        )
        uow.close_connection()

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="All live events returned successfully", status_code=200, data=events
    ).__dict__


@vendor_app.route("/register-event", methods=["POST"])
@utils.validate_and_sanitize_json_payload(
    required_parameters={
        "event_id": sch.UuidSchema,
        "event_form_data": sch.EventFormDataSchema,
        "full_name": sch.StringSchema,
        "phone_number": sch.StringSchema,  # +923333462677
        "email": sch.EmailSchema,
    }
)
def register_event():
    req = request.get_json(force=True)
    qr_id = str(uuid4())
    uow = UnitOfWork()

    try:
        form_data = event_mdl.Registration.from_json_to_form_data(req["event_form_data"])
        event_id = req["event_id"]

        event = uow.events.get(event_id=event_id)
        ticket_price = event_svc.calculate_ticket_price(
            event_id=event_id, form_data=form_data, uow=uow
        )

        paid_registrations_count = event_svc.get_paid_registrations_count(
            event_id=req["event_id"], uow=uow
        )

        checkout_url, paypro_id = pmt_cmd.create_any_deposit_request(
            tx_id=str(uuid4()),
            user_id=event.organizer_id,
            amount=ticket_price,
            full_name=req["full_name"],
            phone_number=req["phone_number"],
            email=req["email"],
            uow=uow,
            auth_svc=pmt_acl.AuthenticationService(),
            pp_svc=pmt_acl.PayproService(),
        )
        event_cmd.register_user_open_loop(
            event_id=event_id,
            qr_id=qr_id,
            current_time=datetime.now() + timedelta(hours=5),
            event_form_data=form_data,
            paypro_id=paypro_id,
            paid_registrations_count=int(paid_registrations_count),
            uow=uow,
        )
        uow.commit_close_connection()

    except (
        event_mdl_exc.EventNotApproved,
        event_mdl_exc.RegistrationEnded,
        event_mdl_exc.UserInvalidClosedLoop,
        event_mdl_exc.EventCapacityExceeded,
        event_mdl_exc.RegistrationAlreadyExists,
        pmt_svc_ex.PaymentUrlNotFoundException,
        pmt_svc_ex.PayProsCreateOrderTimedOut,
        pmt_svc_ex.PayProsGetAuthTokenTimedOut,
    ) as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(
        message="User successfully registered for the event",
        status_code=200,
        data={"checkout_url": checkout_url},
    ).__dict__


@vendor_app.route("/mark-entry-event-attendance", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.EVENT_ORGANIZER])
@utils.user_verified
@utils.validate_and_sanitize_json_payload(required_parameters={"qr_id": sch.UuidSchema})
def mark_entry_event_attendance(uid):
    req = request.get_json(force=True)
    uow = UnitOfWork()

    try:
        event_cmd.mark_attendance(
            qr_id=req["qr_id"],
            current_time=datetime.now() + timedelta(hours=5),
            uow=uow,
            event_service_acl=event_acl.EventsService(),
        )
        attendance_data = event_qry.get_attendance_data(qr_id=req["qr_id"], uow=uow)
        uow.commit_close_connection()

    except (
        event_repo_exc.EventNotFound,
        event_mdl_exc.EventNotApproved,
        event_mdl_exc.AttendancePostEventException,
        event_mdl_exc.EventRegistrationNotStarted,
        event_mdl_exc.RegistrationDoesNotExist,
        event_svc_ex.InvalidAttendanceQrId,
        event_svc_ex.EventNotFound,
    ) as e:
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "mark-entry-event-attendance",
                "invoked_by": "vendor_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise utils.CustomException(str(e))

    except event_mdl_exc.UserIsAlreadyMarkedPresent as e:
        attendance_data = event_qry.get_attendance_data(qr_id=req["qr_id"], uow=uow)
        uow.close_connection()
        logging.info(
            {
                "message": "Custom exception raised",
                "endpoint": "mark-entry-event-attendance",
                "invoked_by": "vendor_app",
                "exception_type": e.__class__.__name__,
                "exception_message": str(e),
                "json_request": req,
                "attendance_data": attendance_data.__dict__,
            },
        )
        return utils.Response(
            message="Event attendance already marked",
            status_code=200,
            data={"attendance_data": attendance_data, "already_marked": True},
        ).__dict__

    except Exception as e:
        uow.close_connection()
        logging.info(
            {
                "message": f"Unhandled exception raised",
                "endpoint": "mark-entry-event-attendance",
                "invoked_by": "vendor_app",
                "exception_type": 500,
                "exception_message": str(e),
                "json_request": req,
            },
        )
        raise e

    return utils.Response(
        message="Event attendance marked successfully",
        status_code=200,
        data={"attendance_data": attendance_data, "already_marked": False},
    ).__dict__


@vendor_app.route("/mark-exit-event-attendance", methods=["POST"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.EVENT_ORGANIZER])
@utils.user_verified
@utils.validate_and_sanitize_json_payload(
    required_parameters={"event_id": sch.UuidSchema, "qr_id": sch.UuidSchema}
)
def mark_exit_event_attendance(uid):
    raise utils.CustomException("Not implemented")
    uow = UnitOfWork()

    try:
        uow.close_connection()

    except () as e:
        uow.close_connection()
        raise utils.CustomException(str(e))

    except Exception as e:
        uow.close_connection()
        raise e

    return utils.Response(message="", status_code=200, data={}).__dict__


@vendor_app.route("/get-society-registrations", methods=["GET"])
@cross_origin(origin="*", headers=["Authorization"])
@utils.authenticate_token
@utils.authenticate_user_type(allowed_user_types=[auth_mdl.UserType.EVENT_ORGANIZER])
@utils.user_verified
def get_society_registrations(uid):
    uow = UnitOfWork()
    transactions = pmt_qry.payment_retools_get_transactions_to_be_reconciled(
        vendor_id=uid,
        uow=uow,
    )
    external_registrations = event_qry.get_registrations(
        paypro_ids=[tx.paypro_id for tx in transactions],
        uow=uow,
    )
    internal_registrations = event_qry.get_internal_registrations(organizer_id=uid, uow=uow)
    unpaid_registrations = event_qry.get_unpaid_registrations(organizer_id=uid, uow=uow)
    uow.close_connection()

    return utils.Response(
        message="All transactions returned successfully",
        status_code=200,
        data={
            "external_registrations": external_registrations,
            "internal_registrations": internal_registrations,
            "unpaid_registrations": unpaid_registrations,
        },
    ).__dict__
