from abc import ABC, abstractmethod

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
