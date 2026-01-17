import pytest
from dishka import AsyncContainer

from brain.application.abstractions.repositories.jwt import IJwtRefreshTokensRepository
from brain.application.interactors.auth.exceptions import (
    TelegramBotAuthSessionNotFoundException,
)
from brain.application.interactors.auth.session_interactor import (
    TelegramBotAuthSessionInteractor,
)
from brain.domain.entities.user import User


@pytest.mark.asyncio
async def test_create_session_persists_empty_session(
    dishka_request: AsyncContainer,
):
    # setup: resolve session interactor
    session_interactor = await dishka_request.get(TelegramBotAuthSessionInteractor)

    # action: create a new auth session
    session = await session_interactor.create_session()

    # check: session can be fetched and is empty
    fetched = await session_interactor.get_session(session.id)
    assert len(session.id) == 16
    assert fetched.id == session.id
    assert fetched.telegram_id is None


@pytest.mark.asyncio
async def test_get_session_with_tokens_returns_none_for_empty_session(
    dishka_request: AsyncContainer,
):
    # setup: resolve session interactor
    session_interactor = await dishka_request.get(TelegramBotAuthSessionInteractor)

    # action: create a new session and request tokens
    session = await session_interactor.create_session()
    session_tokens = await session_interactor.get_session_with_tokens(session.id)

    # check: tokens are missing for empty session
    assert session_tokens.session.id == session.id
    assert session_tokens.tokens is None


@pytest.mark.asyncio
async def test_get_session_raises_for_missing_id(
    dishka_request: AsyncContainer,
):
    # setup: resolve session interactor
    session_interactor = await dishka_request.get(TelegramBotAuthSessionInteractor)

    # action: prepare missing session id
    session_id = "missing-session-id"

    # check: missing session raises an error
    with pytest.raises(TelegramBotAuthSessionNotFoundException):
        await session_interactor.get_session(session_id)


@pytest.mark.asyncio
async def test_attach_user_to_session_issues_tokens(
    dishka_request: AsyncContainer,
    user: User,
):
    # setup: resolve interactor and repo
    session_interactor = await dishka_request.get(TelegramBotAuthSessionInteractor)
    jwt_repo = await dishka_request.get(IJwtRefreshTokensRepository)
    session = await session_interactor.create_session()

    # action: attach user and fetch tokens
    attached = await session_interactor.attach_user_to_session(
        session_id=session.id,
        telegram_id=user.telegram_id,
    )
    session_tokens = await session_interactor.get_session_with_tokens(session.id)

    # check: session is attached and refresh token is stored
    assert attached is True
    assert session_tokens.tokens is not None
    stored = await jwt_repo.get_by_token(session_tokens.tokens.refresh_token)
    assert stored is not None

    await jwt_repo.delete_by_id(stored.id)
