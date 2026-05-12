from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ContentCreate(BaseModel):
    account_id: UUID | None = None
    title: str = Field(min_length=1, max_length=120)
    body: str = ""
    tags: list[str] = Field(default_factory=list)
    source: str = "manual"


class ContentRead(BaseModel):
    id: UUID
    account_id: UUID | None
    title: str
    body: str
    tags: list[str]
    status: str
    source: str
    scheduled_at: datetime | None
    published_at: datetime | None

    model_config = {"from_attributes": True}
