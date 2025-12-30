from brain.domain.entities.jwt import JwtRefreshToken
from brain.infrastructure.db.models.jwt import JwtRefreshTokenDB


def map_jwt_refresh_token_to_dm(token: JwtRefreshTokenDB) -> JwtRefreshToken:
    return JwtRefreshToken(
        id=token.id,
        user_id=token.user_id,
        token=token.token,
        expires_at=token.expires_at,
        created_at=token.created_at,
    )


def map_jwt_refresh_token_to_db(token: JwtRefreshToken) -> JwtRefreshTokenDB:
    return JwtRefreshTokenDB(
        id=token.id,
        user_id=token.user_id,
        token=token.token,
        expires_at=token.expires_at,
        created_at=token.created_at,
    )
