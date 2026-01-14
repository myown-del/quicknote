from dataclasses import asdict

from uuid import UUID

from brain.application.interactors.notes.dto import CreateNote, UpdateNote
from brain.domain.entities.note import Note
from brain.domain.entities.user import User
from brain.presentation.api.routes.notes.models import (
    CreateNoteSchema,
    ReadNoteSchema,
    UpdateNoteSchema,
    WikilinkSuggestionSchema,
)
from brain.application.abstractions.repositories.models import WikilinkSuggestion
from brain.application.types import Unset


def map_note_to_read_schema(note: Note) -> ReadNoteSchema:
    payload = asdict(note)
    payload.pop("represents_keyword_id", None)
    return ReadNoteSchema.model_validate(payload)


def map_create_schema_to_dto(
    schema: CreateNoteSchema,
    user: User,
) -> CreateNote:
    return CreateNote(
        by_user_telegram_id=user.telegram_id,
        title=schema.title,
        text=schema.text,
    )


def map_update_schema_to_dto(
    note_id: UUID,
    schema: UpdateNoteSchema,
) -> UpdateNote:
    payload = schema.model_dump(exclude_unset=True)
    return UpdateNote(
        note_id=note_id,
        title=payload.get("title", Unset),
        text=payload.get("text", Unset),
        patch=payload.get("patch", Unset),
    )


def map_wikilink_suggestion_to_schema(
    suggestion: WikilinkSuggestion,
) -> WikilinkSuggestionSchema:
    return WikilinkSuggestionSchema.model_validate(asdict(suggestion))
