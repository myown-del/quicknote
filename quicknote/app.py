import logging
from functools import partial

from aiogram import Bot
from dishka import make_async_container, AsyncContainer
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI

from quicknote.application.services.factory import ServiceProvider
from quicknote.config.di import ConfigProvider, DatabaseConfigProvider
from quicknote.config.models import APIConfig, Config
from quicknote.config.parser import load_config
from quicknote.log import setup_logging
from quicknote.presentation.api.factory import create_bare_app
from quicknote.presentation.tgbot.factory import DispatcherProvider, BotProvider
from quicknote.infrastructure.db.factory import DatabaseProvider
from quicknote.application.interactors.factory import InteractorProvider

logger = logging.getLogger(__name__)


async def on_startup(container: AsyncContainer, config: APIConfig):
    webhook_url = config.external_host + config.tg_webhook_path

    # bot = await container.get(Bot)
    # await bot.set_webhook(
    #     url=webhook_url
    # )
    logger.info(f"Binded telegram webhooks to url: {webhook_url}")


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
        InteractorProvider(),
        ServiceProvider(),
        DispatcherProvider(),
        context={Config: config}
    )

    fastapi_integration.setup_dishka(container=container, app=app)

    setup = partial(on_startup, container, config.api)
    app.add_event_handler("startup", setup)

    return app
