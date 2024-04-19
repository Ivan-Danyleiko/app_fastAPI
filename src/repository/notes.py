from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.entity.models import Tag, Note
from src.schemas.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


async def get_notes(skip: int, offset: int, db: AsyncSession):
    stmt = select(Note).offset(skip).limit(offset)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_note(note_id: int, db: AsyncSession) -> Note:
    result = await db.execute(select(Note).filter(Note.id == note_id))
    return result.scalar()


async def create_note(body: NoteModel, db: AsyncSession) -> Note:
    async with db.begin():
        tags = await db.execute(select(Tag).filter(Tag.id.in_(body.tags)))
        note = Note(title=body.title, description=body.description, tags=tags.scalars().all())
        db.add(note)
        await db.commit()
        await db.refresh(note)
    return note


async def remove_note(note_id: int, db: AsyncSession) -> Note | None:
    async with db.begin():
        note = await db.execute(select(Note).filter(Note.id == note_id))
        if existing := note.scalar():
            await db.delete(existing)
            await db.commit()
        return existing


async def update_note(note_id: int, body: NoteUpdate, db: AsyncSession) -> Note | None:
    async with db.begin():
        note = await db.execute(select(Note).filter(Note.id == note_id))
        if existing := note.scalar():
            tags = await db.execute(select(Tag).filter(Tag.id.in_(body.tags)))
            existing.title = body.title
            existing.description = body.description
            existing.done = body.done
            existing.tags = tags.scalars().all()
            await db.commit()
        return existing


async def update_status_note(note_id: int, body: NoteStatusUpdate, db: AsyncSession) -> Note | None:
    async with db.begin():
        note = await db.execute(select(Note).filter(Note.id == note_id))
        if existing := note.scalar():
            existing.done = body.done
            await db.commit()
        return existing
