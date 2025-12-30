from fastapi import FastAPI

from brain.config.models import APIConfig
from brain.presentation.api import middlewares
from brain.presentation.api.exceptions import register_exception_handlers
from brain.presentation.api.routes import register_routes


def create_bare_app(config: APIConfig) -> FastAPI:
    app = FastAPI()

    app.middleware("http")(middlewares.access_log_middleware)

    register_routes(app=app, config=config)
    register_exception_handlers(app=app)

    return app
