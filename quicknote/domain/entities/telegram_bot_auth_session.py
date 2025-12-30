from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from quicknote.domain.entities.common import Entity


@dataclass
class TelegramBotAuthSession(Entity):
    """
    Telegram bot auth session domain model
    """

    id: str
    user_id: int | None = field(default=None, kw_only=True)
    jwt_token_id: UUID | None = field(default=None, kw_only=True)
    created_at: datetime | None = field(default=None, kw_only=True)
