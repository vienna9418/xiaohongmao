"""create account and content foundation

Revision ID: 0002_account_content_foundation
Revises: 0001_auth_foundation
Create Date: 2026-05-12
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_account_content_foundation"
down_revision: str | None = "0001_auth_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "platform_accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("teams.id"), nullable=True),
        sa.Column("platform", sa.String(length=40), nullable=False, server_default="rednote"),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("handle", sa.String(length=120), nullable=True),
        sa.Column("persona", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("owner_name", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="active"),
        sa.Column("health_score", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("login_status", sa.String(length=40), nullable=False, server_default="unknown"),
        sa.Column("last_collected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_platform_accounts_team_status", "platform_accounts", ["team_id", "status"])

    op.create_table(
        "contents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("teams.id"), nullable=True),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("platform_accounts.id"), nullable=True),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("tags", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="draft"),
        sa.Column("source", sa.String(length=40), nullable=False, server_default="manual"),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_contents_account_status", "contents", ["account_id", "status"])

    op.create_table(
        "content_assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("content_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("contents.id"), nullable=False),
        sa.Column("asset_type", sa.String(length=40), nullable=False),
        sa.Column("object_key", sa.String(length=500), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "metric_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("platform_accounts.id"), nullable=True),
        sa.Column("content_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("contents.id"), nullable=True),
        sa.Column("metric_type", sa.String(length=40), nullable=False),
        sa.Column("metrics", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_metric_snapshots_account_content", "metric_snapshots", ["account_id", "content_id"])


def downgrade() -> None:
    op.drop_index("ix_metric_snapshots_account_content", table_name="metric_snapshots")
    op.drop_table("metric_snapshots")
    op.drop_table("content_assets")
    op.drop_index("ix_contents_account_status", table_name="contents")
    op.drop_table("contents")
    op.drop_index("ix_platform_accounts_team_status", table_name="platform_accounts")
    op.drop_table("platform_accounts")
