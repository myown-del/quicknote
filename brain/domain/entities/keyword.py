from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from brain.domain.entities.common import Entity


@dataclass
class Keyword(Entity):
    """
    Keyword referenced by notes via wikilinks.
    """

    id: UUID | None = field(default=None, kw_only=True)
    user_id: UUID
    name: str
    updated_at: datetime | None = None
    created_at: datetime | None = None
