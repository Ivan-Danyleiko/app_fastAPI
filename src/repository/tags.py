from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.entity.models import Tag
from src.schemas.schemas import TagModel


async def get_tags(skip: int, limit: int, db: AsyncSession):
    """
    Retrieve a list of tags from the database.

    :param skip: Number of tags to skip.
    :param limit: Maximum number of tags to retrieve.
    :param db: AsyncSession instance for database interaction.
    :return: List of Tag objects.
    """
    stmt = select(Tag).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_tag(tag_id: int, db: AsyncSession) -> Tag:
    """
    Retrieve a specific tag by its ID from the database.

    :param tag_id: ID of the tag to retrieve.
    :param db: AsyncSession instance for database interaction.
    :return: Tag object corresponding to the given ID, if found.
    """
    stmt = select(Tag).filter(Tag.id == tag_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_tag(body: TagModel, db: AsyncSession) -> Tag:
    """
    Create a new tag in the database.

    :param body: Data representing the new tag.
    :param db: AsyncSession instance for database interaction.
    :return: Newly created Tag object.
    """
    tag = Tag(name=body.name)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagModel, db: AsyncSession) -> Tag | None:
    """
    Update an existing tag in the database.

    :param tag_id: ID of the tag to update.
    :param body: Data representing the updated tag information.
    :param db: AsyncSession instance for database interaction.
    :return: Updated Tag object, if found and updated; otherwise, None.
    """
    stmt = select(Tag).filter(Tag.id == tag_id)
    result = await db.execute(stmt)
    tag = result.scalar_one_or_none()
    if tag:
        tag.name = body.name
        await db.commit()
    return tag


async def remove_tag(tag_id: int, db: AsyncSession) -> Tag | None:
    """
    Remove a tag from the database.

    :param tag_id: ID of the tag to remove.
    :param db: AsyncSession instance for database interaction.
    :return: Removed Tag object, if found and deleted; otherwise, None.
    """
    stmt = select(Tag).filter(Tag.id == tag_id)
    result = await db.execute(stmt)
    tag = result.scalar_one_or_none()
    if tag:
        await db.delete(tag)
        await db.commit()
    return tag
