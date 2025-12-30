from dataclasses import dataclass, field
from datetime import datetime
from tkinter import N
from uuid import UUID

from quicknote.domain.entities.common import Entity


@dataclass
class Note(Entity):
    """
    Note domain model
    """

    id: UUID | None = field(default=None, kw_only=True)
    user_id: UUID
    title: str | None = None
    text: str | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None
