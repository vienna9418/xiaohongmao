from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class PlatformAccount(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "platform_accounts"
    __table_args__ = (Index("ix_platform_accounts_team_status", "team_id", "status"),)

    team_id: Mapped[UUID | None] = mapped_column(PgUUID(as_uuid=True), ForeignKey("teams.id"))
    platform: Mapped[str] = mapped_column(String(40), default="rednote", nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    handle: Mapped[str | None] = mapped_column(String(120))
    persona: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    owner_name: Mapped[str] = mapped_column(String(120), default="", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="active", nullable=False)
    health_score: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    login_status: Mapped[str] = mapped_column(String(40), default="unknown", nullable=False)
    last_collected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    contents: Mapped[list["Content"]] = relationship(back_populates="account")
