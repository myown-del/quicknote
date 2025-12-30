from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from quicknote.domain.entities.common import Entity


@dataclass
class NoteDM(Entity):
    """
    Note domain model
    """

    id: UUID | None
    user_id: UUID
    title: str | None
    text: str | None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
