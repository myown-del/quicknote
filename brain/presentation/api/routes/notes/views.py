from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, APIRouter, HTTPException, Query
from starlette import status

from brain.application.interactors import (
    CreateNoteInteractor,
    DeleteNoteInteractor,
    GetNoteInteractor,
    GetNotesInteractor,
    SearchWikilinkSuggestionsInteractor,
    UpdateNoteInteractor,
)
from brain.application.interactors.notes.exceptions import (
    NoteNotFoundException,
    KeywordNoteTitleRequiredException,
    KeywordNoteAlreadyExistsException,
    KeywordNotFoundException,
)
from brain.domain.entities.user import User
from brain.presentation.api.dependencies.auth import get_user_from_request
from brain.presentation.api.routes.notes.mappers import (
    map_create_schema_to_dto,
    map_note_to_read_schema,
    map_update_schema_to_dto,
    map_wikilink_suggestion_to_schema,
)
from brain.presentation.api.routes.notes.models import (
    ReadNoteSchema,
    CreateNoteSchema,
    UpdateNoteSchema,
    WikilinkSuggestionSchema,
)


@inject
async def get_notes(
        interactor: FromDishka[GetNotesInteractor],
        user: User = Depends(get_user_from_request),
):
    notes = await interactor.get_notes(user.telegram_id)
    return [
        map_note_to_read_schema(note)
        for note in notes
    ]


@inject
async def get_wikilink_suggestions(
        interactor: FromDishka[SearchWikilinkSuggestionsInteractor],
        query: str = Query(..., min_length=1),
        user: User = Depends(get_user_from_request),
):
    suggestions = await interactor.search_wikilink_suggestions(
        user_id=user.id,
        query=query,
    )
    return [
        map_wikilink_suggestion_to_schema(suggestion)
        for suggestion in suggestions
    ]


@inject
async def create_note(
        create_interactor: FromDishka[CreateNoteInteractor],
        get_note_interactor: FromDishka[GetNoteInteractor],
        note: CreateNoteSchema,
        user: User = Depends(get_user_from_request),
):
    data = map_create_schema_to_dto(note, user)
    try:
        note_id = await create_interactor.create_note(data)
    except KeywordNoteTitleRequiredException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keyword note requires a title",
        )
    except KeywordNoteAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keyword note with this title already exists",
        )
    except KeywordNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keyword not found",
        )
    note = await get_note_interactor.get_note_by_id(note_id)
    return map_note_to_read_schema(note)


@inject
async def delete_note(
        get_note_interactor: FromDishka[GetNoteInteractor],
        delete_interactor: FromDishka[DeleteNoteInteractor],
        note_id: UUID,
        user: User = Depends(get_user_from_request),
):
    note = await get_note_interactor.get_note_by_id(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    if note.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    try:
        await delete_interactor.delete_note(note_id)
    except NoteNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )


@inject
async def update_note(
        get_note_interactor: FromDishka[GetNoteInteractor],
        update_interactor: FromDishka[UpdateNoteInteractor],
        note_id: UUID,
        note: UpdateNoteSchema,
        user: User = Depends(get_user_from_request),
):
    existing_note = await get_note_interactor.get_note_by_id(note_id)
    if not existing_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    if existing_note.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    data = map_update_schema_to_dto(note_id, note, existing_note)

    try:
        updated_note = await update_interactor.update_note(data)
    except NoteNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    except KeywordNoteTitleRequiredException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keyword note requires a title",
        )
    except KeywordNoteAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keyword note with this title already exists",
        )
    except KeywordNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keyword not found",
        )

    return map_note_to_read_schema(updated_note)


def get_router() -> APIRouter:
    router = APIRouter(prefix='/notes')
    router.add_api_route(
        path='',
        endpoint=get_notes,
        methods=["GET"],
        response_model=list[ReadNoteSchema],
        summary="Get user notes",
        status_code=status.HTTP_200_OK
    )
    router.add_api_route(
        path='/wikilink-suggestions',
        endpoint=get_wikilink_suggestions,
        methods=["GET"],
        response_model=list[WikilinkSuggestionSchema],
        summary="Search wikilink suggestions",
        status_code=status.HTTP_200_OK
    )
    router.add_api_route(
        path='',
        endpoint=create_note,
        methods=["POST"],
        response_model=ReadNoteSchema,
        summary="Create note",
        status_code=status.HTTP_201_CREATED
    )
    router.add_api_route(
        path='/{note_id}',
        endpoint=delete_note,
        methods=["DELETE"],
        summary="Delete note",
        status_code=status.HTTP_204_NO_CONTENT
    )
    router.add_api_route(
        path='/{note_id}',
        endpoint=update_note,
        methods=["PATCH"],
        response_model=ReadNoteSchema,
        summary="Update note",
        status_code=status.HTTP_200_OK
    )
    return router
