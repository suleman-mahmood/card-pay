from core.entrypoint.uow import FakeUnitOfWork
import rsa
from core.authentication.entrypoint import service as auth_svc
from core.authentication.domain import exceptions as auth_exc
import pytest

def test_decrypt_data(seed_verified_auth_user, add_1000_wallet_fake):
    uow = FakeUnitOfWork()
    sender , _ = seed_verified_auth_user(uow)
    recipient , _ = seed_verified_auth_user(uow)

    message = 'Hello, this is a secret message!'
    public_key = bytes(sender.public_key, encoding="utf-8")
    public_key = rsa.PublicKey.load_pkcs1(public_key)

    encryptedMessage = rsa.encrypt(message.encode(), public_key)
    decrypted_message = auth_svc.decrypt_data(digest=encryptedMessage, uow=uow, user_id=sender.id)
    assert decrypted_message == message

    with pytest.raises(auth_exc.DecryptionFailed, match="Data could not be decrypted"):
        decrypted_message = auth_svc.decrypt_data(digest=encryptedMessage, uow=uow, user_id=recipient.id)

    
    
