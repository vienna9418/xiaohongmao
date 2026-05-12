from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db_session
from app.schemas.collect import (
    CollectTaskCreate,
    CollectTaskRead,
    CollectTaskTransition,
    ContentCollectPlanCreate,
)
from app.services.collect_service import (
    create_collect_task,
    create_content_collect_plan,
    list_collect_tasks,
    transition_collect_task,
)
from app.services.collect_state_machine import InvalidCollectTransition

router = APIRouter(prefix="/api/v1/collect-tasks", tags=["collect"])


@router.get("", response_model=list[CollectTaskRead])
async def get_collect_tasks(session: AsyncSession = Depends(get_db_session)) -> list[CollectTaskRead]:
    return await list_collect_tasks(session)


@router.post("", response_model=CollectTaskRead, status_code=status.HTTP_201_CREATED)
async def post_collect_task(
    payload: CollectTaskCreate, session: AsyncSession = Depends(get_db_session)
) -> CollectTaskRead:
    return await create_collect_task(session, payload)


@router.post("/content-plan", response_model=list[CollectTaskRead], status_code=status.HTTP_201_CREATED)
async def post_content_collect_plan(
    payload: ContentCollectPlanCreate, session: AsyncSession = Depends(get_db_session)
) -> list[CollectTaskRead]:
    return await create_content_collect_plan(
        session, payload.content_id, payload.account_id, payload.published_at
    )


@router.post("/{task_id}/transition", response_model=CollectTaskRead)
async def post_collect_transition(
    task_id: UUID,
    payload: CollectTaskTransition,
    session: AsyncSession = Depends(get_db_session),
) -> CollectTaskRead:
    try:
        return await transition_collect_task(
            session,
            task_id,
            payload.to_status,
            message=payload.message,
            details=payload.details,
        )
    except InvalidCollectTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
