from fastapi import FastAPI

from quicknote.config import Config
from .healthcheck import get_router as get_healthcheck_router
from .tgbot import get_router as get_tgbot_router
from .test import router as test_router


def register_routes(app: FastAPI, config: Config):
    app.include_router(get_tgbot_router(config))
    app.include_router(get_healthcheck_router())
    app.include_router(test_router)
