from dataclasses import dataclass


@dataclass
class CreateNote:
    by_user_telegram_id: int
    text: str
