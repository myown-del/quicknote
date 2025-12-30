from uuid import UUID

from brain.application.abstractions.repositories.notes_graph import INotesGraphRepository
from brain.domain.entities.note import Note


class DummyNotesGraphRepository(INotesGraphRepository):
    async def upsert_note(self, note: Note):
        return None

    async def sync_connections(self, note: Note, link_titles: list[str]):
        return None

    async def delete_note(self, note_id: UUID):
        return None

    async def count_notes_by_user_and_title(self, user_id: UUID, title: str) -> int:
        return 0

    async def count_links_between_notes(
        self, user_id: UUID, from_title: str, to_title: str
    ) -> int:
        return 0
