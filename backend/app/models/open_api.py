from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class APIKey(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "api_keys"
    __table_args__ = (Index("ix_api_keys_key_id_active", "key_id", "is_active"),)

    team_id: Mapped[UUID | None] = mapped_column(PgUUID(as_uuid=True), ForeignKey("teams.id"))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    key_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    secret_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    scopes: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class APIRequestLog(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "api_request_logs"
    __table_args__ = (Index("ix_api_request_logs_key_time", "api_key_id", "created_at"),)

    api_key_id: Mapped[UUID | None] = mapped_column(PgUUID(as_uuid=True), ForeignKey("api_keys.id"))
    method: Mapped[str] = mapped_column(String(16), nullable=False)
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    request_id: Mapped[str] = mapped_column(String(120), default="", nullable=False)
    error_message: Mapped[str] = mapped_column(Text, default="", nullable=False)
