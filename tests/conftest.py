import asyncio

import pytest
import pytest_asyncio
from dishka import make_async_container

from brain.config.provider import ConfigProvider
from brain.config.models import Config
from brain.config.parser import load_config
from brain.infrastructure.db.provider import DatabaseProvider
from tests.fixtures.db_provider import TestDbProvider
from tests.fixtures.graph_provider import TestGraphProvider


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def dishka():
    from brain.application.interactors.factory import InteractorProvider
    from brain.infrastructure.jwt.provider import JwtProvider

    config = load_config(
        config_class=Config,
        env_file_path="tests/.env"
    )
    container = make_async_container(
        ConfigProvider(),
        TestDbProvider(),
        DatabaseProvider(),
        TestGraphProvider(),
        InteractorProvider(),
        JwtProvider(),
        context={Config: config}
    )
    yield container
    await container.close()
