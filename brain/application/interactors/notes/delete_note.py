from uuid import UUID

from brain.application.abstractions.repositories.keywords import IKeywordsRepository
from brain.application.abstractions.repositories.notes import INotesRepository
from brain.application.abstractions.repositories.notes_graph import (
    INotesGraphRepository,
)
from brain.application.interactors.notes.exceptions import NoteNotFoundException
from brain.domain.services.wikilinks import extract_link_targets

from brain.domain.services.keywords import collect_cleanup_keyword_names


class DeleteNoteInteractor:
    def __init__(
        self,
        notes_repo: INotesRepository,
        keywords_repo: IKeywordsRepository,
        notes_graph_repo: INotesGraphRepository,
    ):
        self._notes_repo = notes_repo
        self._keywords_repo = keywords_repo
        self._notes_graph_repo = notes_graph_repo

    async def delete_note(self, note_id: UUID) -> None:
        note = await self._notes_repo.get_by_id(note_id)
        if note is None:
            raise NoteNotFoundException()

        link_targets = extract_link_targets(note.text or "")
        cleanup_names = collect_cleanup_keyword_names(
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
