from datetime import datetime
from uuid import uuid4

from quicknote.application.abstractions.repositories.tg_bot_auth import (
    ITelegramBotAuthSessionsRepository,
)
from quicknote.application.interactors.auth.exceptions import (
    TelegramBotAuthSessionNotFoundException,
)
from quicknote.application.interactors.auth.interactor import AuthInteractor
from quicknote.domain.entities.jwt import JwtTokens
from quicknote.domain.entities.telegram_bot_auth_session import TelegramBotAuthSession


class TelegramBotAuthSessionInteractor:
    def __init__(
        self,
        sessions_repo: ITelegramBotAuthSessionsRepository,
        auth_interactor: AuthInteractor,
    ):
        self._sessions_repo = sessions_repo
        self._auth_interactor = auth_interactor

    def _generate_session_id(self) -> str:
        return uuid4().hex[:16]

    async def create_session(self) -> TelegramBotAuthSession:
        session_id = self._generate_session_id()
        for _ in range(5):
            existing = await self._sessions_repo.get_by_id(session_id)
            if not existing:
                session = TelegramBotAuthSession(
                    id=session_id,
                    user_id=None,
                    created_at=datetime.utcnow(),
                )
                await self._sessions_repo.create(session)
                return session
            session_id = self._generate_session_id()

        session = TelegramBotAuthSession(
            id=session_id,
            user_id=None,
            created_at=datetime.utcnow(),
        )
        await self._sessions_repo.create(session)
        return session

    async def get_session(self, session_id: str) -> TelegramBotAuthSession:
        session = await self._sessions_repo.get_by_id(session_id)
        if not session:
            raise TelegramBotAuthSessionNotFoundException()
        return session

    async def attach_user_to_session(self, session_id: str, telegram_id: int) -> bool:
        _, refresh_token_id = await self._auth_interactor.issue_tokens_for_telegram_id(
            telegram_id
        )
        updated = await self._sessions_repo.attach_user_if_empty(
            session_id=session_id,
            telegram_id=telegram_id,
            jwt_token_id=refresh_token_id,
        )
        if not updated:
            await self._auth_interactor.revoke_refresh_token(refresh_token_id)
        return updated

    async def get_session_with_tokens(
        self, session_id: str
    ) -> tuple[TelegramBotAuthSession, JwtTokens | None]:
        session = await self.get_session(session_id)
        if not session.jwt_token_id:
            return session, None

        refresh_token = await self._auth_interactor.get_refresh_token(session.jwt_token_id)
        if not refresh_token:
            return session, None
        if refresh_token.expires_at < datetime.utcnow():
            return session, None

        access_token = self._auth_interactor.create_access_token_for_user(
            refresh_token.user_id
        )
        tokens = JwtTokens(
            access_token=access_token.access_token,
            expires_at=access_token.expires_at,
            refresh_token=refresh_token.token,
            refresh_expires_at=refresh_token.expires_at,
        )
        return session, tokens
