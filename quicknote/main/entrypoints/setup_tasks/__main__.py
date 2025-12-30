import asyncio
import logging

from dishka import make_async_container, AsyncContainer
from aiogram import Bot

from quicknote.config.provider import ConfigProvider, DatabaseConfigProvider
from quicknote.config.models import Config
from quicknote.config.parser import load_config
from quicknote.infrastructure.jwt.provider import JwtProvider
from quicknote.log import setup_logging
from quicknote.presentation.tgbot.provider import DispatcherProvider, BotProvider
from quicknote.infrastructure.db.provider import DatabaseProvider
from quicknote.infrastructure.graph.provider import Neo4jProvider
from quicknote.application.interactors.factory import InteractorProvider

logger = logging.getLogger(__name__)


async def setup_tasks(container: AsyncContainer, config: Config):
    webhook_url = config.external_host + config.tg_webhook_path

    bot = await container.get(Bot)
    await bot.set_webhook(
        url=webhook_url
    )
    logger.info(f"Binded telegram webhooks to url: {webhook_url}")


async def main():
    setup_logging()

    config = load_config(
        config_class=Config,
        env_file_path=".env"
    )
    container = make_async_container(
        ConfigProvider(),
        BotProvider(),
        DatabaseConfigProvider(),
        DatabaseProvider(),
        Neo4jProvider(),
        InteractorProvider(),
        JwtProvider(),
        DispatcherProvider(),
        context={Config: config}
    )

    await setup_tasks(container)
    logger.info("Tasks setup complete")


if __name__ == "__main__":
    asyncio.run(main())