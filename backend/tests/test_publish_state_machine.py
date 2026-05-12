import pytest

from app.services.publish_state_machine import InvalidPublishTransition, assert_transition, can_transition


def test_publish_transition_allowed():
    assert can_transition("pending", "running")
    assert can_transition("running", "uploading")
    assert can_transition("uploading", "submitting")
    assert can_transition("submitting", "success")


def test_publish_transition_rejects_terminal_to_running():
    with pytest.raises(InvalidPublishTransition):
        assert_transition("success", "running")
