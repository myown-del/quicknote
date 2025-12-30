from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from quicknote.domain.entities.jwt import FullJwtToken
from quicknote.domain.entities.tg_bot_auth import TelegramBotAuthSession


@dataclass
class JwtTokenCreationPayload:
    user_id: UUID


@dataclass
class DecodedJwtTokenPayload:
    user_id: UUID
    exp: datetime


@dataclass
class TelegramBotAuthSessionTokens:
    session: TelegramBotAuthSession
    tokens: FullJwtToken | None
