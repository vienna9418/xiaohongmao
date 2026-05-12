from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Content(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "contents"
    __table_args__ = (Index("ix_contents_account_status", "account_id", "status"),)

    team_id: Mapped[UUID | None] = mapped_column(PgUUID(as_uuid=True), ForeignKey("teams.id"))
    account_id: Mapped[UUID | None] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("platform_accounts.id")
    )
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    body: Mapped[str] = mapped_column(Text, default="", nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="draft", nullable=False)
    source: Mapped[str] = mapped_column(String(40), default="manual", nullable=False)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    account: Mapped["PlatformAccount | None"] = relationship(back_populates="contents")
    assets: Mapped[list["ContentAsset"]] = relationship(back_populates="content")


class ContentAsset(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "content_assets"

    content_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), ForeignKey("contents.id"))
    asset_type: Mapped[str] = mapped_column(String(40), nullable=False)
    object_key: Mapped[str] = mapped_column(String(500), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    content: Mapped[Content] = relationship(back_populates="assets")


class MetricSnapshot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "metric_snapshots"
    __table_args__ = (Index("ix_metric_snapshots_account_content", "account_id", "content_id"),)

    account_id: Mapped[UUID | None] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("platform_accounts.id")
    )
    content_id: Mapped[UUID | None] = mapped_column(PgUUID(as_uuid=True), ForeignKey("contents.id"))
    metric_type: Mapped[str] = mapped_column(String(40), nullable=False)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
