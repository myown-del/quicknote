from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReadNoteSchema(BaseModel):
    id: UUID
    title: str | None
    text: str | None
    created_at: datetime
    updated_at: datetime


class CreateNoteSchema(BaseModel):
    title: str | None = None
    text: str | None = None


class UpdateNoteSchema(BaseModel):
    title: str | None = None
    text: str | None = None
