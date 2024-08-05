import pytest
from dishka import AsyncContainer

from quicknote.application.abstractions.repositories.users import IUsersRepository
from quicknote.application.interactors import UserInteractor
from quicknote.application.interactors.users.dto import CreateOrUpdateUser


@pytest.mark.asyncio
async def test_user_creation(dishka: AsyncContainer):
    async with dishka() as container:
        interactor = await container.get(UserInteractor)
        user_repo = await container.get(IUsersRepository)

        data = CreateOrUpdateUser(
            telegram_id=123,
            username="test_username",
            first_name="John",
            last_name="Smith",
        )
        await interactor.create_or_update_user(data)

        user = await user_repo.get_by_telegram_id(data.telegram_id)
        assert user is not None
        assert user.telegram_id == data.telegram_id
        assert user.username == data.username
        assert user.first_name == data.first_name
        assert user.last_name == data.last_name

