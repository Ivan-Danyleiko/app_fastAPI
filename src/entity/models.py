import datetime
from sqlalchemy import Column, Integer, String, Boolean, func, Table, DateTime
from sqlalchemy.orm import Mapped, relationship, DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Date


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    lastname: Mapped[str] = mapped_column(String(25), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[int] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    # birthday: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    birthday: Mapped[datetime.date] = mapped_column(Date)

    notes = relationship("Note", secondary="contact_note_association")


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[int] = mapped_column(DateTime, default=func.now())
    description: Mapped[int] = mapped_column(String(150), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)

    tags = relationship("Tag", secondary="note_tag_association")


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)


note_tag_association = Table(
    "note_tag_association",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"))
)

contact_note_association = Table(
    "contact_note_association",
    Base.metadata,
    Column("contact_id", Integer, ForeignKey("contacts.id", ondelete="CASCADE")),
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE"))
)
