from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime

from quicknote.domain.entities.common import Entity


@dataclass
class JwtToken:
    access_token: str
    expires_at: datetime


@dataclass
class JwtTokens:
    access_token: str
    expires_at: datetime
    refresh_token: str
    refresh_expires_at: datetime


@dataclass
class JwtRefreshToken(Entity):
    id: UUID
    user_id: UUID
    token: str
    expires_at: datetime
    created_at: datetime | None = field(default=None, kw_only=True)
