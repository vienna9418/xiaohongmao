from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "xiaohongmao",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.publish_tasks"],
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=60 * 15,
    task_soft_time_limit=60 * 10,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    timezone="Asia/Shanghai",
)
