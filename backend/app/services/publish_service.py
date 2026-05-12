from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.publish import PublishRecord, PublishTask
from app.schemas.publish import PublishTaskCreate
from app.services.publish_state_machine import assert_transition


async def create_publish_task(session: AsyncSession, payload: PublishTaskCreate) -> PublishTask:
    task = PublishTask(**payload.model_dump(), status="pending")
    session.add(task)
    await session.flush()
    session.add(
        PublishRecord(task_id=task.id, from_status=None, to_status="pending", message="Task created")
    )
    await session.commit()
    await session.refresh(task)
    return task


async def list_publish_tasks(session: AsyncSession) -> list[PublishTask]:
    result = await session.execute(select(PublishTask).order_by(PublishTask.created_at.desc()))
    return list(result.scalars().all())


async def transition_publish_task(
    session: AsyncSession,
    task_id: UUID,
    to_status: str,
    message: str = "",
    details: dict | None = None,
) -> PublishTask:
    task = await session.get(PublishTask, task_id)
    if task is None:
        raise ValueError("Publish task not found")

    from_status = task.status
    assert_transition(from_status, to_status)
    task.status = to_status
    now = datetime.now(UTC)
    if to_status == "running" and task.started_at is None:
        task.started_at = now
    if to_status in {"success", "failed", "cancelled"}:
        task.finished_at = now
    if to_status == "failed":
        task.retry_count += 1
        task.last_error = message

    session.add(
        PublishRecord(
            task_id=task.id,
            from_status=from_status,
            to_status=to_status,
            message=message,
            details=details or {},
        )
    )
    await session.commit()
    await session.refresh(task)
    return task
