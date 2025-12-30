from dataclasses import dataclass

from quicknote.application.abstractions.config.models import IDatabaseConfig, INeo4jConfig


@dataclass
class DatabaseConfig(IDatabaseConfig):
    uri_: str

    @property
    def uri(self) -> str:
        return self.uri_


@dataclass
class Neo4jConfig(INeo4jConfig):
    uri: str
    user: str
    password: str
    database: str
