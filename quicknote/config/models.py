from dataclasses import dataclass
from enum import Enum

from quicknote.application.abstractions.config.models import IDatabaseConfig


@dataclass
class APIConfig:
    internal_host: str
    external_host: str
    port: int
    tg_webhook_path: str
    auto_reload: bool = True
    workers: int = 1


@dataclass
class DatabaseConfig(IDatabaseConfig):
    host: str
    port: int
    database: str
    user: str
    password: str
    engine: str = "postgresql+asyncpg"

    @property
    def uri(self) -> str:
        return f"{self.engine}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int
    password: str

    @property
    def uri(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"


@dataclass
class BotConfig:
    token: str


class EnvironmentType(Enum):
    DEVELOPMENT = "dev"
    TESTING = "test"
    PRODUCTION = "prod"


@dataclass
class AuthenticationConfig:
    secret_key: str
    access_token_lifetime: int = 3600
    refresh_token_lifetime: int = 86400
    algorithm: str = "HS256"


@dataclass
class Config:
    api: APIConfig
    auth: AuthenticationConfig
    db: DatabaseConfig
    redis: RedisConfig
    bot: BotConfig
    environment: EnvironmentType
