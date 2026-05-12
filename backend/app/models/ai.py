from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AIModelConfig(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "ai_model_configs"

    provider: Mapped[str] = mapped_column(String(80), nullable=False)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    base_url: Mapped[str | None] = mapped_column(String(500))
    api_key_ref: Mapped[str | None] = mapped_column(String(255))
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class PromptTemplate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "prompt_templates"

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    category: Mapped[str] = mapped_column(String(80), default="general", nullable=False)
    variables: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    versions: Mapped[list["PromptVersion"]] = relationship(back_populates="template")
    skills: Mapped[list["Skill"]] = relationship(back_populates="prompt_template")


class PromptVersion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "prompt_versions"
    __table_args__ = (Index("ix_prompt_versions_template", "template_id", "version", unique=True),)

    template_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), ForeignKey("prompt_templates.id"))
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, default="", nullable=False)
    user_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    output_schema: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    temperature: Mapped[int] = mapped_column(Integer, default=70, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    template: Mapped[PromptTemplate] = relationship(back_populates="versions")


class Skill(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    category: Mapped[str] = mapped_column(String(80), default="content", nullable=False)
    prompt_template_id: Mapped[UUID | None] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("prompt_templates.id")
    )
    input_schema: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    output_schema: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    prompt_template: Mapped[PromptTemplate | None] = relationship(back_populates="skills")
    runs: Mapped[list["SkillRun"]] = relationship(back_populates="skill")


class SkillRun(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "skill_runs"
    __table_args__ = (Index("ix_skill_runs_skill_status", "skill_id", "status"),)

    skill_id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), ForeignKey("skills.id"))
    account_id: Mapped[UUID | None] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("platform_accounts.id")
    )
    content_id: Mapped[UUID | None] = mapped_column(PgUUID(as_uuid=True), ForeignKey("contents.id"))
    status: Mapped[str] = mapped_column(String(40), default="pending", nullable=False)
    inputs: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    rendered_prompt: Mapped[str] = mapped_column(Text, default="", nullable=False)
    outputs: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    error_message: Mapped[str] = mapped_column(Text, default="", nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    skill: Mapped[Skill] = relationship(back_populates="runs")
