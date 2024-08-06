from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from alembic.command import upgrade
from dishka import AsyncContainer
from alembic.config import Config as AlembicConfig

from quicknote.application.abstractions.config.models import IDatabaseConfig
from quicknote.domain.entities.user import UserDM
from quicknote.infrastructure.db.repositories.hub import RepositoryHub


@pytest_asyncio.fixture(scope="session")
async def alembic_config(dishka: AsyncContainer) -> AlembicConfig:
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option(
        "script_location",
        str(Path("quicknote") / "infrastructure" / "migrations"),
    )
    db_config = await dishka.get(IDatabaseConfig)
    alembic_cfg.set_main_option("sqlalchemy.url", db_config.uri)
    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def upgrade_schema_db(alembic_config: AlembicConfig):
    upgrade(alembic_config, "head")


@pytest_asyncio.fixture
async def dishka_request(dishka: AsyncContainer) -> AsyncContainer:
    async with dishka() as request_container:
        yield request_container


async def clear_db(repo_hub: RepositoryHub):
    await repo_hub.users.delete_all()
    await repo_hub.notes.delete_all()


@pytest_asyncio.fixture
async def repo_hub(dishka_request: AsyncContainer) -> RepositoryHub:
    repo_hub_ = await dishka_request.get(RepositoryHub)
    await clear_db(repo_hub_)
    return repo_hub_


@pytest_asyncio.fixture
async def user(repo_hub: RepositoryHub) -> UserDM:
    user = UserDM(
        id=uuid4(),
        telegram_id=123,
        username="test_username",
        first_name="John",
        last_name="Smith",
    )
    await repo_hub.users.create(user)
    return user
