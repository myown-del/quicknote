from typing import Protocol


class IDatabaseConfig(Protocol):
    @property
    def uri(self) -> str:
        raise NotImplementedError
