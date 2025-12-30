from dataclasses import asdict
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from quicknote.application.interactors.users.interactor import UserInteractor
from quicknote.application.interactors.auth.dto import (
    JwtTokenCreationPayload,
    DecodedJwtTokenPayload,
)
from quicknote.application.interactors.auth.exceptions import JwtTokenExpiredException, JwtTokenInvalidException
from quicknote.application.abstractions.token_verifier import (
    TokenVerifier,
    TokenExpiredError,
    TokenInvalidError,
)
from quicknote.application.abstractions.repositories.jwt import (
    IJwtRefreshTokensRepository,
)

from quicknote.config.models import BotConfig, AuthenticationConfig
from quicknote.domain.entities.jwt import JwtToken, JwtTokens, JwtRefreshToken
from quicknote.domain.entities.user import User


class AuthInteractor:
    def __init__(
        self,
        user_interactor: UserInteractor,
        bot_config: BotConfig,
        auth_config: AuthenticationConfig,
        jwt_service: TokenVerifier,
        jwt_repo: IJwtRefreshTokensRepository,
    ):
        self._user_interactor = user_interactor
        self._bot_config = bot_config
        self._auth_config = auth_config
        self._jwt_service = jwt_service
        self._jwt_repo = jwt_repo

    def _create_jwt_token(
        self,
        payload: JwtTokenCreationPayload,
    ) -> JwtToken:
        return self._jwt_service.create_token(
            payload=asdict(payload)
        )

    def _create_access_token_for_user(self, user_id: UUID) -> JwtToken:
        return self._create_jwt_token(
            payload=JwtTokenCreationPayload(
                user_id=user_id
            )
        )

    async def _create_refresh_token_for_user(self, user_id: UUID) -> JwtRefreshToken:
        refresh_expires_at = datetime.utcnow() + timedelta(
            seconds=self._auth_config.refresh_token_lifetime
        )
        refresh_jwt = self._jwt_service.create_token(
            payload={
                "user_id": user_id,
                "exp": refresh_expires_at,
            }
        )
        refresh_token = JwtRefreshToken(
            id=uuid4(),
            user_id=user_id,
            token=refresh_jwt.access_token,
            expires_at=refresh_expires_at,
            created_at=datetime.utcnow(),
        )
        await self._jwt_repo.create(refresh_token)
        return refresh_token

    def _decode_jwt_token(self, token: str) -> DecodedJwtTokenPayload:
        try:
            data = self._jwt_service.decode_token(token)
        except TokenExpiredError:
            raise JwtTokenExpiredException()
        except TokenInvalidError:
            raise JwtTokenInvalidException()

        jwt_token_payload = DecodedJwtTokenPayload(**data)
        return jwt_token_payload

    async def _issue_tokens_for_user_id(self, user_id: UUID) -> tuple[JwtTokens, UUID]:
        access_token = self._create_access_token_for_user(user_id)
        refresh_token = await self._create_refresh_token_for_user(user_id)
        return (
            JwtTokens(
                access_token=access_token.access_token,
                expires_at=access_token.expires_at,
                refresh_token=refresh_token.token,
                refresh_expires_at=refresh_token.expires_at,
            ),
            refresh_token.id,
        )

    async def issue_tokens_for_telegram_id(self, telegram_id: int) -> tuple[JwtTokens, UUID]:
        user = await self._user_interactor.get_user_by_telegram_id(telegram_id)
        return await self._issue_tokens_for_user_id(user.id)

    async def login(self, telegram_id: int) -> JwtTokens:
        tokens, _ = await self.issue_tokens_for_telegram_id(telegram_id)
        return tokens

    async def refresh_tokens(self, refresh_token: str) -> JwtTokens:
        payload = self._decode_jwt_token(refresh_token)
        token_record = await self._jwt_repo.get_by_token(refresh_token)
        if not token_record:
            raise JwtTokenInvalidException()
        if token_record.expires_at < datetime.utcnow():
            raise JwtTokenExpiredException()
        if token_record.user_id != payload.user_id:
            raise JwtTokenInvalidException()

        await self._jwt_repo.delete_by_id(token_record.id)
        tokens, _ = await self._issue_tokens_for_user_id(token_record.user_id)
        return tokens

    async def revoke_refresh_token(self, token_id: UUID) -> None:
        await self._jwt_repo.delete_by_id(token_id)

    async def get_refresh_token(self, token_id: UUID) -> JwtRefreshToken | None:
        return await self._jwt_repo.get_by_id(token_id)

    def create_access_token_for_user(self, user_id: UUID) -> JwtToken:
        return self._create_access_token_for_user(user_id)

    async def authorize_by_token(self, token: str) -> User:
        payload = self._decode_jwt_token(token)
        user = await self._user_interactor.get_user_by_id(payload.user_id)
        return user
