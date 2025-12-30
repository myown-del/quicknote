from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from quicknote.domain.entities.common import Entity


@dataclass
class JwtRefreshToken(Entity):
    id: UUID
    user_id: UUID
    token: str
    expires_at: datetime
    created_at: datetime | None = field(default=None, kw_only=True)
