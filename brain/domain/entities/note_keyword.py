from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from brain.domain.entities.common import Entity


@dataclass
class NoteKeyword(Entity):
    """
    Link between a note and a keyword.
    """

    note_id: UUID
    keyword_id: UUID
    user_id: UUID
    created_at: datetime | None = None
