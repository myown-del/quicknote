from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock

import pytest
from starlette import status

from brain.application.interactors.notes.dto import UpdateNote
from brain.application.interactors.notes.exceptions import (
    KeywordNotFoundException,
    NoteNotFoundException,
    NoteTitleAlreadyExistsException,
    NoteTitleRequiredException,
)
from brain.domain.entities.note import Note


def make_note(user_id, title="Note title", text="Note text"):
    now = datetime(2024, 1, 2, 3, 4, 5)
    return Note(
        id=uuid4(),
        user_id=user_id,
        title=title,
        text=text,
        represents_keyword_id=uuid4(),
        created_at=now,
        updated_at=now,
    )


def test_update_note_success(notes_api_client):
    # setup: mock get and update interactors
    client, mocks, user = notes_api_client
    existing_note = make_note(user.id, title="Old")
    updated_note = make_note(user.id, title="New")
    note_id = existing_note.id
    mocks.get_note.get_note_by_id = AsyncMock(return_value=existing_note)
    mocks.update_note.update_note = AsyncMock(return_value=updated_note)

    # action: update note via API
    response = client.request(
        "PATCH",
        f"/api/notes/{note_id}",
        json={"title": "New"},
    )

    # check: response payload and interactor args
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["id"] == str(updated_note.id)
    assert payload["title"] == "New"

    update_args = mocks.update_note.update_note.call_args[0]
    assert isinstance(update_args[0], UpdateNote)
    assert update_args[0].note_id == note_id
    assert update_args[0].title == "New"


def test_update_note_not_found(notes_api_client):
    # setup: mock missing note
    client, mocks, _ = notes_api_client
    note_id = uuid4()
    mocks.get_note.get_note_by_id = AsyncMock(return_value=None)

    # action: update a missing note
    response = client.request(
        "PATCH",
        f"/api/notes/{note_id}",
        json={"title": "New"},
    )

    # check: not found response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Note not found"


def test_update_note_forbidden(notes_api_client):
    # setup: mock note belonging to another user
    client, mocks, _ = notes_api_client
    note = make_note(uuid4())
    note_id = note.id
    mocks.get_note.get_note_by_id = AsyncMock(return_value=note)

    # action: update note not owned by user
    response = client.request(
        "PATCH",
        f"/api/notes/{note_id}",
        json={"title": "New"},
    )

    # check: forbidden response
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Forbidden"


@pytest.mark.parametrize(
    "exception,detail",
    [
        (NoteTitleRequiredException(), "Note title cannot be null"),
        (NoteTitleAlreadyExistsException(), "Note title must be unique"),
        (KeywordNotFoundException(), "Keyword not found"),
    ],
)
def test_update_note_errors(notes_api_client, exception, detail):
    # setup: mock update interactor failure
    client, mocks, user = notes_api_client
    note = make_note(user.id)
    note_id = note.id
    mocks.get_note.get_note_by_id = AsyncMock(return_value=note)
    mocks.update_note.update_note = AsyncMock(side_effect=exception)

    # action: update note with invalid data
    response = client.request(
        "PATCH",
        f"/api/notes/{note_id}",
        json={"title": "New"},
    )

    # check: error response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == detail


def test_update_note_interactor_not_found(notes_api_client):
    # setup: mock delete interactor not found error
    client, mocks, user = notes_api_client
    note = make_note(user.id)
    note_id = note.id
    mocks.get_note.get_note_by_id = AsyncMock(return_value=note)
    mocks.update_note.update_note = AsyncMock(side_effect=NoteNotFoundException())

    # action: update note that interactor cannot find
    response = client.request(
        "PATCH",
        f"/api/notes/{note_id}",
        json={"title": "New"},
    )

    # check: not found response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Note not found"
