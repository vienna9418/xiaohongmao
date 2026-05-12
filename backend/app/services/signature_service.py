from __future__ import annotations

import hashlib
import hmac
import time
from dataclasses import dataclass

SIGNATURE_TTL_SECONDS = 300


@dataclass(frozen=True)
class SignaturePayload:
    method: str
    path: str
    timestamp: str
    body: str

    def canonical(self) -> str:
        return "\n".join([self.method.upper(), self.path, self.timestamp, self.body])


def sign_request(secret: str, payload: SignaturePayload) -> str:
    digest = hmac.new(secret.encode("utf-8"), payload.canonical().encode("utf-8"), hashlib.sha256)
    return digest.hexdigest()


def verify_signature(secret: str, payload: SignaturePayload, signature: str) -> bool:
    try:
        timestamp = int(payload.timestamp)
    except ValueError:
        return False
    if abs(int(time.time()) - timestamp) > SIGNATURE_TTL_SECONDS:
        return False
    expected = sign_request(secret, payload)
    return hmac.compare_digest(expected, signature)
