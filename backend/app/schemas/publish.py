from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


PUBLISH_STATUSES = {
    "pending",
    "running",
    "login_required",
    "uploading",
    "submitting",
    "success",
    "failed",
    "cancelled",
}


class PublishTaskCreate(BaseModel):
    account_id: UUID
    content_id: UUID
    scheduled_at: datetime | None = None
    max_retries: int = Field(default=3, ge=0, le=10)


class PublishTaskRead(BaseModel):
    id: UUID
    account_id: UUID
    content_id: UUID
    status: str
    scheduled_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None
    retry_count: int
    max_retries: int
    last_error: str
    result_url: str | None
    screenshot_key: str | None

    model_config = {"from_attributes": True}


class PublishTaskTransition(BaseModel):
    to_status: str
    message: str = ""
    details: dict = Field(default_factory=dict)
