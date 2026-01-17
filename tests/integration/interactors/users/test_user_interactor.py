import pytest
from dishka import AsyncContainer

from brain.application.interactors import UserInteractor
from brain.application.interactors.users.dto import CreateOrUpdateUser
from brain.infrastructure.db.repositories.hub import RepositoryHub


@pytest.mark.asyncio
async def test_user_creation(dishka_request: AsyncContainer, repo_hub: RepositoryHub):
    interactor = await dishka_request.get(UserInteractor)

    data = CreateOrUpdateUser(
        telegram_id=4,
        username="test_username",
        first_name="John",
        last_name="Smith",
    )
    await interactor.create_or_update_user(data)

    user = await repo_hub.users.get_by_telegram_id(data.telegram_id)
    assert user is not None
    assert user.telegram_id == data.telegram_id
    assert user.username == data.username
    assert user.first_name == data.first_name
    assert user.last_name == data.last_name
    assert user.created_at is not None
    assert user.updated_at is not None
