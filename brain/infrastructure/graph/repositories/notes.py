from uuid import UUID

from neo4j import AsyncDriver

from brain.application.abstractions.repositories.notes_graph import INotesGraphRepository
from brain.domain.entities.note import Note


class NotesGraphRepository(INotesGraphRepository):
    def __init__(self, driver: AsyncDriver, database: str):
        self._driver = driver
        self._database = database

    async def upsert_note(self, note: Note):
        query = (
            "MERGE (n:Note {id: $id}) "
            "SET n.user_id = $user_id, n.title = $title, n.text = $text, "
            "n.represents_keyword_id = $represents_keyword_id"
        )
        async with self._driver.session(database=self._database) as session:
            await session.run(
                query,
                id=str(note.id),
                user_id=str(note.user_id),
                title=note.title,
                text=note.text,
                represents_keyword_id=(
                    str(note.represents_keyword_id)
                    if note.represents_keyword_id is not None
                    else None
                ),
            )

    async def sync_connections(
        self,
        note: Note,
        link_targets: list[str],
        previous_title: str | None = None,
        previous_represents_keyword_id: UUID | None = None,
    ):
        async with self._driver.session(database=self._database) as session:
            await session.run(
                "MATCH (n:Note {id: $id}) "
                "OPTIONAL MATCH (n)-[r:LINKS_TO|HAS_KEYWORD]->() "
                "DELETE r",
                id=str(note.id),
            )

            if previous_represents_keyword_id and (
                note.represents_keyword_id is None or previous_title != note.title
            ):
                await session.run(
                    "MATCH (source:Note)-[r:LINKS_TO]->(target:Note {id: $id}) "
                    "MATCH (source)-[:HAS_KEYWORD]->(:Keyword {user_id: $user_id, name: $prev_title}) "
                    "DELETE r",
                    id=str(note.id),
                    user_id=str(note.user_id),
                    prev_title=previous_title,
                )

            if link_targets:
                await session.run(
                    "MATCH (source:Note {id: $id}) "
                    "UNWIND $targets AS target "
                    "MERGE (k:Keyword {user_id: $user_id, name: target}) "
                    "MERGE (source)-[:HAS_KEYWORD]->(k)",
                    id=str(note.id),
                    user_id=str(note.user_id),
                    targets=link_targets,
                )

                await session.run(
                    "MATCH (source:Note {id: $id}) "
                    "UNWIND $targets AS target "
                    "MATCH (target_note:Note {user_id: $user_id, title: target}) "
                    "WHERE target_note.represents_keyword_id IS NOT NULL "
                    "AND target_note.id <> $id "
                    "MERGE (source)-[:LINKS_TO]->(target_note)",
                    id=str(note.id),
                    user_id=str(note.user_id),
                    targets=link_targets,
                )

            if note.title and note.represents_keyword_id:
                await session.run(
                    "MATCH (target:Note {id: $id}) "
                    "MATCH (k:Keyword {user_id: $user_id, name: $title}) "
                    "MATCH (source:Note)-[:HAS_KEYWORD]->(k) "
                    "WHERE source.id <> target.id "
                    "MERGE (source)-[:LINKS_TO]->(target)",
                    id=str(note.id),
                    user_id=str(note.user_id),
                    title=note.title,
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
                "MATCH (from:Note {user_id: $user_id, title: $from_title}) "
                "MATCH (to:Note {user_id: $user_id, title: $to_title}) "
                "OPTIONAL MATCH (from)-[direct:LINKS_TO]->(to) "
                "OPTIONAL MATCH (from)-[:HAS_KEYWORD]->(k:Keyword)<-[:HAS_KEYWORD]-(to) "
                "RETURN count(DISTINCT direct) + count(DISTINCT k) AS c",
                user_id=str(user_id),
                from_title=from_title,
                to_title=to_title,
            )
            record = await result.single()
            return record["c"] if record else 0
