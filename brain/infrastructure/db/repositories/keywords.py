from uuid import UUID, uuid4

from sqlalchemy import delete, select, exists, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from brain.application.abstractions.repositories.keywords import IKeywordsRepository
from brain.infrastructure.db.models.keyword import KeywordDB
from brain.infrastructure.db.models.note import NoteDB
from brain.infrastructure.db.models.keyword import NoteKeywordDB


class KeywordsRepository(IKeywordsRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _normalize(names: list[str]) -> list[str]:
        seen: set[str] = set()
        normalized: list[str] = []
        for name in names:
            trimmed = name.strip()
            if not trimmed or trimmed in seen:
                continue
            seen.add(trimmed)
            normalized.append(trimmed)
        return normalized

    async def ensure_keywords(self, user_id: UUID, names: list[str]) -> None:
        normalized = self._normalize(names)
        if not normalized:
            return

        stmt = insert(KeywordDB).values(
            [{"id": uuid4(), "user_id": user_id, "name": name} for name in normalized]
        )
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["user_id", "name"]
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def replace_note_keywords(
        self,
        note_id: UUID,
        user_id: UUID,
        names: list[str],
    ) -> None:
        normalized = self._normalize(names)
        await self._session.execute(
            delete(NoteKeywordDB).where(NoteKeywordDB.note_id == note_id)
        )

        if not normalized:
            await self._session.commit()
            return

        await self.ensure_keywords(user_id=user_id, names=normalized)

        keyword_ids_stmt = (
            select(KeywordDB.id)
            .where(KeywordDB.user_id == user_id)
            .where(KeywordDB.name.in_(normalized))
        )
        result = await self._session.execute(keyword_ids_stmt)
        keyword_ids = [row[0] for row in result.all()]
        if not keyword_ids:
            await self._session.commit()
            return

        insert_stmt = insert(NoteKeywordDB).values(
            [{"note_id": note_id, "keyword_id": keyword_id} for keyword_id in keyword_ids]
        )
        await self._session.execute(insert_stmt)
        await self._session.commit()

    async def delete_note_keywords(self, note_id: UUID) -> None:
        await self._session.execute(
            delete(NoteKeywordDB).where(NoteKeywordDB.note_id == note_id)
        )
        await self._session.commit()

    async def delete_unused_keywords(self, user_id: UUID, names: list[str]) -> None:
        normalized = self._normalize(names)
        if not normalized:
            return

        stmt = (
            delete(KeywordDB)
            .where(KeywordDB.user_id == user_id)
            .where(KeywordDB.name.in_(normalized))
            .where(
                ~exists()
                .where(NoteKeywordDB.keyword_id == KeywordDB.id)
            )
            .where(
                ~exists()
                .where(NoteDB.user_id == user_id)
                .where(NoteDB.represents_keyword.is_(True))
                .where(func.coalesce(NoteDB.title, "") == KeywordDB.name)
            )
        )
        await self._session.execute(stmt)
        await self._session.commit()
