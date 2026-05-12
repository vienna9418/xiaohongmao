from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Content
from app.schemas.content import ContentCreate


async def create_content(session: AsyncSession, payload: ContentCreate) -> Content:
    content = Content(**payload.model_dump())
    session.add(content)
    await session.commit()
    await session.refresh(content)
    return content


async def list_contents(session: AsyncSession) -> list[Content]:
    result = await session.execute(select(Content).order_by(Content.created_at.desc()))
    return list(result.scalars().all())
