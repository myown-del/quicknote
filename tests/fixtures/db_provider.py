from dishka import Provider, Scope, provide

from quicknote.application.abstractions.repositories.notes import INotesRepository
from quicknote.application.abstractions.repositories.users import IUsersRepository
from tests.mocks.db.repositories.notes import NotesRepositoryMock
from tests.mocks.db.repositories.users import UsersRepositoryMock


class DbProvider(Provider):
    scope = Scope.APP

    users_repository = provide(
        UsersRepositoryMock, scope=Scope.REQUEST, provides=IUsersRepository
    )
    notes_repository = provide(
        NotesRepositoryMock, scope=Scope.REQUEST, provides=INotesRepository
    )
