from typing import AsyncIterable

from dishka import Provider, from_context, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from quicknote.application.abstractions.repositories.hub import IRepositoryHub
from quicknote.application.interactors.notes import NoteInteractor
from quicknote.application.interactors.users import UserInteractor
from quicknote.config import Config
from quicknote.infrastructure.db.connection import new_session_maker
from quicknote.infrastructure.db.repositories.hub import RepositoryHub


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    repository_hub = provide(RepositoryHub, scope=Scope.REQUEST, provides=IRepositoryHub)

    get_user_interactor = provide(UserInteractor, scope=Scope.REQUEST)
    get_note_interactor = provide(NoteInteractor, scope=Scope.REQUEST)
