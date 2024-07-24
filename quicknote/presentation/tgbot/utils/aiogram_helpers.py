from aiogram.types import TelegramObject, User


def extract_user_from_event(event: TelegramObject) -> User | None:
    try:
        if event.message:
            return event.message.from_user
        elif event.callback_query:
            return event.callback_query.from_user
    except Exception:
        return None
