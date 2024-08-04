from enum import Enum

from pydantic.v1 import BaseSettings


class APIConfig(BaseSettings):
    auto_reload: bool = True
    workers: int = 1
    internal_host: str
    external_host: str
    tg_webhook_path: str
    port: int


class DatabaseConfig(BaseSettings):
    host: str
    port: int
    database: str
    user: str
    password: str

    @property
    def uri(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseSettings):
    host: str
    port: int
    db: int
    password: str

    @property
    def uri(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"


class BotConfig(BaseSettings):
    token: str


class EnvironmentType(Enum):
    DEVELOPMENT = "dev"
    TESTING = "test"
    PRODUCTION = "prod"


class AuthenticationConfig(BaseSettings):
    secret_key: str
    access_token_lifetime: int = 3600
    refresh_token_lifetime: int = 86400
    algorithm: str = "HS256"


class Config(BaseSettings):
    api: APIConfig
    auth: AuthenticationConfig
    db: DatabaseConfig
    redis: RedisConfig
    bot: BotConfig
    environment: EnvironmentType

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


def load_config(env_file=".env") -> Config:
    config = Config(_env_file=env_file)
    return config
