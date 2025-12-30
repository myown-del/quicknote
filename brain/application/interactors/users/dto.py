from dataclasses import dataclass


@dataclass
class CreateOrUpdateUser:
    telegram_id: int
    username: str | None
    first_name: str
    last_name: str | None
