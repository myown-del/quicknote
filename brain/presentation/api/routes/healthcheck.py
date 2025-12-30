from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from starlette.requests import Request


async def ping_pong(request: Request):
    return PlainTextResponse("pong")


def get_router() -> APIRouter:
    router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])
    router.add_route(
        path="/ping",
        endpoint=ping_pong,
        methods=["GET"],
    )
    return router
