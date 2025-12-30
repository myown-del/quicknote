from typing import TypeVar

from sqlalchemy.orm.decl_api import DeclarativeBase


class Base(DeclarativeBase):
    pass


SqlAlchemyModelT = TypeVar("SqlAlchemyModelT", bound=Base)
