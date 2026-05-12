from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db_session
from app.schemas.account import PlatformAccountCreate, PlatformAccountRead
from app.services.account_service import create_account, list_accounts

router = APIRouter(prefix="/api/v1/accounts", tags=["accounts"])


@router.get("", response_model=list[PlatformAccountRead])
async def get_accounts(session: AsyncSession = Depends(get_db_session)) -> list[PlatformAccountRead]:
    return await list_accounts(session)


@router.post("", response_model=PlatformAccountRead, status_code=status.HTTP_201_CREATED)
async def post_account(
    payload: PlatformAccountCreate, session: AsyncSession = Depends(get_db_session)
) -> PlatformAccountRead:
    return await create_account(session, payload)
