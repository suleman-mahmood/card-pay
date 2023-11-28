import math
from io import BytesIO
from typing import Dict, List

import qrcode
from core.comms.entrypoint import commands as comms_cmd
from core.entrypoint.uow import AbstractUnitOfWork
from core.event.domain import model as event_mdl
from core.event.entrypoint import exceptions as event_exc
from core.event.entrypoint import queries as event_qry

DRAMALINE_EVENT_ID = "4399b8ea-0ee8-4b69-8187-861baf61c858"
LAPS_EVENT_ID = "80ce325b-4081-4e7c-86aa-039e117ef4c8"
FURTHER_PARTICIPANTS_COUNT_QUESTION = "Number of team members (excluding the one registering)"
MAX_LIMIT_VOUCHER = 20
VOUCHER_QUESTION = "Promo code"


def send_registration_email(tx_id: str, uow: AbstractUnitOfWork):
    attendance_details = event_qry.get_attendance_details(tx_id=tx_id, uow=uow)
    event = uow.events.get(event_id=attendance_details.event_id)

    data = {"qr_id": attendance_details.qr_id, "event_id": attendance_details.event_id}
    data_str = str(data)

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )

    qr.add_data(data_str)
    qr.make(fit=True)

    buffer = BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(buffer)
    qr_code_bytes = buffer.getvalue()
    buffer.close()

    html = f"""
        <html>
            <head>
                <title>{event.name} Confirmation Email</title>
            </head>
            <body>
                <h1>Hi {attendance_details.full_name}!</h1>

                <p>We're excited to confirm your registration for {event.name}</p>

                <p>Please show this QR code at the venue to mark your attendance:</p>
                <img src="cid:qr_code_image">

                <h2>Event Details</h2>

                <ul>
                    <li>Date: {event.event_start_timestamp.strftime('%d%S %B, %Y')}</li>
                    <li>Time: {event.event_start_timestamp.strftime('%I:%M %p')}</li>
                    <li>Location: {event.venue}</li>
                </ul>

                <p>Please review the event details carefully and make any necessary arrangements.</p>

                <p>We look forward to seeing you at the event!</p>

                <p>Sincerely,</p>
                <p>CardPay Team</p>
            </body>
        </html>
    """

    comms_cmd.send_image_email(
        subject=f"Registration successful for {event.name}",
        html=html,
        to=attendance_details.email,
        image_bytes=qr_code_bytes,
    )


def calculate_ticket_price(
    event_id: str,
    form_data: Dict[str, List[event_mdl.EventFormDataItem]],
    uow: AbstractUnitOfWork,
) -> int:
    event = uow.events.get(event_id=event_id)

    if event_id != LAPS_EVENT_ID:
        return event.registration_fee

    try:
        participants = int(
            next(
                item
                for item in form_data["fields"]
                if item.question == FURTHER_PARTICIPANTS_COUNT_QUESTION
            ).answer
        )
    except StopIteration:
        participants = 1

    try:
        voucher = str(
            next(item for item in form_data["fields"] if item.question == VOUCHER_QUESTION).answer
        )
    except StopIteration:
        voucher = ""

    if voucher == "":
        return math.ceil(
            (participants + 1) * event.registration_fee * (1.25) + event.registration_fee
        )

    redeemed = event_qry.get_redeemed_count_from_vouchers(voucher_code=voucher, uow=uow)

    if redeemed == MAX_LIMIT_VOUCHER:
        raise event_exc.VoucherLimitExceeded("Voucher limit has exceeded")

    total_price = (participants + 1) * event.registration_fee * (1.25)

    if voucher == "XBAF":
        total_price = 0.5 * total_price + event.registration_fee
    elif voucher == "DD5N":
        total_price = event.registration_fee
    elif voucher == "QYNE":
        total_price = 0.5 * (
            (participants + 1) * event.registration_fee * (1.25) + event.registration_fee
        )
    else:
        raise event_exc.VoucherNotFound("Voucher not found")

    return math.ceil(total_price)
