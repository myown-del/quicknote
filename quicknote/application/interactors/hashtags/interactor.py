from uuid import UUID, uuid4

from quicknote.application.abstractions.repositories.hub import IRepositoryHub
from quicknote.application.interactors.hashtags.exceptions import (
    HashtagTooLongException,
)
from quicknote.application.interactors.hashtags.rules import MAX_HASHTAG_LENGTH
from quicknote.domain.entities.note import HashtagDM


class HashtagInteractor:
    def __init__(self, repo_hub: IRepositoryHub):
        self._repo_hub = repo_hub

    async def create_hashtags(self, hashtags: list[str]):
        if any(len(hashtag) > MAX_HASHTAG_LENGTH for hashtag in hashtags):
            raise HashtagTooLongException()

        hashtags_dms = [HashtagDM(id=uuid4(), name=hashtag) for hashtag in hashtags]
        await self._repo_hub.hashtags.create_hashtags(hashtags_dms)

    async def update_note_hashtags(self, note_id: UUID, hashtags: list[str]):
        await self._repo_hub.hashtags.set_note_hashtags(
            note_id=note_id, hashtags=hashtags
        )
