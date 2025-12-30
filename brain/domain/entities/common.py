from abc import ABC
from typing import TypeVar


class Entity(ABC):
    """
    Base class for all data model entities
    """

    pass


EntityT = TypeVar("EntityT", bound=Entity)
