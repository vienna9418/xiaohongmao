from __future__ import annotations

from typing import Any


class AIAdapter:
    """OpenAI-compatible adapter placeholder.

    V1 foundation keeps the adapter interface stable while avoiding hard dependency on a
    specific model provider during early local development.
    """

    async def generate_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        output_schema: dict[str, Any] | None = None,
        temperature: int = 70,
    ) -> dict[str, Any]:
        return {
            "mode": "mock",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "temperature": temperature,
            "output_schema": output_schema or {},
            "result": "AI adapter is ready. Configure provider credentials to enable live generation.",
        }


ai_adapter = AIAdapter()
