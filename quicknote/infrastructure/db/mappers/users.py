from quicknote.domain.entities.user import UserDM
from quicknote.infrastructure.db.models import User


def get_user_dm(user: User) -> UserDM:
    return UserDM(
        id=user.id,
        telegram_id=user.telegram_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def get_user_db(user_dm: UserDM) -> User:
    return User(
        id=user_dm.id,
        telegram_id=user_dm.telegram_id,
        username=user_dm.username,
        first_name=user_dm.first_name,
        last_name=user_dm.last_name,
        created_at=user_dm.created_at,
        updated_at=user_dm.updated_at,
    )
