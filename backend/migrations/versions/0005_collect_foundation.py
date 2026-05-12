"""create collect foundation

Revision ID: 0005_collect_foundation
Revises: 0004_publish_foundation
Create Date: 2026-05-12
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0005_collect_foundation"
down_revision: str | None = "0004_publish_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "collect_tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("platform_accounts.id"), nullable=True),
        sa.Column("content_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("contents.id"), nullable=True),
        sa.Column("collect_type", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="pending"),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_retries", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("last_error", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_collect_tasks_status_schedule", "collect_tasks", ["status", "scheduled_at"])
    op.create_index("ix_collect_tasks_account_content", "collect_tasks", ["account_id", "content_id"])

    op.create_table(
        "collect_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("collect_tasks.id"), nullable=False),
        sa.Column("from_status", sa.String(length=40), nullable=True),
        sa.Column("to_status", sa.String(length=40), nullable=False),
        sa.Column("message", sa.Text(), nullable=False, server_default=""),
        sa.Column("details", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_collect_records_task", "collect_records", ["task_id"])


def downgrade() -> None:
    op.drop_index("ix_collect_records_task", table_name="collect_records")
    op.drop_table("collect_records")
    op.drop_index("ix_collect_tasks_account_content", table_name="collect_tasks")
    op.drop_index("ix_collect_tasks_status_schedule", table_name="collect_tasks")
    op.drop_table("collect_tasks")
