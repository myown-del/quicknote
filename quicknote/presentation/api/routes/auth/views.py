from dataclasses import asdict

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, HTTPException, status, Depends

from quicknote.application.interactors.auth.exceptions import JwtTokenExpiredException
from quicknote.application.interactors.auth.interactor import AuthInteractor
from quicknote.application.interactors.users.exceptions import UserNotFoundException
from quicknote.config.models import AuthenticationConfig
from quicknote.domain.entities.user import UserDM
from quicknote.presentation.api.dependencies.auth import get_user_from_request
from quicknote.presentation.api.routes.auth.models import JwtTokenSchema, FakeAuthSchema


@inject
async def telegram_widget_auth(
    auth_interactor: FromDishka[AuthInteractor],
    request: Request,
):
    body = await request.json()
    valid_signature = await auth_interactor.check_auth_widget_hash(body)
    if not valid_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature",
        )

    telegram_id = body.get("id")
    try:
        token = await auth_interactor.login(telegram_id)
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
        user: UserDM = Depends(get_user_from_request),
):
    token = await auth_interactor.login(user.telegram_id)
    return JwtTokenSchema.model_validate(asdict(token))


def get_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["Authentication"])
    router.add_api_route(
        path="/tg-widget",
        endpoint=telegram_widget_auth,
        methods=["POST"],
        response_model=JwtTokenSchema
    )
    router.add_api_route(
        path="/fake",
        endpoint=fake_auth,
        methods=["POST"],
        response_model=JwtTokenSchema
    )
    router.add_api_route(
        path="/refresh-token",
        endpoint=refresh_token,
        methods=["POST"],
        response_model=JwtTokenSchema
    )
    return router
