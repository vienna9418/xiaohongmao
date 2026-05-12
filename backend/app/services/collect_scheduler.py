from __future__ import annotations

from datetime import UTC, datetime, timedelta

CONTENT_COLLECT_OFFSETS = [
    timedelta(hours=1),
    timedelta(hours=6),
    timedelta(hours=24),
    timedelta(hours=72),
    timedelta(days=7),
]


def build_content_collect_schedule(published_at: datetime | None = None) -> list[datetime]:
    base = published_at or datetime.now(UTC)
    if base.tzinfo is None:
        base = base.replace(tzinfo=UTC)
    return [base + offset for offset in CONTENT_COLLECT_OFFSETS]
