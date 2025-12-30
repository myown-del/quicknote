from datetime import datetime

from pydantic import BaseModel


class JwtTokenSchema(BaseModel):
    access_token: str
    expires_at: datetime


class FakeAuthSchema(BaseModel):
    user_telegram_id: int
    admin_token: str
