from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from quicknote.application.abstractions.repositories.notes import INotesRepository
from quicknote.application.abstractions.repositories.users import IUsersRepository
from quicknote.application.abstractions.config.models import IDatabaseConfig
from quicknote.infrastructure.db.connection import create_engine, create_session_maker
from quicknote.infrastructure.db.repositories.notes import NotesRepository
from quicknote.infrastructure.db.repositories.users import UsersRepository


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_engine(self, config: IDatabaseConfig) -> AsyncIterable[AsyncEngine]:
        engine = create_engine(config)
        yield engine
        # await engine.dispose(True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session

    users_repository = provide(
        UsersRepository, scope=Scope.REQUEST, provides=IUsersRepository
    )
    notes_repository = provide(
        NotesRepository, scope=Scope.REQUEST, provides=INotesRepository
    )
