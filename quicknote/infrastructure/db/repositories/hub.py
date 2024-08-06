from dataclasses import dataclass

from quicknote.application.abstractions.repositories.notes import INotesRepository
from quicknote.application.abstractions.repositories.users import IUsersRepository


@dataclass
class RepositoryHub:
    users: IUsersRepository
    notes: INotesRepository
