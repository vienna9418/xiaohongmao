from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db_session
from app.schemas.ai import (
    PromptRenderRequest,
    PromptRenderResponse,
    PromptTemplateCreate,
    PromptTemplateRead,
    SkillCreate,
    SkillRead,
    SkillRunRead,
    SkillRunRequest,
)
from app.services.ai_service import (
    create_prompt_template,
    create_skill,
    list_prompt_templates,
    list_skills,
    run_skill,
)
from app.services.prompt_engine import render_prompt

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


@router.get("/prompts", response_model=list[PromptTemplateRead])
async def get_prompts(session: AsyncSession = Depends(get_db_session)) -> list[PromptTemplateRead]:
    return await list_prompt_templates(session)


@router.post("/prompts", response_model=PromptTemplateRead, status_code=status.HTTP_201_CREATED)
async def post_prompt(
    payload: PromptTemplateCreate, session: AsyncSession = Depends(get_db_session)
) -> PromptTemplateRead:
    return await create_prompt_template(session, payload)


@router.post("/prompts/render", response_model=PromptRenderResponse)
async def post_render_prompt(payload: PromptRenderRequest) -> PromptRenderResponse:
    rendered, missing = render_prompt(payload.user_prompt, payload.variables)
    return PromptRenderResponse(rendered_prompt=rendered, missing_variables=missing)


@router.get("/skills", response_model=list[SkillRead])
async def get_skills(session: AsyncSession = Depends(get_db_session)) -> list[SkillRead]:
    return await list_skills(session)


@router.post("/skills", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
async def post_skill(
    payload: SkillCreate, session: AsyncSession = Depends(get_db_session)
) -> SkillRead:
    return await create_skill(session, payload)


@router.post("/skills/{skill_id}/run", response_model=SkillRunRead)
async def post_skill_run(
    skill_id: UUID,
    payload: SkillRunRequest,
    session: AsyncSession = Depends(get_db_session),
) -> SkillRunRead:
    try:
        return await run_skill(session, skill_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

