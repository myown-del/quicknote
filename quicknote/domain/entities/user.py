from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from quicknote.domain.entities.common import Entity


@dataclass
class UserDM(Entity):
    """
    User domain model
    """

    id: UUID
    telegram_id: int
    username: str | None
    first_name: str
    last_name: str | None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
