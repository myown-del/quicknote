from typing import Protocol

from quicknote.domain.entities.jwt import JwtToken


class TokenExpiredError(Exception):
    pass


class TokenInvalidError(Exception):
    pass


class TokenVerifier(Protocol):
    def create_token(self, payload: dict) -> JwtToken:
        ...

    def decode_token(self, token: str) -> dict:
        ...
