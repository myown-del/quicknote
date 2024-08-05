import asyncio

import pytest
import pytest_asyncio
from dishka import make_async_container

from quicknote.application.interactors.factory import InteractorProvider
from tests.fixtures.db_provider import DbProvider


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
    container = make_async_container(
        DbProvider(),
        InteractorProvider(),
    )
    yield container
    await container.close()
