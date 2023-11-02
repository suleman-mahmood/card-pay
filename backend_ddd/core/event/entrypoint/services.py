from io import BytesIO

import qrcode
from core.comms.entrypoint import commands as comms_cmd
from core.entrypoint.uow import AbstractUnitOfWork
from core.event.entrypoint import queries as event_qry


def send_registration_email(paypro_id: str, uow: AbstractUnitOfWork):
    attendance_details = event_qry.get_attendance_details(paypro_id=paypro_id, uow=uow)

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

    comms_cmd.send_image_email(
        subject="Successful Registration Completed",
        text="Here is your attendance QR Code",
        to=attendance_details.email,
        image_bytes=qr_code_bytes,
    )
