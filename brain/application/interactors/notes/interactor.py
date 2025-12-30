from datetime import datetime
from uuid import uuid4, UUID

from brain.application.abstractions.repositories.notes import INotesRepository
from brain.application.abstractions.repositories.notes_graph import INotesGraphRepository
from brain.application.abstractions.repositories.users import IUsersRepository
from brain.application.abstractions.repositories.keywords import IKeywordsRepository
from brain.application.interactors.notes.dto import CreateNote, UpdateNote
from brain.application.abstractions.repositories.models import WikilinkSuggestion
from brain.application.interactors.notes.exceptions import (
    NoteNotFoundException,
    KeywordNoteTitleRequiredException,
    KeywordNoteAlreadyExistsException,
)
from brain.application.interactors.users.exceptions import UserNotFoundException
from brain.domain.entities.note import Note
from brain.domain.exceptions import (
    KeywordNoteAlreadyExistsError,
    KeywordNoteTitleRequiredError,
)
from brain.domain.services.notes import ensure_keyword_note_valid
from brain.domain.services.wikilinks import extract_link_targets


class NoteInteractor:
    def __init__(
            self,
            notes_repo: INotesRepository,
            users_repo: IUsersRepository,
            notes_graph_repo: INotesGraphRepository,
            keywords_repo: IKeywordsRepository,
    ):
        self._notes_repo = notes_repo
        self._users_repo = users_repo
        self._notes_graph_repo = notes_graph_repo
        self._keywords_repo = keywords_repo

    async def create_note(self, note_data: CreateNote) -> UUID:
        user = await self._users_repo.get_by_telegram_id(
            note_data.by_user_telegram_id
        )
        if not user:
            raise UserNotFoundException()

        existing_count = 0
        if note_data.represents_keyword:
            existing_count = await self._notes_repo.count_keyword_notes_by_user_and_title(
                user_id=user.id,
                title=note_data.title or "",
            )
        try:
            ensure_keyword_note_valid(
                title=note_data.title,
                represents_keyword=note_data.represents_keyword,
                existing_keyword_count=existing_count,
            )
        except KeywordNoteTitleRequiredError as exc:
            raise KeywordNoteTitleRequiredException() from exc
        except KeywordNoteAlreadyExistsError as exc:
            raise KeywordNoteAlreadyExistsException() from exc

        note = Note(
            id=uuid4(),
            user_id=user.id,
            title=note_data.title,
            text=note_data.text,
            represents_keyword=note_data.represents_keyword,
        )
        await self._notes_repo.create(note)
        await self._notes_graph_repo.upsert_note(note)
        link_targets = extract_link_targets(note.text or "")
        await self._keywords_repo.replace_note_keywords(
            note_id=note.id,
            user_id=user.id,
            names=link_targets,
        )
        await self._notes_graph_repo.sync_connections(note, link_targets)

        return note.id

    async def get_notes(self, user_telegram_id: int) -> list[Note]:
        notes = await self._notes_repo.get_by_user_telegram_id(user_telegram_id)
        return notes

    async def get_note_by_id(self, note_id: UUID) -> Note | None:
        note = await self._notes_repo.get_by_id(note_id)
        return note

    async def search_wikilink_suggestions(
        self,
        user_id: UUID,
        query: str,
    ) -> list[WikilinkSuggestion]:
        return await self._notes_repo.search_wikilink_suggestions(
            user_id=user_id,
            query=query,
        )

    async def delete_note(self, note_id: UUID):
        note = await self._notes_repo.get_by_id(note_id)
        if note is None:
            raise NoteNotFoundException()

        link_targets = extract_link_targets(note.text or "")
        await self._notes_repo.delete_by_id(note_id)
        await self._keywords_repo.delete_note_keywords(note_id)
        await self._keywords_repo.delete_unused_keywords(
            user_id=note.user_id,
            names=link_targets,
        )
        await self._notes_graph_repo.delete_note(note_id)

    async def update_note(self, note_data: UpdateNote) -> Note:
        note = await self._notes_repo.get_by_id(note_data.note_id)
        if note is None:
            raise NoteNotFoundException()

        previous_targets = extract_link_targets(note.text or "")
        previous_title = note.title
        previous_represents_keyword = note.represents_keyword
        note.title = note_data.title
        note.text = note_data.text
        if note_data.represents_keyword is not None:
            note.represents_keyword = note_data.represents_keyword
        note.updated_at = datetime.utcnow()

        existing_count = 0
        if note.represents_keyword:
            existing_count = await self._notes_repo.count_keyword_notes_by_user_and_title(
                user_id=note.user_id,
                title=note.title or "",
                exclude_note_id=note.id,
            )
        try:
            ensure_keyword_note_valid(
                title=note.title,
                represents_keyword=note.represents_keyword,
                existing_keyword_count=existing_count,
            )
        except KeywordNoteTitleRequiredError as exc:
            raise KeywordNoteTitleRequiredException() from exc
        except KeywordNoteAlreadyExistsError as exc:
            raise KeywordNoteAlreadyExistsException() from exc

        await self._notes_repo.update(note)
        await self._notes_graph_repo.upsert_note(note)
        link_targets = extract_link_targets(note.text or "")
        await self._keywords_repo.replace_note_keywords(
            note_id=note.id,
            user_id=note.user_id,
            names=link_targets,
        )
        removed_targets = [
            title for title in previous_targets
            if title not in set(link_targets)
        ]
        await self._keywords_repo.delete_unused_keywords(
            user_id=note.user_id,
            names=removed_targets,
        )
        await self._notes_graph_repo.sync_connections(
            note,
            link_targets,
            previous_title=previous_title,
            previous_represents_keyword=previous_represents_keyword,
        )

        return note
