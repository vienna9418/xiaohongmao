from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db_session
from app.schemas.content import ContentCreate, ContentRead
from app.services.content_service import create_content, list_contents

router = APIRouter(prefix="/api/v1/contents", tags=["contents"])


@router.get("", response_model=list[ContentRead])
async def get_contents(session: AsyncSession = Depends(get_db_session)) -> list[ContentRead]:
    return await list_contents(session)


@router.post("", response_model=ContentRead, status_code=status.HTTP_201_CREATED)
async def post_content(
    payload: ContentCreate, session: AsyncSession = Depends(get_db_session)
) -> ContentRead:
    return await create_content(session, payload)
