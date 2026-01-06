from dishka import Provider, Scope, provide, from_context

from brain.application.abstractions.config.models import IDatabaseConfig, INeo4jConfig
from brain.config.models import APIConfig, Config, BotConfig, AuthenticationConfig, RedisConfig, S3Config


class ConfigProvider(Provider):
    scope = Scope.APP
    config = from_context(provides=Config, scope=Scope.APP)

    @provide
    def get_api_config(self, config: Config) -> APIConfig:
        return config.api

    @provide
    def get_s3_config(self, config: Config) -> S3Config:
        return config.s3

    @provide
    def get_bot_config(self, config: Config) -> BotConfig:
        return config.bot

    @provide
    def get_auth_config(self, config: Config) -> AuthenticationConfig:
        return config.auth


class DatabaseConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_config(self, config: Config) -> IDatabaseConfig:
        return config.db

    @provide
    def get_neo4j_config(self, config: Config) -> INeo4jConfig:
        return config.neo4j

    @provide
    def get_redis_config(self, config: Config) -> RedisConfig:
        return config.redis
