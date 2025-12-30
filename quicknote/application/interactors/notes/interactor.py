from uuid import uuid4, UUID

from quicknote.application.abstractions.repositories.notes import INotesRepository
from quicknote.application.abstractions.repositories.users import IUsersRepository
from quicknote.application.interactors.notes.dto import CreateNote
from quicknote.application.interactors.notes.exceptions import NoteTooLongException, NoteNotFoundException
from quicknote.application.interactors.users.exceptions import UserNotFoundException
from quicknote.domain.entities.note import NoteDM


class NoteInteractor:
    def __init__(
            self,
            notes_repo: INotesRepository,
            users_repo: IUsersRepository,
    ):
        self._notes_repo = notes_repo
        self._users_repo = users_repo

    async def create_note(self, note_data: CreateNote) -> UUID:
        user = await self._users_repo.get_by_telegram_id(
            note_data.by_user_telegram_id
        )
        if not user:
            raise UserNotFoundException()

        note = NoteDM(
            id=uuid4(),
            user_id=user.id,
            title=note_data.title,
            text=note_data.text
        )
        await self._notes_repo.create(note)

        return note.id

    async def get_notes(self, user_telegram_id: int) -> list[NoteDM]:
        notes = await self._notes_repo.get_by_user_telegram_id(user_telegram_id)
        return notes

    async def get_note_by_id(self, note_id: UUID) -> NoteDM | None:
        note = await self._notes_repo.get_by_id(note_id)
        return note

    async def delete_note(self, note_id: UUID):
        note = await self._notes_repo.get_by_id(note_id)
        if note is None:
            raise NoteNotFoundException()

        await self._notes_repo.delete_by_id(note_id)
