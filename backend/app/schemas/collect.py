from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class CollectTaskCreate(BaseModel):
    account_id: UUID | None = None
    content_id: UUID | None = None
    collect_type: str = Field(pattern="^(account|content)$")
    scheduled_at: datetime | None = None
    max_retries: int = Field(default=3, ge=0, le=10)

    @model_validator(mode="after")
    def validate_target(self) -> "CollectTaskCreate":
        if self.collect_type == "account" and self.account_id is None:
            raise ValueError("account_id is required for account collection")
        if self.collect_type == "content" and self.content_id is None:
            raise ValueError("content_id is required for content collection")
        return self


class CollectTaskRead(BaseModel):
    id: UUID
    account_id: UUID | None
    content_id: UUID | None
    collect_type: str
    status: str
    scheduled_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None
    retry_count: int
    max_retries: int
    last_error: str

    model_config = {"from_attributes": True}


class CollectTaskTransition(BaseModel):
    to_status: str
    message: str = ""
    details: dict = Field(default_factory=dict)


class ContentCollectPlanCreate(BaseModel):
    content_id: UUID
    account_id: UUID | None = None
    published_at: datetime | None = None
