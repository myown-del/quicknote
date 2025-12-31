from datetime import datetime
from uuid import uuid4, UUID

from brain.application.abstractions.repositories.notes import INotesRepository
from brain.application.abstractions.repositories.notes_graph import INotesGraphRepository
from brain.application.abstractions.repositories.users import IUsersRepository
from brain.application.abstractions.repositories.keywords import IKeywordsRepository
from brain.application.interactors.notes.dto import CreateNote, UpdateNote
from brain.application.abstractions.repositories.models import WikilinkSuggestion
from brain.application.interactors.notes.keyword_utils import normalize_keyword_names
from brain.application.interactors.notes.exceptions import (
    NoteNotFoundException,
    KeywordNoteTitleRequiredException,
    KeywordNoteAlreadyExistsException,
    KeywordNotFoundException,
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

    async def _get_user_or_raise(self, telegram_id: int):
        user = await self._users_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise UserNotFoundException()
        return user

    def _collect_cleanup_keyword_names(
        self,
        link_targets: list[str],
        represents_keyword_id: UUID | None,
        title: str | None,
    ) -> list[str]:
        names = list(link_targets)
        if represents_keyword_id and title:
            names.append(title)
        return normalize_keyword_names(names)

    async def _ensure_represents_keyword_id(
        self,
        user_id: UUID,
        title: str | None,
    ) -> UUID:
        if not title:
            raise KeywordNoteTitleRequiredException()
        keyword = await self._keywords_repo.get_by_user_and_name(
            user_id=user_id,
            name=title,
        )
        if keyword:
            return keyword.id
        await self._keywords_repo.ensure_keywords(user_id=user_id, names=[title])
        keyword = await self._keywords_repo.get_by_user_and_name(
            user_id=user_id,
            name=title,
        )
        if not keyword:
            raise KeywordNotFoundException()
        return keyword.id

    def _validate_keyword_note(
        self,
        title: str | None,
        represents_keyword: bool,
        existing_count: int,
    ) -> None:
        try:
            ensure_keyword_note_valid(
                title=title,
                represents_keyword=represents_keyword,
                existing_keyword_count=existing_count,
            )
        except KeywordNoteTitleRequiredError as exc:
            raise KeywordNoteTitleRequiredException() from exc
        except KeywordNoteAlreadyExistsError as exc:
            raise KeywordNoteAlreadyExistsException() from exc

    async def _ensure_unique_keyword_note(
        self,
        user_id: UUID,
        keyword_id: UUID,
        exclude_note_id: UUID | None = None,
    ) -> None:
        existing_keyword_note = await self._notes_repo.count_keyword_notes_by_user_and_keyword_id(
            user_id=user_id,
            keyword_id=keyword_id,
            exclude_note_id=exclude_note_id,
        )
        if existing_keyword_note > 0:
            raise KeywordNoteAlreadyExistsException()

    async def _prepare_represents_keyword_id_for_create(
        self,
        user_id: UUID,
        title: str | None,
        represents_keyword: bool,
    ) -> UUID | None:
        if not represents_keyword:
            return None
        represents_keyword_id = await self._ensure_represents_keyword_id(
            user_id=user_id,
            title=title,
        )
        await self._ensure_unique_keyword_note(
            user_id=user_id,
            keyword_id=represents_keyword_id,
        )
        return represents_keyword_id

    async def _apply_note_updates(
        self,
        note: Note,
        note_data: UpdateNote,
    ) -> tuple[list[str], str | None, UUID | None]:
        previous_targets = extract_link_targets(note.text or "")
        previous_title = note.title
        previous_represents_keyword_id = note.represents_keyword_id

        note.title = note_data.title
        note.text = note_data.text

        if note_data.represents_keyword is not None:
            if note_data.represents_keyword:
                note.represents_keyword_id = await self._ensure_represents_keyword_id(
                    user_id=note.user_id,
                    title=note.title,
                )
            else:
                note.represents_keyword_id = None
        elif note.represents_keyword_id is not None:
            note.represents_keyword_id = await self._ensure_represents_keyword_id(
                user_id=note.user_id,
                title=note.title,
            )

        note.updated_at = datetime.utcnow()

        return previous_targets, previous_title, previous_represents_keyword_id

    async def _sync_note_keywords_and_graph(
        self,
        note: Note,
        link_targets: list[str],
        previous_title: str | None = None,
        previous_represents_keyword_id: UUID | None = None,
    ) -> None:
        await self._keywords_repo.replace_note_keywords(
            note_id=note.id,
            user_id=note.user_id,
            names=link_targets,
        )
        if previous_title is None and previous_represents_keyword_id is None:
            await self._notes_graph_repo.sync_connections(note, link_targets)
            return
        await self._notes_graph_repo.sync_connections(
            note,
            link_targets,
            previous_title=previous_title,
            previous_represents_keyword_id=previous_represents_keyword_id,
        )

    async def _cleanup_removed_keywords(
        self,
        user_id: UUID,
        previous_targets: list[str],
        previous_title: str | None,
        previous_represents_keyword_id: UUID | None,
        current_targets: list[str],
        current_title: str | None,
        current_represents_keyword_id: UUID | None,
    ) -> None:
        previous_cleanup_names = self._collect_cleanup_keyword_names(
            link_targets=previous_targets,
            represents_keyword_id=previous_represents_keyword_id,
            title=previous_title,
        )
        current_cleanup_names = self._collect_cleanup_keyword_names(
            link_targets=current_targets,
            represents_keyword_id=current_represents_keyword_id,
            title=current_title,
        )
        removed_targets = [
            title for title in previous_cleanup_names
            if title not in set(current_cleanup_names)
        ]
        await self._keywords_repo.delete_unused_keywords(
            user_id=user_id,
            names=removed_targets,
        )

    async def create_note(self, note_data: CreateNote) -> UUID:
        user = await self._get_user_or_raise(note_data.by_user_telegram_id)

        existing_count = 0
        if note_data.represents_keyword:
            existing_count = await self._notes_repo.count_keyword_notes_by_user_and_title(
                user_id=user.id,
                title=note_data.title or "",
            )
        self._validate_keyword_note(
            title=note_data.title,
            represents_keyword=note_data.represents_keyword,
            existing_count=existing_count,
        )

        represents_keyword_id = await self._prepare_represents_keyword_id_for_create(
            user_id=user.id,
            title=note_data.title,
            represents_keyword=note_data.represents_keyword,
        )
        note = Note(
            id=uuid4(),
            user_id=user.id,
            title=note_data.title,
            text=note_data.text,
            represents_keyword_id=represents_keyword_id,
        )
        await self._notes_repo.create(note)
        await self._notes_graph_repo.upsert_note(note)
        link_targets = extract_link_targets(note.text or "")
        await self._sync_note_keywords_and_graph(note, link_targets)

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
        cleanup_names = self._collect_cleanup_keyword_names(
            link_targets=link_targets,
            represents_keyword_id=note.represents_keyword_id,
            title=note.title,
        )
        await self._notes_repo.delete_by_id(note_id)
        await self._keywords_repo.delete_note_keywords(note_id)
        await self._keywords_repo.delete_unused_keywords(
            user_id=note.user_id,
            names=cleanup_names,
        )
        await self._notes_graph_repo.delete_note(note_id)

    async def update_note(self, note_data: UpdateNote) -> Note:
        note = await self._notes_repo.get_by_id(note_data.note_id)
        if note is None:
            raise NoteNotFoundException()

        previous_targets, previous_title, previous_represents_keyword_id = (
            await self._apply_note_updates(note, note_data)
        )

        existing_count = 0
        if note.represents_keyword_id is not None:
            existing_count = await self._notes_repo.count_keyword_notes_by_user_and_title(
                user_id=note.user_id,
                title=note.title or "",
                exclude_note_id=note.id,
            )
            await self._ensure_unique_keyword_note(
                user_id=note.user_id,
                keyword_id=note.represents_keyword_id,
                exclude_note_id=note.id,
            )
        self._validate_keyword_note(
            title=note.title,
            represents_keyword=note.represents_keyword_id is not None,
            existing_count=existing_count,
        )

        await self._notes_repo.update(note)
        await self._notes_graph_repo.upsert_note(note)
        link_targets = extract_link_targets(note.text or "")
        await self._sync_note_keywords_and_graph(
            note,
            link_targets,
            previous_title=previous_title,
            previous_represents_keyword_id=previous_represents_keyword_id,
        )
        await self._cleanup_removed_keywords(
            user_id=note.user_id,
            previous_targets=previous_targets,
            previous_title=previous_title,
            previous_represents_keyword_id=previous_represents_keyword_id,
            current_targets=link_targets,
            current_title=note.title,
            current_represents_keyword_id=note.represents_keyword_id,
        )

        return note
