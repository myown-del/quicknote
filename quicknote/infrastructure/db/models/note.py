from __future__ import annotations

from uuid import UUID

from sqlalchemy import Uuid, String, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from quicknote.infrastructure.db.models.base import Base
from quicknote.infrastructure.db.models.mixins import CreatedUpdatedMixin


class Hashtag(Base):
    __tablename__ = "hashtags"

    id: Mapped[UUID] = Column(Uuid, primary_key=True)
    name: Mapped[str] = Column(String(64), unique=True)
    notes: Mapped[list[NoteHashtag]] = relationship(
        "NoteHashtag", back_populates="hashtag", lazy="selectin"
    )


class NoteHashtag(Base):
    __tablename__ = "notes_hashtags"

    note_id: Mapped[UUID] = Column(Uuid, ForeignKey("notes.id"), primary_key=True)
    hashtag_id: Mapped[UUID] = Column(Uuid, ForeignKey("hashtags.id"), primary_key=True)
    note: Mapped[Note] = relationship(
        "Note", back_populates="hashtags", lazy="selectin"
    )
    hashtag: Mapped[Hashtag] = relationship(
        "Hashtag", back_populates="notes", lazy="selectin"
    )


class Note(Base, CreatedUpdatedMixin):
    __tablename__ = "notes"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    text: Mapped[str] = mapped_column(String(length=4096), nullable=False)
    hashtags: Mapped[list[NoteHashtag]] = relationship(
        "NoteHashtag", back_populates="note", lazy="selectin"
    )

    user = relationship("User", back_populates="notes", lazy="selectin")
