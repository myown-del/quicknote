from brain.domain.entities.user import User
from brain.infrastructure.db.models.user import UserDB


def map_user_to_dm(user: UserDB) -> User:
    return User(
        id=user.id,    
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def map_user_to_db(user: User) -> UserDB:
    return UserDB(
        id=user.id,
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )