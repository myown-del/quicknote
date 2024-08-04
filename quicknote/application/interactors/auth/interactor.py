from dataclasses import asdict
from datetime import datetime

from quicknote.application.abstractions.repositories.hub import IRepositoryHub
from quicknote.application.interactors import UserInteractor
from quicknote.application.interactors.auth.dto import (
    JwtTokenCreationPayload,
    DecodedJwtTokenPayload,
)
from quicknote.application.interactors.auth.exceptions import JwtTokenExpiredException
from quicknote.application.services.jwt import JwtService
from quicknote.config import Config
from aiogram.utils.auth_widget import check_signature as check_widget_auth_signature

from quicknote.domain.entities.jwt import JwtToken
from quicknote.domain.entities.user import UserDM


class AuthInteractor:
    def __init__(
        self,
        repo_hub: IRepositoryHub,
        user_interactor: UserInteractor,
        config: Config,
        jwt_service: JwtService,
    ):
        self._repo_hub = repo_hub
        self._user_interactor = user_interactor
        self._config = config
        self._jwt_service = jwt_service

    async def check_auth_widget_hash(self, body: dict) -> bool:
        return check_widget_auth_signature(
            token=self._config.bot.token, hash=str(body.get("hash")), **body
        )

    def _create_jwt_token(
        self,
        payload: JwtTokenCreationPayload,
    ) -> JwtToken:
        return self._jwt_service.create_token(payload=asdict(payload))

    def _decode_jwt_token(self, token: str) -> DecodedJwtTokenPayload:
        data = self._jwt_service.decode_token(token)
        jwt_token_payload = DecodedJwtTokenPayload(**data)
        return jwt_token_payload

    async def login(self, telegram_id: int) -> JwtToken:
        user = await self._user_interactor.get_user_by_telegram_id(telegram_id)
        return self._create_jwt_token(payload=JwtTokenCreationPayload(user_id=user.id))

    async def authorize_by_token(self, token: str) -> UserDM:
        payload = self._decode_jwt_token(token)

        if payload.expires_at < datetime.utcnow():
            raise JwtTokenExpiredException()

        user = await self._user_interactor.get_user_by_id(payload.user_id)
        return user