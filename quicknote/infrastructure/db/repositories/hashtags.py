from uuid import UUID

from sqlalchemy import select, insert, text, delete

from quicknote.application.abstractions.repositories.hashtags import IHashtagsRepository
from quicknote.domain.entities.note import HashtagDM
from quicknote.infrastructure.db.mappers.notes import get_hashtag_db
from quicknote.infrastructure.db.models import Note, Hashtag, NoteHashtag


class HashtagsRepository(IHashtagsRepository):
    async def create_hashtags(self, hashtags: list[HashtagDM]):
        query = """
            INSERT INTO hashtags (id, name)
            VALUES (:id, :name)
            ON CONFLICT (name) DO NOTHING
        """

        params = [{"id": hashtag.id, "name": hashtag.name} for hashtag in hashtags]

        async with self._session.begin():
            await self._session.execute(text(query), params)
            await self._session.commit()

    async def set_note_hashtags(self, note_id: UUID, hashtags: list[str]):
        async with self._session.begin():
            note = await self._session.get(Note, note_id)
            if not note:
                raise ValueError(f"Note with id {note_id} not found")

            await self._session.execute(
                delete(NoteHashtag).where(NoteHashtag.note_id == note_id)
            )

            hashtag_ids = await self._session.execute(
                select(Hashtag.id).where(Hashtag.name.in_(hashtags))
            )
            hashtag_ids = [row[0] for row in hashtag_ids]

            note_hashtags = [
                NoteHashtag(note_id=note_id, hashtag_id=hashtag_id)
                for hashtag_id in hashtag_ids
            ]
            self._session.add_all(note_hashtags)

        await self._session.commit()
