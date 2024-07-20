from fastapi import FastAPI

from quicknote.log import setup_logging


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI()
    return app
