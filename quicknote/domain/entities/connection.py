from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from quicknote.domain.entities.common import Entity


@dataclass
class NoteConnection(Entity):
    """
    Connection between notes based on wikilinks.
    """

    from_note_id: UUID
    to_note_id: UUID
    user_id: UUID
    created_at: datetime | None = None
