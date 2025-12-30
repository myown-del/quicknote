from dataclasses import dataclass
from datetime import datetime


@dataclass
class JwtToken:
    access_token: str
    expires_at: datetime


@dataclass
class JwtTokens:
    access_token: str
    expires_at: datetime
    refresh_token: str
    refresh_expires_at: datetime
