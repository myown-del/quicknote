import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import SimpleEventIsolation, MemoryStorage
from dishka import Provider, Scope, AsyncContainer, provide
from dishka.integrations.aiogram import setup_dishka

from quicknote.config import Config
from quicknote.presentation.tgbot.handlers import register_handlers
from quicknote.presentation.tgbot.middlewares import register_middlewares

logger = logging.getLogger(__name__)


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_bot(self, config: Config) -> Bot:
        bot = Bot(
            token=config.bot.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML, allow_sending_without_reply=True
            ),
        )
        return bot


class DispatcherProvider(Provider):
    scope = Scope.APP

    @provide
    def create_dispatcher(
        self,
        container: AsyncContainer,
    ) -> Dispatcher:
        dp = Dispatcher(
            storage=MemoryStorage(),
            events_isolation=SimpleEventIsolation(),
        )
        setup_dishka(container=container, router=dp)
        register_handlers(dp)
        register_middlewares(dp)
        return dp
