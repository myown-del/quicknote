from abc import ABC, abstractmethod
from typing import Protocol
from uuid import UUID

from quicknote.domain.entities.note import NoteDM


class INotesRepository(Protocol):
    """
    Интерфейс репозитория заметок
    """

    @abstractmethod
    async def create(self, entity: NoteDM):
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_telegram_id(self, telegram_id: int) -> list[NoteDM]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> NoteDM:
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self):
        raise NotImplementedError
