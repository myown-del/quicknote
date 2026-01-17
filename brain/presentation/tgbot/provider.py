import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from dishka import Provider, Scope, AsyncContainer, provide
from dishka.integrations.aiogram import setup_dishka

from brain.config.models import RedisConfig
from brain.presentation.tgbot.bot_provider import BotProvider
from brain.presentation.tgbot.dialogs import register_dialogs
from brain.presentation.tgbot.handlers import register_handlers
from brain.presentation.tgbot.middlewares import register_middlewares

logger = logging.getLogger(__name__)


class DispatcherProvider(Provider):
    scope = Scope.APP

    @provide
    def create_dispatcher(
        self,
        container: AsyncContainer,
        redis_config: RedisConfig,
    ) -> Dispatcher:
        storage = RedisStorage.from_url(redis_config.uri)
        storage.key_builder = DefaultKeyBuilder(with_destiny=True)
        dp = Dispatcher(
            storage=storage,
            events_isolation=SimpleEventIsolation(),
        )
        setup_dishka(container=container, router=dp)
        setup_dialogs(dp)

        register_handlers(dp)
        register_dialogs(dp)
        register_middlewares(dp)

        return dp
