from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from quicknote.application.abstractions.repositories.notes import INotesRepository
from quicknote.application.abstractions.repositories.users import IUsersRepository
from quicknote.config import Config
from quicknote.infrastructure.db.connection import new_session_maker
from quicknote.infrastructure.db.repositories.notes import NotesRepository
from quicknote.infrastructure.db.repositories.users import UsersRepository


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    users_repository = provide(
        UsersRepository, scope=Scope.REQUEST, provides=IUsersRepository
    )
    notes_repository = provide(
        NotesRepository, scope=Scope.REQUEST, provides=INotesRepository
    )
