from uuid import UUID

from brain.application.abstractions.repositories.notes_graph import INotesGraphRepository
from brain.domain.entities.graph import GraphData
from brain.domain.entities.note import Note


class DummyNotesGraphRepository(INotesGraphRepository):
    async def upsert_note(self, note: Note):
        return None

    async def sync_connections(
        self,
        note: Note,
        link_targets: list[str],
        previous_title: str | None = None,
        previous_represents_keyword_id: UUID | None = None,
    ):
        return None

    async def delete_note(self, note_id: UUID):
        return None

    async def count_notes_by_user_and_title(self, user_id: UUID, title: str) -> int:
        return 0

    async def count_links_between_notes(
        self, user_id: UUID, from_title: str, to_title: str
    ) -> int:
        return 0

    async def get_graph(
        self,
        user_id: UUID,
        query: str | None = None,
        depth: int = 1,
    ) -> GraphData:
        return GraphData(nodes=[], connections=[])
