from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db_session
from app.api.deps.open_api import PublicAPIContext, require_scope
from app.schemas.ai import SkillRunRead, SkillRunRequest
from app.schemas.collect import CollectTaskCreate, CollectTaskRead
from app.schemas.content import ContentCreate, ContentRead
from app.schemas.publish import PublishTaskCreate, PublishTaskRead
from app.services.ai_service import run_skill
from app.services.collect_service import create_collect_task
from app.services.content_service import create_content
from app.services.publish_service import create_publish_task

router = APIRouter(prefix="/api/public/v1", tags=["public-api"])


@router.post("/contents", response_model=ContentRead)
async def public_create_content(
    payload: ContentCreate,
    session: AsyncSession = Depends(get_db_session),
    _: PublicAPIContext = Depends(require_scope("contents:write")),
) -> ContentRead:
    return await create_content(session, payload)


@router.post("/skills/{skill_id}/run", response_model=SkillRunRead)
async def public_run_skill(
    skill_id: UUID,
    payload: SkillRunRequest,
    session: AsyncSession = Depends(get_db_session),
    _: PublicAPIContext = Depends(require_scope("ai:run")),
) -> SkillRunRead:
    try:
        return await run_skill(session, skill_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/publish-tasks", response_model=PublishTaskRead)
async def public_create_publish_task(
    payload: PublishTaskCreate,
    session: AsyncSession = Depends(get_db_session),
    _: PublicAPIContext = Depends(require_scope("publish:write")),
) -> PublishTaskRead:
    return await create_publish_task(session, payload)


@router.post("/collect-tasks", response_model=CollectTaskRead)
async def public_create_collect_task(
    payload: CollectTaskCreate,
    session: AsyncSession = Depends(get_db_session),
    _: PublicAPIContext = Depends(require_scope("collect:write")),
) -> CollectTaskRead:
    return await create_collect_task(session, payload)
