from dataclasses import dataclass
from datetime import datetime


@dataclass
class JwtToken:
    access_token: str
    expires_at: datetime
