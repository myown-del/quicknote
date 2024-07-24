from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


from datetime import datetime


def utcnow_wrapper() -> datetime:
    """
    Решает баг в adaptix
    """
    return datetime.utcnow()


class CreatedUpdatedMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow_wrapper
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=utcnow_wrapper
    )
