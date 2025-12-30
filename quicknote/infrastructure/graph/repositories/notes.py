from uuid import UUID

from neo4j import AsyncDriver

from quicknote.application.abstractions.repositories.notes_graph import INotesGraphRepository
from quicknote.domain.entities.note import Note


class NotesGraphRepository(INotesGraphRepository):
    def __init__(self, driver: AsyncDriver, database: str):
        self._driver = driver
        self._database = database

    async def upsert_note(self, note: Note):
        query = (
            "MERGE (n:Note {id: $id}) "
            "SET n.user_id = $user_id, n.title = $title, n.text = $text"
        )
        async with self._driver.session(database=self._database) as session:
            await session.run(
                query,
                id=str(note.id),
                user_id=str(note.user_id),
                title=note.title,
                text=note.text,
            )

    async def sync_connections(self, note: Note, link_titles: list[str]):
        async with self._driver.session(database=self._database) as session:
            await session.run(
                "MATCH (n:Note {id: $id}) "
                "OPTIONAL MATCH (n)-[r:LINKS_TO]->() "
                "DELETE r",
                id=str(note.id),
            )

            if not link_titles:
                return

            await session.run(
                "MATCH (source:Note {id: $id}) "
                "UNWIND $titles AS title "
                "MATCH (target:Note {user_id: $user_id, title: title}) "
                "MERGE (source)-[:LINKS_TO]->(target)",
                id=str(note.id),
                user_id=str(note.user_id),
                titles=link_titles,
            )

    async def delete_note(self, note_id: UUID):
        async with self._driver.session(database=self._database) as session:
            await session.run(
                "MATCH (n:Note {id: $id}) "
                "DETACH DELETE n",
                id=str(note_id),
            )

    async def count_notes_by_user_and_title(self, user_id: UUID, title: str) -> int:
        async with self._driver.session(database=self._database) as session:
            result = await session.run(
                "MATCH (n:Note {user_id: $user_id, title: $title}) "
                "RETURN count(n) AS c",
                user_id=str(user_id),
                title=title,
            )
            record = await result.single()
            return record["c"] if record else 0

    async def count_links_between_notes(
        self, user_id: UUID, from_title: str, to_title: str
    ) -> int:
        async with self._driver.session(database=self._database) as session:
            result = await session.run(
                "MATCH (:Note {user_id: $user_id, title: $from_title})"
                "-[:LINKS_TO]->"
                "(:Note {user_id: $user_id, title: $to_title}) "
                "RETURN count(*) AS c",
                user_id=str(user_id),
                from_title=from_title,
                to_title=to_title,
            )
            record = await result.single()
            return record["c"] if record else 0
