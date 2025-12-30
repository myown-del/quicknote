from dataclasses import dataclass

from brain.application.abstractions.repositories.notes import INotesRepository
from brain.application.abstractions.repositories.keywords import IKeywordsRepository
from brain.application.abstractions.repositories.users import IUsersRepository


@dataclass
class RepositoryHub:
    users: IUsersRepository
    notes: INotesRepository
    keywords: IKeywordsRepository
