from abc import abstractmethod
from typing import Protocol

from uuid import UUID

from quicknote.domain.entities.telegram_bot_auth_session import TelegramBotAuthSession


class ITelegramBotAuthSessionsRepository(Protocol):
    @abstractmethod
    async def create(self, entity: TelegramBotAuthSession) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, session_id: str) -> TelegramBotAuthSession | None:
        raise NotImplementedError

    @abstractmethod
    async def attach_user_if_empty(
        self,
        session_id: str,
        telegram_id: int,
        jwt_token_id: UUID,
    ) -> bool:
        raise NotImplementedError
