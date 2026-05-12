from __future__ import annotations

from uuid import UUID

from app.tasks.celery_app import celery_app


@celery_app.task(name="collect.execute")
def execute_collect_task(task_id: str) -> dict[str, str]:
    """Collect task placeholder.

    The production collector will load the authorized account profile, open the
    creator console, parse account/content metrics, write metric_snapshots, and
    update collect task status. This placeholder validates queue wiring first.
    """
    parsed = UUID(task_id)
    return {"task_id": str(parsed), "status": "queued", "collector": "placeholder"}
