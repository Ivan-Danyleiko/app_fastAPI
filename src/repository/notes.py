from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.entity.models import Tag, Note
from src.schemas.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


async def get_notes(skip: int, offset: int, db: AsyncSession):
    """
    Retrieve a list of notes from the database.

    :param skip: The number of notes to skip.
    :param offset: The maximum number of notes to retrieve.
    :param db: AsyncSession instance for database interaction.
    :return: A list of Note objects.
    """
    stmt = select(Note).offset(skip).limit(offset)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_note(note_id: int, db: AsyncSession) -> Note:
    """
    Retrieve a specific note by its ID from the database.

    :param note_id: The ID of the note to retrieve.
    :param db: AsyncSession instance for database interaction.
    :return: The Note object corresponding to the given ID, if found.
    """
    result = await db.execute(select(Note).filter(Note.id == note_id))
    return result.scalar()


async def create_note(body: NoteModel, db: AsyncSession) -> Note:
    """
    Create a new note in the database.

    :param body: Data representing the new note.
    :param db: AsyncSession instance for database interaction.
    :return: The newly created Note object.
    """
    async with db.begin():
        tags = await db.execute(select(Tag).filter(Tag.id.in_(body.tags)))
        note = Note(title=body.title, description=body.description, tags=tags.scalars().all())
        db.add(note)
        await db.commit()
        await db.refresh(note)
    return note


async def remove_note(note_id: int, db: AsyncSession) -> Note | None:
    """
    Remove a note from the database.

    :param note_id: The ID of the note to remove.
    :param db: AsyncSession instance for database interaction.
    :return: The removed Note object, if found and deleted; otherwise, None.
    """
    async with db.begin():
        note = await db.execute(select(Note).filter(Note.id == note_id))
        if existing := note.scalar():
            await db.delete(existing)
            await db.commit()
        return existing


async def update_note(note_id: int, body: NoteUpdate, db: AsyncSession) -> Note | None:
    """
    Update an existing note in the database.

    :param note_id: The ID of the note to update.
    :param body: Data representing the updated note information.
    :param db: AsyncSession instance for database interaction.
    :return: The updated Note object, if found and updated; otherwise, None.
    """
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
    """
    Update the status (done or not done) of a note in the database.

    :param note_id: The ID of the note to update.
    :param body: Data representing the updated note status.
    :param db: AsyncSession instance for database interaction.
    :return: The updated Note object, if found and status updated; otherwise, None.
    """
    async with db.begin():
        note = await db.execute(select(Note).filter(Note.id == note_id))
        if existing := note.scalar():
            existing.done = body.done
            await db.commit()
        return existing
