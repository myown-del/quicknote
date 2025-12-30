from quicknote.domain.entities.telegram_bot_auth_session import TelegramBotAuthSession
from quicknote.infrastructure.db.models.telegram_bot_auth_session import (
    TelegramBotAuthSessionDB,
)


def map_telegram_bot_auth_session_to_dm(
    session: TelegramBotAuthSessionDB,
) -> TelegramBotAuthSession:
    return TelegramBotAuthSession(
        id=session.id,
        user_id=session.user_id,
        jwt_token_id=session.jwt_token_id,
        created_at=session.created_at,
    )


def map_telegram_bot_auth_session_to_db(
    session: TelegramBotAuthSession,
) -> TelegramBotAuthSessionDB:
    return TelegramBotAuthSessionDB(
        id=session.id,
        user_id=session.user_id,
        jwt_token_id=session.jwt_token_id,
        created_at=session.created_at,
    )
