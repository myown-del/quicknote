from abc import ABC

from quicknote.application.abstractions.repositories.note import INoteRepository
from quicknote.application.abstractions.repositories.user import IUserRepository


class IRepositoryHub(ABC):
    users: IUserRepository
    notes: INoteRepository
