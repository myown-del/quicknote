from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from brain.domain.entities.common import Entity


@dataclass
class TelegramBotAuthSession(Entity):
    """
    Telegram bot auth session domain model
    """

    id: str
    telegram_id: int | None = field(default=None, kw_only=True)
    jwt_token_id: UUID | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.utcnow, kw_only=True)
