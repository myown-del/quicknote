from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateNote:
    by_user_telegram_id: int
    title: str | None
    text: str | None
    represents_keyword: bool = False


@dataclass
class UpdateNote:
    note_id: UUID
    title: str | None
    text: str | None
    represents_keyword: bool | None = None

