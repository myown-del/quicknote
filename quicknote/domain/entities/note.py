from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from quicknote.domain.entities.common import Entity


@dataclass
class NoteDM(Entity):
    """
    Note domain model
    """

    id: UUID
    user_id: UUID
    text: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)