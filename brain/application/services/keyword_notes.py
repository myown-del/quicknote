from uuid import UUID

from brain.application.abstractions.repositories.keywords import IKeywordsRepository
from brain.application.abstractions.repositories.notes import INotesRepository
from brain.application.interactors.notes.exceptions import (
    KeywordNoteAlreadyExistsException,
    KeywordNoteTitleRequiredException,
    KeywordNotFoundException,
)


class KeywordNoteService:
    def __init__(
        self,
        notes_repo: INotesRepository,
        keywords_repo: IKeywordsRepository,
    ):
        self._notes_repo = notes_repo
        self._keywords_repo = keywords_repo

    async def validate_keyword_note(
        self,
        user_id: UUID,
        title: str | None,
        represents_keyword: bool,
        exclude_note_id: UUID | None = None,
    ) -> UUID | None:
        if not represents_keyword:
            return None

        if not title:
            raise KeywordNoteTitleRequiredException()

        keyword = await self._keywords_repo.get_by_user_and_name(user_id, name=title)
        if not keyword:
            await self._keywords_repo.ensure_keywords(user_id=user_id, names=[title])
            keyword = await self._keywords_repo.get_by_user_and_name(
                user_id, name=title
            )

        if not keyword:
            raise KeywordNotFoundException()

        existing_count = (
            await self._notes_repo.count_keyword_notes_by_user_and_keyword_id(
                user_id=user_id,
                keyword_id=keyword.id,
                exclude_note_id=exclude_note_id,
            )
        )
        if existing_count > 0:
            raise KeywordNoteAlreadyExistsException()

        return keyword.id
