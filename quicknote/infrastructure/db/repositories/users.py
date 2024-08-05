from datetime import datetime
from uuid import UUID

from sqlalchemy import select, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from quicknote.application.abstractions.repositories.users import IUsersRepository
from quicknote.domain.entities.user import UserDM
from quicknote.infrastructure.db.mappers.users import get_user_dm, get_user_db
from quicknote.infrastructure.db.models.user import User


class UsersRepository(IUsersRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, entity: UserDM) -> None:
        db_model = get_user_db(entity)
        self._session.add(db_model)
        await self._session.commit()

    async def _get_db_by_id(self, entity_id: UUID) -> User | None:
        query = select(User).where(User.id == bindparam("entity_id"))
        result = await self._session.execute(
            statement=query,
            params={"entity_id": entity_id},
        )
        return result.scalar()

    async def update(self, entity: UserDM) -> None:
        old_db_model = await self._get_db_by_id(entity.id)
        old_db_model.username = entity.username
        old_db_model.first_name = entity.first_name
        old_db_model.last_name = entity.last_name
        old_db_model.updated_at = datetime.utcnow()
        await self._session.commit()

    async def get_by_telegram_id(self, telegram_id: int) -> UserDM | None:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await self._session.execute(query)
        db_model = result.scalar()
        if db_model:
            return get_user_dm(db_model)

    async def get_by_id(self, entity_id: UUID) -> UserDM | None:
        db_model = await self._get_db_by_id(entity_id)
        if db_model:
            return get_user_dm(db_model)
