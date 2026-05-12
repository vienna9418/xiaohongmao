from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PlatformAccountCreate(BaseModel):
    display_name: str = Field(min_length=1, max_length=120)
    handle: str | None = Field(default=None, max_length=120)
    persona: str = Field(default="", max_length=255)
    owner_name: str = Field(default="", max_length=120)


class PlatformAccountRead(BaseModel):
    id: UUID
    display_name: str
    handle: str | None
    persona: str
    owner_name: str
    status: str
    health_score: int
    login_status: str
    last_collected_at: datetime | None

    model_config = {"from_attributes": True}
