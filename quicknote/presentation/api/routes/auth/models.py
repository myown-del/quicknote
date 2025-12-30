from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JwtTokenchema(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str
    refresh_expires_at: datetime


class FakeAuthSchema(BaseModel):
    user_telegram_id: int
    admin_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TelegramBotAuthSessionSchema(BaseModel):
    id: str
    telegram_id: int | None
    jwt_token_id: UUID | None = None
    created_at: datetime
    jwt_token: JwtTokenchema | None = None
