import re
from uuid import uuid4, UUID

from quicknote.application.abstractions.repositories.hub import IRepositoryHub
from quicknote.application.interactors.hashtags.interactor import HashtagInteractor
from quicknote.application.interactors.notes.dto import CreateNote
from quicknote.application.interactors.notes.exceptions import NoteTooLongException
from quicknote.application.interactors.notes.rules import MAX_NOTE_LENGTH
from quicknote.domain.entities.note import NoteDM


def parse_hashtags(text: str) -> list[str]:
    pattern = r"#(\w+)"
    hashtags = re.findall(pattern, text)
    return hashtags


class NoteInteractor:
    def __init__(self, repo_hub: IRepositoryHub, hashtag_interactor: HashtagInteractor):
        self._repo_hub = repo_hub
        self._hashtag_interactor = hashtag_interactor

    async def create_note(self, note_data: CreateNote):
        if len(note_data.text) > MAX_NOTE_LENGTH:
            raise NoteTooLongException()

        # Parsing and creating hashtags
        note_hashtags = parse_hashtags(note_data.text)
        if note_hashtags:
            await self._hashtag_interactor.create_hashtags(note_hashtags)

        # Creating note
        user = await self._repo_hub.users.get_by_telegram_id(
            note_data.by_user_telegram_id
        )
        note = NoteDM(id=uuid4(), user_id=user.id, text=note_data.text)
        await self._repo_hub.notes.create(note)

        # Linking hashtags to the note
        if note_hashtags:
            await self._hashtag_interactor.update_note_hashtags(
                note_id=note.id, hashtags=note_hashtags
            )

    async def get_notes(self, user_telegram_id: int) -> list[NoteDM]:
        notes = await self._repo_hub.notes.get_by_user_telegram_id(user_telegram_id)
        return notes

    async def get_note_by_id(self, note_id: UUID) -> NoteDM:
        note = await self._repo_hub.notes.get_by_id(note_id)
        return note