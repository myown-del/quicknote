from abc import ABC, abstractmethod
from uuid import UUID

from quicknote.application.abstractions.repositories.base import IBaseRepository
from quicknote.domain.entities.note import HashtagDM


class IHashtagsRepository(IBaseRepository, ABC):
    @abstractmethod
    def create_hashtags(self, hashtags: list[HashtagDM]):
        raise NotImplementedError

    @abstractmethod
    def set_note_hashtags(self, note_id: UUID, hashtags: list[str]):
        raise NotImplementedError
