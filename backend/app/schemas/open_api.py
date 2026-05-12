from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class APIKeyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    scopes: list[str] = Field(default_factory=lambda: ["contents:write", "ai:run", "publish:write", "collect:write", "metrics:read"])
    expires_at: datetime | None = None


class APIKeyCreated(BaseModel):
    id: UUID
    name: str
    key_id: str
    secret: str
    scopes: list[str]
    expires_at: datetime | None


class APIKeyRead(BaseModel):
    id: UUID
    name: str
    key_id: str
    scopes: list[str]
    is_active: bool
    last_used_at: datetime | None
    expires_at: datetime | None

    model_config = {"from_attributes": True}


class PublicMetricQuery(BaseModel):
    account_id: UUID | None = None
    content_id: UUID | None = None
