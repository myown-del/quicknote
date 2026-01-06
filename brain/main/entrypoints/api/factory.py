import logging
from functools import partial

from dishka import make_async_container, AsyncContainer
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI

from brain.config.provider import ConfigProvider, DatabaseConfigProvider
from brain.config.models import APIConfig, Config
from brain.config.parser import load_config
from brain.infrastructure.jwt.provider import JwtProvider
from brain.log import setup_logging
from brain.presentation.api.factory import create_bare_app
from brain.presentation.tgbot.provider import DispatcherProvider, BotProvider
from brain.infrastructure.db.provider import DatabaseProvider
from brain.infrastructure.graph.provider import Neo4jProvider
from brain.infrastructure.s3.provider import S3Provider
from brain.application.interactors.factory import InteractorProvider

logger = logging.getLogger(__name__)


async def on_startup(container: AsyncContainer, config: APIConfig):
    logger.info("Startup complete")
    

def create_app() -> FastAPI:
    setup_logging()

    config = load_config(
        config_class=Config,
        env_file_path=".env"
    )
    app = create_bare_app(config=config.api)
    container = make_async_container(
        ConfigProvider(),
        BotProvider(),
        DatabaseConfigProvider(),
        DatabaseProvider(),
        Neo4jProvider(),
        S3Provider(),
        InteractorProvider(),
        JwtProvider(),
        DispatcherProvider(),
        context={Config: config}
    )

    fastapi_integration.setup_dishka(container=container, app=app)

    setup = partial(on_startup, container, config.api)
    app.add_event_handler("startup", setup)

    return app
