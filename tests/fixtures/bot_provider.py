from unittest.mock import AsyncMock

from aiogram import Bot
from dishka import Provider, Scope, provide


class MockBotProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_bot(self) -> Bot:
        bot = AsyncMock(spec=Bot)
        return bot
