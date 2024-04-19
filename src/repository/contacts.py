from datetime import date, timedelta
from typing import Sequence

from sqlalchemy import select, extract, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact
from src.schemas.schemas import ContactCreate, ContactUpdate


async def get_contacts(db: AsyncSession, search_query: str = None) -> Sequence[Contact]:
    if search_query:
        stmt = select(Contact).filter(
            (Contact.name.ilike(f"%{search_query}%"))
            | (Contact.lastname.ilike(f"%{search_query}%"))
            | (Contact.email.ilike(f"%{search_query}%"))
        )
    else:
        stmt = select(Contact)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession) -> Contact:
    stmt = select(Contact).filter(Contact.id == contact_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_contact(contact: ContactCreate, db: AsyncSession) -> Contact:
    new_contact = Contact(**contact.dict())
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact


async def update_contact(contact_id: int, contact: ContactUpdate, db: AsyncSession) -> Contact:
    stmt = select(Contact).filter(Contact.id == contact_id)
    result = await db.execute(stmt)
    existing_contact = result.scalar_one_or_none()
    if existing_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(existing_contact, key, value)
        await db.commit()
    return existing_contact


async def delete_contact(contact_id: int, db: AsyncSession) -> Contact:
    stmt = select(Contact).filter(Contact.id == contact_id)
    result = await db.execute(stmt)
    existing_contact = result.scalar_one_or_none()
    if existing_contact:
        await db.delete(existing_contact)
        await db.commit()
    return existing_contact


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
