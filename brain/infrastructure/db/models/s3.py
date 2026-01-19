from uuid import UUID

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from brain.infrastructure.db.models.base import Base
from brain.infrastructure.db.models.mixins import CreatedUpdatedMixin


class S3FileDB(Base, CreatedUpdatedMixin):
    __tablename__ = "s3_files"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    object_name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    content_type: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
