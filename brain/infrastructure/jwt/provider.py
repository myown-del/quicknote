from dishka import Provider, Scope, provide

from brain.application.abstractions.token_verifier import TokenVerifier
from brain.config.models import AuthenticationConfig
from brain.infrastructure.jwt.service import JwtService


class JwtProvider(Provider):
    scope = Scope.APP

    @provide
    def get_token_verifier(self, config: AuthenticationConfig) -> TokenVerifier:
        return JwtService(
            secret_key=config.secret_key,
            access_token_lifetime=config.access_token_lifetime,
            algorithm=config.algorithm,
        )
