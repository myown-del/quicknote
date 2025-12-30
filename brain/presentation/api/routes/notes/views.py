from dataclasses import asdict
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, APIRouter, HTTPException
from starlette import status

from brain.application.interactors import NoteInteractor
from brain.application.interactors.notes.dto import CreateNote, UpdateNote
from brain.application.interactors.notes.exceptions import NoteNotFoundException
from brain.domain.entities.user import User
from brain.presentation.api.dependencies.auth import get_user_from_request
from brain.presentation.api.routes.notes.models import (
    ReadNoteSchema,
    CreateNoteSchema,
    UpdateNoteSchema,
)


@inject
async def get_notes(
        interactor: FromDishka[NoteInteractor],
        user: User = Depends(get_user_from_request),
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
        user: User = Depends(get_user_from_request),
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
        user: User = Depends(get_user_from_request),
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


@inject
async def update_note(
        interactor: FromDishka[NoteInteractor],
        note_id: UUID,
        note: UpdateNoteSchema,
        user: User = Depends(get_user_from_request),
):
    existing_note = await interactor.get_note_by_id(note_id)
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

    payload = note.model_dump(exclude_unset=True)
    data = UpdateNote(
        note_id=note_id,
        title=payload.get("title", existing_note.title),
        text=payload.get("text", existing_note.text),
    )

    try:
        updated_note = await interactor.update_note(data)
    except NoteNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    return ReadNoteSchema.model_validate(asdict(updated_note))


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
    router.add_api_route(
        path='/{note_id}',
        endpoint=update_note,
        methods=["PATCH"],
        response_model=ReadNoteSchema,
        summary="Update note",
        status_code=status.HTTP_200_OK
    )
    return router
