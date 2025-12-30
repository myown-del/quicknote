from __future__ import annotations

from uuid import UUID

from sqlalchemy import Uuid, String, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from quicknote.infrastructure.db.models.base import Base
from quicknote.infrastructure.db.models.mixins import CreatedUpdatedMixin


class Note(Base, CreatedUpdatedMixin):
    __tablename__ = "notes"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    title: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    text: Mapped[str | None] = mapped_column(String(length=4096), nullable=True)

    user = relationship("User", back_populates="notes", lazy="selectin")
