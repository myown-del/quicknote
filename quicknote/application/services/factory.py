from dishka import Provider, Scope, provide

from quicknote.application.services.jwt import JwtService
from quicknote.config.models import AuthenticationConfig


class ServiceProvider(Provider):
    scope = Scope.APP

    @provide
    def get_jwt_service(self, config: AuthenticationConfig) -> JwtService:
        return JwtService(
            secret_key=config.secret_key,
            access_token_lifetime=config.access_token_lifetime,
            algorithm=config.algorithm,
        )
