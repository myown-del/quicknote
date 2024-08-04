from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request, HTTPException, status

from quicknote.application.interactors.auth.exceptions import JwtTokenExpiredException
from quicknote.application.interactors.auth.interactor import AuthInteractor
from quicknote.application.interactors.users.exceptions import UserNotFoundException
from quicknote.presentation.api.routes.auth.models import JwtTokenResponse


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

    return JwtTokenResponse.model_validate(token)


@inject
async def refresh_token(
    auth_interactor: FromDishka[AuthInteractor],
    request: Request,
):
    raise NotImplementedError


def get_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["Authentication"])
    router.add_api_route(
        path="/tg-widget",
        endpoint=telegram_widget_auth,
        methods=["POST"],
    )
    return router
