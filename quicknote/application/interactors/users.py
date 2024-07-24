from datetime import datetime
from uuid import uuid4

from quicknote.application.abstractions.repositories.hub import IRepositoryHub
from quicknote.application.interactors.dto import CreateOrUpdateUser
from quicknote.domain.entities.user import UserDM


class UserInteractor:
    def __init__(
        self,
        repo_hub: IRepositoryHub,
    ):
        self._repo_hub = repo_hub

    async def create_or_update_user(self, user: CreateOrUpdateUser):
        user_entity = UserDM(
            id=uuid4(),
            telegram_id=user.telegram_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        user = await self._repo_hub.users.get_by_telegram_id(user.telegram_id)
        if user:
            user_entity.id = user.id
            await self._repo_hub.users.update(user_entity)
        else:
            await self._repo_hub.users.create(user_entity)
