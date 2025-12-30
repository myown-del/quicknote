from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from quicknote.domain.entities.jwt_refresh_token import JwtRefreshToken


class IJwtRefreshTokensRepository(Protocol):
    @abstractmethod
    async def create(self, entity: JwtRefreshToken) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, token_id: UUID) -> JwtRefreshToken | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_token(self, token: str) -> JwtRefreshToken | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, token_id: UUID) -> None:
        raise NotImplementedError
