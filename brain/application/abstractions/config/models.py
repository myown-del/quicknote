from typing import Protocol


class IDatabaseConfig(Protocol):
    @property
    def uri(self) -> str:
        raise NotImplementedError


class INeo4jConfig(Protocol):
    uri: str
    user: str
    password: str
    database: str
