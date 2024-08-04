from datetime import datetime, timedelta

import jwt

from quicknote.domain.entities.jwt import JwtToken


class JwtService:
    def __init__(
        self,
        secret_key: str,
        access_token_lifetime: int,
        algorithm: str,
    ):
        self._secret_key = secret_key
        self._access_token_lifetime = access_token_lifetime
        self._algorithm = algorithm

    def create_token(self, payload: dict) -> JwtToken:
        expires_at = payload.get("exp")
        if expires_at is None:
            expires_at = datetime.utcnow() + timedelta(
                seconds=self._access_token_lifetime
            )
            payload["exp"] = expires_at

        encoded_jwt = jwt.encode(
            payload=payload, key=self._secret_key, algorithm=self._algorithm
        )
        return JwtToken(access_token=encoded_jwt, expires_at=expires_at)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(jwt=token, key=self._secret_key, algorithms=[self._algorithm])
