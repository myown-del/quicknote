from quicknote.application.abstractions.repositories.note import INoteRepository
from quicknote.domain.entities.note import NoteDM
from quicknote.infrastructure.db.mappers.universal import from_entity_to_db
from quicknote.infrastructure.db.models import Note


class NotesRepository(INoteRepository):
    async def create(self, entity: NoteDM):
        db_model = from_entity_to_db(entity, db_cls=Note)
        self._session.add(db_model)
        await self._session.commit()
