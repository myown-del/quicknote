from dataclasses import dataclass

from brain.application.abstractions.repositories.notes import INotesRepository
from brain.application.abstractions.repositories.keywords import IKeywordsRepository
from brain.application.abstractions.repositories.users import IUsersRepository
from brain.application.abstractions.repositories.s3_files import (
    IS3FilesRepository,
)


@dataclass
class RepositoryHub:
    users: IUsersRepository
    s3_files: IS3FilesRepository
    notes: INotesRepository
    keywords: IKeywordsRepository
