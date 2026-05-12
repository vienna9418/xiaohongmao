from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class CollectTask(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "collect_tasks"
    __table_args__ = (
        Index("ix_collect_tasks_status_schedule", "status", "scheduled_at"),
        Index("ix_collect_tasks_account_content", "account_id", "content_id"),
    )

    account_id: Mapped[UUID | None] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("platform_accounts.id")
    )
    content_id: Mapped[UUID | None] = mapped_column(PgUUID(as_uuid=True), ForeignKey("contents.id"))
    collect_type: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="pending", nullable=False)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    last_error: Mapped[str] = mapped_column(Text, default="", nullable=False)

    records: Mapped[list["CollectRecord"]] = relationship(back_populates="task")


class CollectRecord(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "collect_records"
    __table_args__ = (Index("ix_collect_records_task", "task_id"),)

    task_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), ForeignKey("collect_tasks.id"))
    from_status: Mapped[str | None] = mapped_column(String(40))
    to_status: Mapped[str] = mapped_column(String(40), nullable=False)
    message: Mapped[str] = mapped_column(Text, default="", nullable=False)
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)

    task: Mapped[CollectTask] = relationship(back_populates="records")
