from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.entity.models import Tag
from src.schemas.schemas import TagModel


async def get_tags(skip: int, limit: int, db: AsyncSession):
    stmt = select(Tag).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_tag(tag_id: int, db: AsyncSession) -> Tag:
    stmt = select(Tag).filter(Tag.id == tag_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_tag(body: TagModel, db: AsyncSession) -> Tag:
    tag = Tag(name=body.name)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagModel, db: AsyncSession) -> Tag | None:
    stmt = select(Tag).filter(Tag.id == tag_id)
    result = await db.execute(stmt)
    tag = result.scalar_one_or_none()
    if tag:
        tag.name = body.name
        await db.commit()
    return tag


async def remove_tag(tag_id: int, db: AsyncSession) -> Tag | None:
    stmt = select(Tag).filter(Tag.id == tag_id)
    result = await db.execute(stmt)
    tag = result.scalar_one_or_none()
    if tag:
        await db.delete(tag)
        await db.commit()
    return tag
