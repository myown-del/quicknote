from sqlalchemy.ext.asyncio import AsyncSession

from quicknote.application.abstractions.repositories.hub import IRepositoryHub
from quicknote.application.abstractions.repositories.note import INoteRepository
from quicknote.application.abstractions.repositories.user import IUserRepository
from quicknote.infrastructure.db.repositories.notes import NotesRepository
from quicknote.infrastructure.db.repositories.users import UsersRepository


class RepositoryHub(IRepositoryHub):
    users: IUserRepository
    notes: INoteRepository

    def __init__(self, session: AsyncSession):
        self._session = session
        self.users: IUserRepository = UsersRepository(session)
        self.notes: INoteRepository = NotesRepository(session)
