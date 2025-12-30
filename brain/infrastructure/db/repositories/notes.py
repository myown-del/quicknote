from datetime import datetime
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from brain.application.abstractions.repositories.notes import INotesRepository
from brain.domain.entities.note import Note
from brain.infrastructure.db.mappers.notes import map_note_to_db, map_note_to_dm
from brain.infrastructure.db.models.note import NoteDB
from brain.infrastructure.db.models.user import UserDB


class NotesRepository(INotesRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, entity: Note):
        db_model = map_note_to_db(entity)
        self._session.add(db_model)
        await self._session.commit()

    async def get_by_user_telegram_id(self, telegram_id: int) -> list[Note]:
        query = (
            select(NoteDB)
            .join(UserDB)
            .where(UserDB.telegram_id == telegram_id)
        )
        result = await self._session.execute(query)

        db_models = result.unique().scalars().all()
        notes = [map_note_to_dm(db_model) for db_model in db_models]
        return notes

    async def get_by_id(self, note_id: UUID) -> Note | None:
        query = (
            select(NoteDB)
            .where(NoteDB.id == note_id)
        )
        result = await self._session.execute(query)
        db_model = result.scalar()
        if db_model:
            return map_note_to_dm(db_model)

    async def update(self, entity: Note):
        query = (
            select(NoteDB)
            .where(NoteDB.id == entity.id)
        )
        result = await self._session.execute(query)
        db_model = result.scalar()
        if not db_model:
            return
        db_model.title = entity.title
        db_model.text = entity.text
        db_model.updated_at = entity.updated_at or datetime.utcnow()
        await self._session.commit()

    async def delete_all(self):
        await self._session.execute(text("DELETE FROM notes"))
        await self._session.commit()

    async def delete_by_id(self, entity_id: UUID):
        query = (
            select(NoteDB)
            .where(NoteDB.id == entity_id)
        )
        result = await self._session.execute(query)
        db_model = result.scalar()
        await self._session.delete(db_model)
        await self._session.commit()
