from datetime import datetime

from pydantic import BaseModel


class JwtTokenResponse(BaseModel):
    access_token: str
    expires_at: datetime
