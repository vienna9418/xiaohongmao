from __future__ import annotations

import re
from typing import Any

VARIABLE_PATTERN = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


def find_prompt_variables(template: str) -> list[str]:
    return sorted(set(VARIABLE_PATTERN.findall(template)))


def render_prompt(template: str, variables: dict[str, Any]) -> tuple[str, list[str]]:
    missing: list[str] = []

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in variables:
            missing.append(key)
            return match.group(0)
        return str(variables[key])

    rendered = VARIABLE_PATTERN.sub(replace, template)
    return rendered, sorted(set(missing))
