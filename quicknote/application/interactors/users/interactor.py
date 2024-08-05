from uuid import uuid4, UUID

from quicknote.application.abstractions.repositories.users import IUsersRepository
from quicknote.application.interactors.users.dto import CreateOrUpdateUser
from quicknote.application.interactors.users.exceptions import UserNotFoundException
from quicknote.domain.entities.user import UserDM


class UserInteractor:
    def __init__(
        self,
        users_repo: IUsersRepository,
    ):
        self._users_repo = users_repo

    async def create_or_update_user(self, user_data: CreateOrUpdateUser):
        user_entity = UserDM(
            id=uuid4(),
            telegram_id=user_data.telegram_id,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        user = await self._users_repo.get_by_telegram_id(user_data.telegram_id)
        if user:
            user_entity.id = user.id
            await self._users_repo.update(user_entity)
        else:
            await self._users_repo.create(user_entity)

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserDM:
        user = await self._users_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise UserNotFoundException()
        return user

    async def get_user_by_id(self, user_id: UUID) -> UserDM:
        user = await self._users_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user
