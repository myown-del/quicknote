from datetime import datetime
from uuid import UUID

from brain.application.abstractions.repositories.keywords import IKeywordsRepository
from brain.application.abstractions.repositories.notes import INotesRepository
from brain.application.abstractions.repositories.notes_graph import (
    INotesGraphRepository,
)
from brain.application.interactors.notes.dto import UpdateNote
from brain.application.interactors.notes.exceptions import NoteNotFoundException
from brain.application.services.keyword_notes import KeywordNoteService
from brain.application.services.note_titles import NoteTitleService
from brain.application.services.note_keyword_sync import NoteKeywordSyncService
from brain.domain.entities.note import Note
from brain.domain.services.wikilinks import extract_link_targets

from brain.domain.services.keywords import collect_cleanup_keyword_names


class UpdateNoteInteractor:
    def __init__(
        self,
        notes_repo: INotesRepository,
        notes_graph_repo: INotesGraphRepository,
        keywords_repo: IKeywordsRepository,
        keyword_note_service: KeywordNoteService,
        note_title_service: NoteTitleService,
        keyword_sync_service: NoteKeywordSyncService,
    ):
        self._notes_repo = notes_repo
        self._notes_graph_repo = notes_graph_repo
        self._keywords_repo = keywords_repo
        self._keyword_note_service = keyword_note_service
        self._note_title_service = note_title_service
        self._keyword_sync_service = keyword_sync_service

    async def update_note(self, note_data: UpdateNote) -> Note:
        note = await self._notes_repo.get_by_id(note_data.note_id)
        if note is None:
            raise NoteNotFoundException()

        previous_state = Note(
            id=note.id,
            user_id=note.user_id,
            title=note.title,
            text=note.text,
            represents_keyword_id=note.represents_keyword_id,
            updated_at=note.updated_at,
            created_at=note.created_at,
        )

        title = await self._note_title_service.ensure_update_title(
            user_id=note.user_id,
            title=note_data.title,
            exclude_note_id=note.id,
        )
        note.title = title
        note.text = note_data.text

        note.represents_keyword_id = await self._keyword_note_service.ensure_keyword_for_title(
            user_id=note.user_id,
            title=note.title,
        )

        note.updated_at = datetime.utcnow()

        await self._notes_repo.update(note)
        await self._notes_graph_repo.upsert_note(note)
        await self._keyword_sync_service.sync(note, previous_state=previous_state)

        previous_targets = extract_link_targets(previous_state.text or "")
        current_targets = extract_link_targets(note.text or "")
        previous_cleanup_names = collect_cleanup_keyword_names(
            link_targets=previous_targets,
            represents_keyword_id=previous_state.represents_keyword_id,
            title=previous_state.title,
        )
        current_cleanup_names = collect_cleanup_keyword_names(
            link_targets=current_targets,
            represents_keyword_id=note.represents_keyword_id,
            title=note.title,
        )
        removed_targets = [
            title for title in previous_cleanup_names
            if title not in set(current_cleanup_names)
        ]
        await self._keywords_repo.delete_unused_keywords(
            user_id=note.user_id,
            names=removed_targets,
        )

        return note
