from pathlib import Path

import pytest
import pytest_asyncio
from alembic.command import upgrade
from dishka import AsyncContainer
from alembic.config import Config as AlembicConfig

from quicknote.application.abstractions.config.models import IDatabaseConfig
from quicknote.config.models import DatabaseConfig


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
