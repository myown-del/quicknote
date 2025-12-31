from uuid import UUID

from brain.application.abstractions.repositories.models import WikilinkSuggestion
from brain.application.abstractions.repositories.notes import INotesRepository


class SearchWikilinkSuggestionsInteractor:
    def __init__(self, notes_repo: INotesRepository):
        self._notes_repo = notes_repo

    async def search_wikilink_suggestions(
        self,
        user_id: UUID,
        query: str,
    ) -> list[WikilinkSuggestion]:
        return await self._notes_repo.search_wikilink_suggestions(
            user_id=user_id,
            query=query,
        )
