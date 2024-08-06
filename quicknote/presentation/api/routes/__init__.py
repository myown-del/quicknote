from fastapi import FastAPI

from quicknote.config.models import APIConfig
from .healthcheck import get_router as get_healthcheck_router
from .tgbot import get_router as get_tgbot_router
from .auth import get_router as get_auth_router
from .test import router as test_router


def register_routes(app: FastAPI, config: APIConfig):
    app.include_router(get_tgbot_router(config))
    app.include_router(get_healthcheck_router())
    app.include_router(get_auth_router())
    app.include_router(test_router)
