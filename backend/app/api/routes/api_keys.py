from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db_session
from app.schemas.open_api import APIKeyCreate, APIKeyCreated, APIKeyRead
from app.services.api_key_service import create_api_key, list_api_keys

router = APIRouter(prefix="/api/v1/api-keys", tags=["api-keys"])


@router.get("", response_model=list[APIKeyRead])
async def get_api_keys(session: AsyncSession = Depends(get_db_session)) -> list[APIKeyRead]:
    return await list_api_keys(session)


@router.post("", response_model=APIKeyCreated, status_code=status.HTTP_201_CREATED)
async def post_api_key(
    payload: APIKeyCreate, session: AsyncSession = Depends(get_db_session)
) -> APIKeyCreated:
    return await create_api_key(session, payload)
