from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from brain.domain.entities.keyword import Keyword


class IKeywordsRepository(Protocol):
    @abstractmethod
    async def get_by_id(self, keyword_id: UUID) -> Keyword | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_and_name(self, user_id: UUID, name: str) -> Keyword | None:
        raise NotImplementedError

    @abstractmethod
    async def ensure_keywords(self, user_id: UUID, names: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def replace_note_keywords(
        self,
        note_id: UUID,
        user_id: UUID,
        names: list[str],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_note_keyword_names(self, note_id: UUID) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    async def delete_note_keywords(self, note_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_unused_keywords(self, user_id: UUID, names: list[str]) -> None:
        raise NotImplementedError
