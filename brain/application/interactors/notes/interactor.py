from uuid import uuid4, UUID

from brain.application.abstractions.repositories.notes import INotesRepository
from brain.application.abstractions.repositories.notes_graph import INotesGraphRepository
from brain.application.abstractions.repositories.users import IUsersRepository
from brain.application.interactors.notes.dto import CreateNote
from brain.application.interactors.notes.exceptions import NoteNotFoundException
from brain.application.interactors.users.exceptions import UserNotFoundException
from brain.domain.entities.note import Note
from brain.domain.services.wikilinks import extract_wikilinks


class NoteInteractor:
    def __init__(
            self,
            notes_repo: INotesRepository,
            users_repo: IUsersRepository,
            notes_graph_repo: INotesGraphRepository,
    ):
        self._notes_repo = notes_repo
        self._users_repo = users_repo
        self._notes_graph_repo = notes_graph_repo

    async def create_note(self, note_data: CreateNote) -> UUID:
        user = await self._users_repo.get_by_telegram_id(
            note_data.by_user_telegram_id
        )
        if not user:
            raise UserNotFoundException()

        note = Note(
            id=uuid4(),
            user_id=user.id,
            title=note_data.title,
            text=note_data.text
        )
        await self._notes_repo.create(note)
        await self._notes_graph_repo.upsert_note(note)
        link_titles = extract_wikilinks(note.text or "")
        await self._notes_graph_repo.sync_connections(note, link_titles)

        return note.id

    async def get_notes(self, user_telegram_id: int) -> list[Note]:
        notes = await self._notes_repo.get_by_user_telegram_id(user_telegram_id)
        return notes

    async def get_note_by_id(self, note_id: UUID) -> Note | None:
        note = await self._notes_repo.get_by_id(note_id)
        return note

    async def delete_note(self, note_id: UUID):
        note = await self._notes_repo.get_by_id(note_id)
        if note is None:
            raise NoteNotFoundException()

        await self._notes_repo.delete_by_id(note_id)
        await self._notes_graph_repo.delete_note(note_id)
