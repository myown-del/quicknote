from uuid import UUID

from quicknote.application.abstractions.repositories.notes import INotesRepository
from quicknote.domain.entities.note import NoteDM


class NotesRepositoryMock(INotesRepository):
    def __init__(self):
        self.notes = []

    async def create(self, entity: NoteDM):
        self.notes.append(entity)

    async def get_by_user_telegram_id(self, telegram_id: int) -> list[NoteDM]:
        raise NotImplementedError()

    async def get_by_id(self, entity_id: UUID) -> NoteDM:
        for note in self.notes:
            if note.id == entity_id:
                return note
