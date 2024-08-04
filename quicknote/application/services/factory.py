from dishka import Provider, Scope, provide

from quicknote.application.services.jwt import JwtService
from quicknote.config import Config


class ServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def get_jwt_service(self, config: Config) -> JwtService:
        return JwtService(
            secret_key=config.auth.secret_key,
            access_token_lifetime=config.auth.access_token_lifetime,
            algorithm=config.auth.algorithm,
        )
