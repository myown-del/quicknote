from uuid import UUID

from brain.application.abstractions.repositories.notes_graph import INotesGraphRepository
from brain.domain.entities.graph import GraphData


class GetGraphInteractor:
    def __init__(self, notes_graph_repo: INotesGraphRepository):
        self._notes_graph_repo = notes_graph_repo

    async def get_graph(
        self,
        user_id: UUID,
        query: str | None = None,
        depth: int = 1,
    ) -> GraphData:
        return await self._notes_graph_repo.get_graph(
            user_id=user_id,
            query=query,
            depth=depth,
        )
