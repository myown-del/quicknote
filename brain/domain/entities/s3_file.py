from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from brain.domain.entities.common import Entity


@dataclass
class S3File(Entity):
    """
    S3 file domain model
    """

    id: UUID | None = field(default=None, kw_only=True)
    object_name: str
    content_type: str | None = field(default=None, kw_only=True)
    created_at: datetime | None = field(default=None, kw_only=True)
    updated_at: datetime | None = field(default=None, kw_only=True)
