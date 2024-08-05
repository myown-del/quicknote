import re
from uuid import uuid4, UUID

from quicknote.application.abstractions.repositories.notes import INotesRepository
from quicknote.application.abstractions.repositories.users import IUsersRepository
from quicknote.application.interactors.notes.dto import CreateNote
from quicknote.application.interactors.notes.exceptions import NoteTooLongException
from quicknote.application.interactors.notes.rules import MAX_NOTE_LENGTH
from quicknote.application.interactors.users.exceptions import UserNotFoundException
from quicknote.domain.entities.note import NoteDM


def parse_hashtags(text: str) -> list[str]:
    pattern = r"#(\w+)"
    hashtags = re.findall(pattern, text)
    return hashtags


class NoteInteractor:
    def __init__(
            self,
            notes_repo: INotesRepository,
            users_repo: IUsersRepository,
    ):
        self._notes_repo = notes_repo
        self._users_repo = users_repo

    async def create_note(self, note_data: CreateNote) -> UUID:
        if len(note_data.text) > MAX_NOTE_LENGTH:
            raise NoteTooLongException()

        # Creating note
        user = await self._users_repo.get_by_telegram_id(
            note_data.by_user_telegram_id
        )
        if not user:
            raise UserNotFoundException()

        note = NoteDM(id=uuid4(), user_id=user.id, text=note_data.text)
        await self._notes_repo.create(note)

        return note.id

    async def get_notes(self, user_telegram_id: int) -> list[NoteDM]:
        notes = await self._notes_repo.get_by_user_telegram_id(user_telegram_id)
        return notes

    async def get_note_by_id(self, note_id: UUID) -> NoteDM:
        note = await self._notes_repo.get_by_id(note_id)
        return note
