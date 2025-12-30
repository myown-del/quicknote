from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, HTTPException, status, Query

from quicknote.application.interactors.auth.exceptions import (
    JwtTokenExpiredException,
    JwtTokenInvalidException,
    TelegramBotAuthSessionNotFoundException,
)
from quicknote.application.interactors.auth.interactor import AuthInteractor
from quicknote.application.interactors.auth.session_interactor import (
    TelegramBotAuthSessionInteractor,
)
from quicknote.application.interactors.users.exceptions import UserNotFoundException
from quicknote.config.models import AuthenticationConfig
from quicknote.presentation.api.routes.auth.models import (
    JwtTokenSchema,
    FakeAuthSchema,
    RefreshTokenSchema,
    TelegramBotAuthSessionSchema,
)


@inject
async def fake_auth(
        auth_interactor: FromDishka[AuthInteractor],
        auth_config: FromDishka[AuthenticationConfig],
        body: FakeAuthSchema,
):
    if body.admin_token != auth_config.admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    try:
        token = await auth_interactor.login(body.user_telegram_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except JwtTokenExpiredException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )

    return JwtTokenSchema.model_validate(asdict(token))


@inject
async def refresh_token(
        auth_interactor: FromDishka[AuthInteractor],
        body: RefreshTokenSchema,
):
    try:
        token = await auth_interactor.refresh_tokens(body.refresh_token)
    except JwtTokenExpiredException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except JwtTokenInvalidException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return JwtTokenSchema.model_validate(asdict(token))


@inject
async def create_tg_bot_auth_session(
    interactor: FromDishka[TelegramBotAuthSessionInteractor],
):
    session = await interactor.create_session()
    return TelegramBotAuthSessionSchema.model_validate(asdict(session))


@inject
async def get_tg_bot_auth_session(
    interactor: FromDishka[TelegramBotAuthSessionInteractor],
    session_id: str = Query(..., alias="id"),
):
    try:
        session, tokens = await interactor.get_session_with_tokens(
            session_id=session_id
        )
    except TelegramBotAuthSessionNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    payload = asdict(session)
    if tokens:
        payload["jwt_token"] = JwtTokenSchema.model_validate(asdict(tokens))
    return TelegramBotAuthSessionSchema.model_validate(payload)


def get_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["Authentication"])
    router.add_api_route(
        path="/fake",
        endpoint=fake_auth,
        methods=["POST"],
        response_model=JwtTokenSchema
    )
    router.add_api_route(
        path="/tokens/refresh",
        endpoint=refresh_token,
        methods=["POST"],
        response_model=JwtTokenSchema
    )
    router.add_api_route(
        path="/tg-bot/session",
        endpoint=create_tg_bot_auth_session,
        methods=["POST"],
        response_model=TelegramBotAuthSessionSchema,
        status_code=status.HTTP_201_CREATED,
    )
    router.add_api_route(
        path="/tg-bot/session",
        endpoint=get_tg_bot_auth_session,
        methods=["GET"],
        response_model=TelegramBotAuthSessionSchema,
        status_code=status.HTTP_200_OK,
    )
    return router
