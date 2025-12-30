from dataclasses import asdict
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status

from quicknote.application.interactors import NoteInteractor
from quicknote.application.interactors.notes.dto import CreateNote
from quicknote.application.interactors.notes.exceptions import NoteNotFoundException
from quicknote.domain.entities.user import UserDM
from quicknote.presentation.api.dependencies.auth import get_user_from_request
from quicknote.presentation.api.routes.notes.models import ReadNoteSchema, CreateNoteSchema


@inject
async def get_notes(
        interactor: FromDishka[NoteInteractor],
        user: UserDM = Depends(get_user_from_request),
):
    notes = await interactor.get_notes(user.telegram_id)
    return [
        ReadNoteSchema.model_validate(asdict(note))
        for note in notes
    ]


@inject
async def create_note(
        interactor: FromDishka[NoteInteractor],
        note: CreateNoteSchema,
        user: UserDM = Depends(get_user_from_request),
):
    data = CreateNote(
        by_user_telegram_id=user.telegram_id,
        title=note.title,
        text=note.text
    )
    note_id = await interactor.create_note(data)
    note = await interactor.get_note_by_id(note_id)
    return ReadNoteSchema.model_validate(asdict(note))


@inject
async def delete_note(
        interactor: FromDishka[NoteInteractor],
        note_id: UUID,
        user: UserDM = Depends(get_user_from_request),
):
    note = await interactor.get_note_by_id(note_id)
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
        await interactor.delete_note(note_id)
    except NoteNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )


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
    return router
