from fastapi import FastAPI

from quicknote.config import Config
from quicknote.presentation.api.exceptions import register_exception_handlers
from quicknote.presentation.api.routes import register_routes


def create_bare_app(config: Config) -> FastAPI:
    app = FastAPI()

    register_routes(app=app, config=config)
    register_exception_handlers(app=app)

    return app
