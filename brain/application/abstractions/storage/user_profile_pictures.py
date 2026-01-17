from abc import abstractmethod
from typing import Protocol


class IProfilePictureStorage(Protocol):
    @abstractmethod
    def upload(
        self,
        content: bytes,
        object_name: str,
        content_type: str | None = None,
    ) -> str:
        raise NotImplementedError
