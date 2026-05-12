from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai import PromptTemplate, PromptVersion, Skill, SkillRun
from app.schemas.ai import PromptTemplateCreate, SkillCreate, SkillRunRequest
from app.services.ai_adapter import ai_adapter
from app.services.prompt_engine import render_prompt


async def create_prompt_template(
    session: AsyncSession, payload: PromptTemplateCreate
) -> PromptTemplate:
    template = PromptTemplate(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        category=payload.category,
        variables=payload.variables,
    )
    session.add(template)
    await session.flush()
    version = PromptVersion(
        template_id=template.id,
        version=1,
        system_prompt=payload.system_prompt,
        user_prompt=payload.user_prompt,
        output_schema=payload.output_schema,
        temperature=payload.temperature,
        is_current=True,
    )
    session.add(version)
    await session.commit()
    await session.refresh(template)
    return template


async def list_prompt_templates(session: AsyncSession) -> list[PromptTemplate]:
    result = await session.execute(select(PromptTemplate).order_by(PromptTemplate.created_at.desc()))
    return list(result.scalars().all())


async def create_skill(session: AsyncSession, payload: SkillCreate) -> Skill:
    skill = Skill(**payload.model_dump())
    session.add(skill)
    await session.commit()
    await session.refresh(skill)
    return skill


async def list_skills(session: AsyncSession) -> list[Skill]:
    result = await session.execute(select(Skill).order_by(Skill.created_at.desc()))
    return list(result.scalars().all())


async def run_skill(session: AsyncSession, skill_id: UUID, payload: SkillRunRequest) -> SkillRun:
    skill = await session.get(Skill, skill_id)
    if skill is None:
        raise ValueError("Skill not found")

    prompt = ""
    output_schema = skill.output_schema
    if skill.prompt_template_id:
        result = await session.execute(
            select(PromptVersion)
            .where(PromptVersion.template_id == skill.prompt_template_id)
            .where(PromptVersion.is_current.is_(True))
            .order_by(PromptVersion.version.desc())
        )
        version = result.scalar_one_or_none()
        if version is not None:
            prompt, missing = render_prompt(version.user_prompt, payload.inputs)
            if missing:
                output = {"missing_variables": missing}
                status = "failed"
                error = "Missing prompt variables"
            else:
                ai_output = await ai_adapter.generate_json(
                    system_prompt=version.system_prompt,
                    user_prompt=prompt,
                    output_schema=version.output_schema or output_schema,
                    temperature=version.temperature,
                )
                output = ai_output
                status = "success" if payload.dry_run else "pending"
                error = ""
        else:
            output = {}
            status = "failed"
            error = "Prompt version not found"
    else:
        prompt = str(payload.inputs)
        output = {"result": "Skill has no prompt template bound", "inputs": payload.inputs}
        status = "success"
        error = ""

    now = datetime.now(UTC)
    run = SkillRun(
        skill_id=skill.id,
        account_id=payload.account_id,
        content_id=payload.content_id,
        status=status,
        inputs=payload.inputs,
        rendered_prompt=prompt,
        outputs=output,
        error_message=error,
        started_at=now,
        finished_at=now,
    )
    session.add(run)
    await session.commit()
    await session.refresh(run)
    return run
