from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Query
from starlette import status

from brain.application.interactors import GetGraphInteractor
from brain.domain.entities.user import User
from brain.presentation.api.dependencies.auth import get_user_from_request
from brain.presentation.api.routes.graph.mappers import map_graph_to_schema
from brain.presentation.api.routes.graph.models import GraphSchema


@inject
async def get_graph(
    interactor: FromDishka[GetGraphInteractor],
    query: str | None = Query(default=None, min_length=1),
    depth: int = Query(default=1, ge=0),
    user: User = Depends(get_user_from_request),
) -> GraphSchema:
    graph = await interactor.get_graph(
        user_id=user.id,
        query=query,
        depth=depth,
    )
    return map_graph_to_schema(graph)


def get_router() -> APIRouter:
    router = APIRouter(prefix="/graph", tags=["Graph"])
    router.add_api_route(
        path="",
        endpoint=get_graph,
        methods=["GET"],
        response_model=GraphSchema,
        summary="Get graph nodes and connections",
        status_code=status.HTTP_200_OK,
    )
    return router
