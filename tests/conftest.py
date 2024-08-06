import asyncio

import pytest
import pytest_asyncio
from dishka import make_async_container

from quicknote.application.interactors.factory import InteractorProvider
from quicknote.config.di import ConfigProvider
from quicknote.config.models import Config
from quicknote.config.parser import load_config
from quicknote.infrastructure.db.factory import DatabaseProvider
from tests.fixtures.db_provider import TestDbProvider


@pytest.fixture(scope="session")
def event_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


@pytest_asyncio.fixture(scope="session")
async def dishka():
    config = load_config(
        config_class=Config,
        env_file_path="tests/.env"
    )
    container = make_async_container(
        ConfigProvider(),
        TestDbProvider(),
        DatabaseProvider(),
        InteractorProvider(),
        context={Config: config}
    )
    yield container
    await container.close()
