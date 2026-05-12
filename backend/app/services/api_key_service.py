from __future__ import annotations

from datetime import UTC, datetime
from secrets import token_urlsafe

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.open_api import APIKey
from app.schemas.open_api import APIKeyCreate, APIKeyCreated


def generate_key_pair() -> tuple[str, str]:
    key_id = "xhm_" + token_urlsafe(18).replace("-", "_")[:24]
    secret = "xhm_secret_" + token_urlsafe(32)
    return key_id, secret


async def create_api_key(session: AsyncSession, payload: APIKeyCreate) -> APIKeyCreated:
    key_id, secret = generate_key_pair()
    api_key = APIKey(
        name=payload.name,
        key_id=key_id,
        secret_hash=get_password_hash(secret),
        scopes=payload.scopes,
        expires_at=payload.expires_at,
        is_active=True,
    )
    session.add(api_key)
    await session.commit()
    await session.refresh(api_key)
    return APIKeyCreated(
        id=api_key.id,
        name=api_key.name,
        key_id=api_key.key_id,
        secret=secret,
        scopes=api_key.scopes,
        expires_at=api_key.expires_at,
    )


async def list_api_keys(session: AsyncSession) -> list[APIKey]:
    result = await session.execute(select(APIKey).order_by(APIKey.created_at.desc()))
    return list(result.scalars().all())


async def get_active_api_key(session: AsyncSession, key_id: str) -> APIKey | None:
    result = await session.execute(select(APIKey).where(APIKey.key_id == key_id).where(APIKey.is_active.is_(True)))
    api_key = result.scalar_one_or_none()
    if api_key is None:
        return None
    if api_key.expires_at is not None and api_key.expires_at < datetime.now(UTC):
        return None
    return api_key


async def mark_api_key_used(session: AsyncSession, api_key: APIKey) -> None:
    api_key.last_used_at = datetime.now(UTC)
    await session.commit()


def verify_api_secret(secret: str, secret_hash: str) -> bool:
    return verify_password(secret, secret_hash)
