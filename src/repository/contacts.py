from datetime import date, timedelta
from typing import Sequence

from sqlalchemy import select, extract, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.schemas import ContactCreate, ContactUpdate, ContactBase


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession) -> Contact:
    stmt = select(Contact).filter(Contact.id == contact_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_contact(body: ContactBase, db: AsyncSession, user: User):
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)  # (title=body.title,
    # description=body.description)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactBase, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.title = body.title
        contact.description = body.description
        contact.completed = body.completed
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def get_contacts_upcoming_birthdays(db: AsyncSession) -> Sequence[Contact]:
    today = date.today()
    next_week = today + timedelta(days=7)
    stmt = select(Contact).filter(
        and_(
            extract("month", Contact.birthday) == today.month,
            extract("day", Contact.birthday) >= today.day,
            extract("day", Contact.birthday) <= next_week.day,
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()
