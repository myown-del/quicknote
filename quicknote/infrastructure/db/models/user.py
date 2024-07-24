from uuid import UUID

from sqlalchemy import Uuid, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from quicknote.infrastructure.db.models.base import Base
from quicknote.infrastructure.db.models.mixins import CreatedUpdatedMixin


class User(Base, CreatedUpdatedMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
