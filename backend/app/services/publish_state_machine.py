from __future__ import annotations

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"running", "cancelled"},
    "running": {"login_required", "uploading", "failed", "cancelled"},
    "login_required": {"pending", "failed", "cancelled"},
    "uploading": {"submitting", "failed", "cancelled"},
    "submitting": {"success", "failed", "cancelled"},
    "success": set(),
    "failed": {"pending"},
    "cancelled": set(),
}


class InvalidPublishTransition(ValueError):
    pass


def can_transition(from_status: str, to_status: str) -> bool:
    return to_status in ALLOWED_TRANSITIONS.get(from_status, set())


def assert_transition(from_status: str, to_status: str) -> None:
    if not can_transition(from_status, to_status):
        raise InvalidPublishTransition(f"Cannot transition publish task from {from_status} to {to_status}")
