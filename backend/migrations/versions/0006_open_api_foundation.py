"""create open api foundation

Revision ID: 0006_open_api_foundation
Revises: 0005_collect_foundation
Create Date: 2026-05-12
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006_open_api_foundation"
down_revision: str | None = "0005_collect_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "api_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("team_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("teams.id"), nullable=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("key_id", sa.String(length=80), nullable=False, unique=True),
        sa.Column("secret_hash", sa.String(length=255), nullable=False),
        sa.Column("scopes", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_api_keys_key_id_active", "api_keys", ["key_id", "is_active"])

    op.create_table(
        "api_request_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("api_key_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("api_keys.id"), nullable=True),
        sa.Column("method", sa.String(length=16), nullable=False),
        sa.Column("path", sa.String(length=500), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("request_id", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("error_message", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_api_request_logs_key_time", "api_request_logs", ["api_key_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_api_request_logs_key_time", table_name="api_request_logs")
    op.drop_table("api_request_logs")
    op.drop_index("ix_api_keys_key_id_active", table_name="api_keys")
    op.drop_table("api_keys")
