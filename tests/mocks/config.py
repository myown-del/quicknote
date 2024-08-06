from dataclasses import dataclass

from quicknote.application.abstractions.config.models import IDatabaseConfig


@dataclass
class DatabaseConfig(IDatabaseConfig):
    uri_: str

    @property
    def uri(self) -> str:
        return self.uri_
