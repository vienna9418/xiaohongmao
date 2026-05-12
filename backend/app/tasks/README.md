# Worker runtime

Celery is used for production-stable background jobs.

## Start worker

```powershell
cd backend
celery -A app.tasks.celery_app.celery_app worker --loglevel=info --pool=solo
```

## Planned queues

- publish: automated creator-console publishing
- collect: account/content metrics collection
- ai: AI generation and Skill execution

## Current placeholder tasks

- `publish.execute`
- `collect.execute`
