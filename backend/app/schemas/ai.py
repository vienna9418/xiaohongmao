from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class AIModelConfigRead(BaseModel):
    id: UUID
    provider: str
    model: str
    base_url: str | None
    is_default: bool
    is_active: bool

    model_config = {"from_attributes": True}


class PromptTemplateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    code: str = Field(min_length=1, max_length=120)
    description: str = ""
    category: str = "general"
    variables: list[str] = Field(default_factory=list)
    system_prompt: str = ""
    user_prompt: str = Field(min_length=1)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    temperature: int = Field(default=70, ge=0, le=200)


class PromptTemplateRead(BaseModel):
    id: UUID
    name: str
    code: str
    description: str
    category: str
    variables: list[str]
    is_active: bool

    model_config = {"from_attributes": True}


class PromptRenderRequest(BaseModel):
    user_prompt: str
    variables: dict[str, Any] = Field(default_factory=dict)


class PromptRenderResponse(BaseModel):
    rendered_prompt: str
    missing_variables: list[str]


class SkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    code: str = Field(min_length=1, max_length=120)
    description: str = ""
    category: str = "content"
    prompt_template_id: UUID | None = None
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)


class SkillRead(BaseModel):
    id: UUID
    name: str
    code: str
    description: str
    category: str
    prompt_template_id: UUID | None
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    score: int
    is_active: bool

    model_config = {"from_attributes": True}


class SkillRunRequest(BaseModel):
    inputs: dict[str, Any] = Field(default_factory=dict)
    account_id: UUID | None = None
    content_id: UUID | None = None
    dry_run: bool = True


class SkillRunRead(BaseModel):
    id: UUID
    skill_id: UUID
    account_id: UUID | None
    content_id: UUID | None
    status: str
    inputs: dict[str, Any]
    rendered_prompt: str
    outputs: dict[str, Any]
    error_message: str

    model_config = {"from_attributes": True}
