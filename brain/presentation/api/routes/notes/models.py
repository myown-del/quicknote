from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReadNoteSchema(BaseModel):
    id: UUID
    title: str | None
    text: str | None
    represents_keyword: bool
    created_at: datetime
    updated_at: datetime


class CreateNoteSchema(BaseModel):
    title: str | None = None
    text: str | None = None
    represents_keyword: bool = False


class UpdateNoteSchema(BaseModel):
    title: str | None = None
    text: str | None = None
    represents_keyword: bool | None = None


class WikilinkSuggestionSchema(BaseModel):
    title: str
    represents_keyword: bool
