from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from quicknote.application.abstractions.repositories.notes import INotesRepository
from quicknote.domain.entities.note import NoteDM
from quicknote.infrastructure.db.mappers.notes import get_note_db, get_note_dm
from quicknote.infrastructure.db.models import Note, User, NoteHashtag


class NotesRepository(INotesRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, entity: NoteDM):
        db_model = get_note_db(entity)
        self._session.add(db_model)
        await self._session.commit()

    async def get_by_user_telegram_id(self, telegram_id: int) -> list[NoteDM]:
        query = (
            select(Note)
            .join(User)
            .where(User.telegram_id == telegram_id)
            .options(
                selectinload(Note.hashtags),
            )
        )
        result = await self._session.execute(query)

        db_models = result.unique().scalars().all()
        notes = [get_note_dm(db_model) for db_model in db_models]
        return notes

    async def get_by_id(self, note_id: UUID) -> NoteDM | None:
        query = (
            select(Note)
            .where(Note.id == note_id)
            .options(
                selectinload(Note.hashtags),
            )
        )
        result = await self._session.execute(query)
        db_model = result.scalar()
        if db_model:
            return get_note_dm(db_model)
