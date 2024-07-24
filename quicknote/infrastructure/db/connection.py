from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from quicknote.config import Config


def new_session_maker(config: Config) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        config.db.uri,
        pool_size=15,
        max_overflow=15,
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
