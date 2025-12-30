from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class IKeywordsRepository(Protocol):
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
    async def delete_note_keywords(self, note_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_unused_keywords(self, user_id: UUID, names: list[str]) -> None:
        raise NotImplementedError
