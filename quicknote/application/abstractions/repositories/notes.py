from abc import ABC, abstractmethod
from uuid import UUID

from quicknote.application.abstractions.repositories.base import IBaseRepository
from quicknote.domain.entities.note import NoteDM


class INoteRepository(IBaseRepository, ABC):
    """
    Интерфейс репозитория заметок
    """

    @abstractmethod
    async def create(self, entity: NoteDM):
        """
        Создать заметку
        """

    @abstractmethod
    async def get_by_user_telegram_id(self, telegram_id: int) -> list[NoteDM]:
        """
        Получить заметки по идентификатору пользователя
        """

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> NoteDM:
        """
        Получить заметку по идентификатору
        """
