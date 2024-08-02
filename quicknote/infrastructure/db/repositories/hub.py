from sqlalchemy.ext.asyncio import AsyncSession

from quicknote.application.abstractions.repositories.hashtags import IHashtagsRepository
from quicknote.application.abstractions.repositories.hub import IRepositoryHub
from quicknote.application.abstractions.repositories.notes import INoteRepository
from quicknote.application.abstractions.repositories.users import IUserRepository
from quicknote.infrastructure.db.repositories.hashtags import HashtagsRepository
from quicknote.infrastructure.db.repositories.notes import NotesRepository
from quicknote.infrastructure.db.repositories.users import UsersRepository


class RepositoryHub(IRepositoryHub):
    users: IUserRepository
    notes: INoteRepository
    hashtags: IHashtagsRepository

    def __init__(self, session: AsyncSession):
        self._session = session
        self.users: IUserRepository = UsersRepository(session)
        self.notes: INoteRepository = NotesRepository(session)
        self.hashtags: IHashtagsRepository = HashtagsRepository(session)
