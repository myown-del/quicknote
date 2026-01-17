from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReadUserSchema(BaseModel):
    id: UUID
    telegram_id: int
    username: str | None
    first_name: str
    last_name: str | None
    created_at: datetime
    updated_at: datetime