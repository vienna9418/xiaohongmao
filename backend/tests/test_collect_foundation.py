from datetime import UTC, datetime

import pytest

from app.services.collect_scheduler import build_content_collect_schedule
from app.services.collect_state_machine import InvalidCollectTransition, assert_transition, can_transition


def test_collect_transition_allowed():
    assert can_transition("pending", "running")
    assert can_transition("running", "success")


def test_collect_transition_rejects_terminal_to_running():
    with pytest.raises(InvalidCollectTransition):
        assert_transition("success", "running")


def test_content_collect_schedule_offsets():
    base = datetime(2026, 5, 12, 8, 0, tzinfo=UTC)
    schedule = build_content_collect_schedule(base)
    assert len(schedule) == 5
    assert schedule[0].hour == 9
    assert schedule[-1].day == 19
