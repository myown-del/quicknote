from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class JwtTokenCreationPayload:
    user_id: UUID


@dataclass
class DecodedJwtTokenPayload:
    user_id: UUID
    exp: datetime
