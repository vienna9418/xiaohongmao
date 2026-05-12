from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db_session
from app.schemas.publish import PublishTaskCreate, PublishTaskRead, PublishTaskTransition
from app.services.publish_service import (
    create_publish_task,
    list_publish_tasks,
    transition_publish_task,
)
from app.services.publish_state_machine import InvalidPublishTransition

router = APIRouter(prefix="/api/v1/publish-tasks", tags=["publish"])


@router.get("", response_model=list[PublishTaskRead])
async def get_publish_tasks(session: AsyncSession = Depends(get_db_session)) -> list[PublishTaskRead]:
    return await list_publish_tasks(session)


@router.post("", response_model=PublishTaskRead, status_code=status.HTTP_201_CREATED)
async def post_publish_task(
    payload: PublishTaskCreate, session: AsyncSession = Depends(get_db_session)
) -> PublishTaskRead:
    return await create_publish_task(session, payload)


@router.post("/{task_id}/transition", response_model=PublishTaskRead)
async def post_publish_transition(
    task_id: UUID,
    payload: PublishTaskTransition,
    session: AsyncSession = Depends(get_db_session),
) -> PublishTaskRead:
    try:
        return await transition_publish_task(
            session,
            task_id,
            payload.to_status,
            message=payload.message,
            details=payload.details,
        )
    except InvalidPublishTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
