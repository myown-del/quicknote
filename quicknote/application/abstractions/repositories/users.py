from abc import ABC, abstractmethod
from uuid import UUID

from quicknote.application.abstractions.repositories.base import IBaseRepository
from quicknote.domain.entities.user import UserDM


class IUserRepository(IBaseRepository, ABC):
    """
    Интерфейс репозитория пользователей
    """

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> UserDM | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity: UserDM) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: UserDM) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserDM | None:
        raise NotImplementedError
