from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db_session
from app.models.open_api import APIKey
from app.services.api_key_service import get_active_api_key, mark_api_key_used, verify_api_secret
from app.services.signature_service import SignaturePayload, verify_signature


@dataclass(frozen=True)
class PublicAPIContext:
    api_key: APIKey


async def get_public_api_context(
    request: Request,
    x_xhm_key: str = Header(alias="X-XHM-Key"),
    x_xhm_secret: str = Header(alias="X-XHM-Secret"),
    x_xhm_timestamp: str = Header(alias="X-XHM-Timestamp"),
    x_xhm_signature: str = Header(alias="X-XHM-Signature"),
    session: AsyncSession = Depends(get_db_session),
) -> PublicAPIContext:
    api_key = await get_active_api_key(session, x_xhm_key)
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    if not verify_api_secret(x_xhm_secret, api_key.secret_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API secret")

    body = (await request.body()).decode("utf-8")
    payload = SignaturePayload(
        method=request.method,
        path=request.url.path,
        timestamp=x_xhm_timestamp,
        body=body,
    )
    if not verify_signature(x_xhm_secret, payload, x_xhm_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
    await mark_api_key_used(session, api_key)
    return PublicAPIContext(api_key=api_key)


def require_scope(scope: str):
    async def dependency(ctx: PublicAPIContext = Depends(get_public_api_context)) -> PublicAPIContext:
        if scope not in ctx.api_key.scopes and "*" not in ctx.api_key.scopes:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing API scope")
        return ctx

    return dependency
