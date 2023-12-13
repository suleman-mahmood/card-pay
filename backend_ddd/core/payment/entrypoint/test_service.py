from datetime import datetime, timedelta
from core.entrypoint.uow import FakeUnitOfWork
import json
from core.payment.entrypoint import service as pmt_svc
from core.payment.domain import exceptions as pmt_exc
import pytest

def test_encrypted_timestamp():
    decrypted_data = json.dumps(
        {"current_timestamp": str(datetime.now() + timedelta(hours=5) - timedelta(minutes=2))}
    )
    pmt_svc.validate_encrypted_timestamp(decrypted_data=decrypted_data)

    with pytest.raises(pmt_exc.OfflineQrExpired, match="Offline QR Code has expired"):
        decrypted_data = json.dumps(
            {"current_timestamp": str(datetime.now() + timedelta(hours=5) - timedelta(minutes=6))}
        )
        pmt_svc.validate_encrypted_timestamp(decrypted_data=decrypted_data)