from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import PlatformAccount
from app.schemas.account import PlatformAccountCreate


async def create_account(session: AsyncSession, payload: PlatformAccountCreate) -> PlatformAccount:
    account = PlatformAccount(**payload.model_dump())
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account


async def list_accounts(session: AsyncSession) -> list[PlatformAccount]:
    result = await session.execute(select(PlatformAccount).order_by(PlatformAccount.created_at.desc()))
    return list(result.scalars().all())
