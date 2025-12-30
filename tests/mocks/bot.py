from aiogram import Bot
from dishka import provide, Scope, Provider
from aiogram_tests.mocked_bot import MockedBot

from brain.config import Config


class MockBotProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_bot(self, config: Config) -> Bot:
        return MockedBot(token=config.bot.token)
