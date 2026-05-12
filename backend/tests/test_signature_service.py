import time

from app.services.signature_service import SignaturePayload, sign_request, verify_signature


def test_signature_roundtrip():
    payload = SignaturePayload(method="POST", path="/api/public/v1/contents", timestamp=str(int(time.time())), body="{}")
    signature = sign_request("secret", payload)
    assert verify_signature("secret", payload, signature)


def test_signature_rejects_wrong_secret():
    payload = SignaturePayload(method="POST", path="/api/public/v1/contents", timestamp=str(int(time.time())), body="{}")
    signature = sign_request("secret", payload)
    assert not verify_signature("wrong", payload, signature)
