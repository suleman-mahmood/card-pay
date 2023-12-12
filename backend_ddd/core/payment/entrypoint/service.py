import json
from core.payment.domain import model as pmt_mdl

def validate_encrypted_timestamp(decrypted_data: str):
    decrypted_object = json.loads(decrypted_data)
    offline_qr_verification = pmt_mdl.OfflineQrExpiration(decrypted_object=decrypted_object)
    offline_qr_verification.verify_digest()

