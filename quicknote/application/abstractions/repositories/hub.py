from abc import ABC

from quicknote.application.abstractions.repositories.hashtags import IHashtagsRepository
from quicknote.application.abstractions.repositories.notes import INoteRepository
from quicknote.application.abstractions.repositories.users import IUserRepository


class IRepositoryHub(ABC):
    users: IUserRepository
    notes: INoteRepository
    hashtags: IHashtagsRepository
