from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.collect import CollectRecord, CollectTask
from app.schemas.collect import CollectTaskCreate
from app.services.collect_scheduler import build_content_collect_schedule
from app.services.collect_state_machine import assert_transition


async def create_collect_task(session: AsyncSession, payload: CollectTaskCreate) -> CollectTask:
    task = CollectTask(**payload.model_dump(), status="pending")
    session.add(task)
    await session.flush()
    session.add(
        CollectRecord(task_id=task.id, from_status=None, to_status="pending", message="Task created")
    )
    await session.commit()
    await session.refresh(task)
    return task


async def create_content_collect_plan(
    session: AsyncSession, content_id: UUID, account_id: UUID | None, published_at: datetime | None
) -> list[CollectTask]:
    tasks: list[CollectTask] = []
    for scheduled_at in build_content_collect_schedule(published_at):
        task = CollectTask(
            account_id=account_id,
            content_id=content_id,
            collect_type="content",
            scheduled_at=scheduled_at,
            status="pending",
        )
        session.add(task)
        tasks.append(task)
    await session.flush()
    for task in tasks:
        session.add(
            CollectRecord(
                task_id=task.id,
                from_status=None,
                to_status="pending",
                message="Content collect plan created",
            )
        )
    await session.commit()
    for task in tasks:
        await session.refresh(task)
    return tasks


async def list_collect_tasks(session: AsyncSession) -> list[CollectTask]:
    result = await session.execute(select(CollectTask).order_by(CollectTask.created_at.desc()))
    return list(result.scalars().all())


async def transition_collect_task(
    session: AsyncSession,
    task_id: UUID,
    to_status: str,
    message: str = "",
    details: dict | None = None,
) -> CollectTask:
    task = await session.get(CollectTask, task_id)
    if task is None:
        raise ValueError("Collect task not found")

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
        CollectRecord(
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
