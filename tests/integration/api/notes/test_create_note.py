from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock

import pytest
from starlette import status

from brain.application.interactors.notes.dto import CreateNote
from brain.application.interactors.notes.exceptions import (
    KeywordNotFoundException,
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


def test_create_note_success(notes_api_client):
    # setup: mock create and get note interactors
    client, mocks, user = notes_api_client
    note_id = uuid4()
    note = make_note(user.id, title="New Note", text="Body")
    mocks.create_note.create_note = AsyncMock(return_value=note_id)
    mocks.get_note.get_note_by_id = AsyncMock(return_value=note)

    # action: create note via API
    response = client.request(
        "POST",
        "/api/notes",
        json={"title": "New Note", "text": "Body"},
    )

    # check: response and interactor args
    assert response.status_code == status.HTTP_201_CREATED
    payload = response.json()
    assert payload["id"] == str(note.id)
    assert payload["title"] == "New Note"
    assert payload["text"] == "Body"

    create_args = mocks.create_note.create_note.call_args[0]
    assert isinstance(create_args[0], CreateNote)
    assert create_args[0].by_user_telegram_id == user.telegram_id
    assert create_args[0].title == "New Note"
    assert create_args[0].text == "Body"
    mocks.get_note.get_note_by_id.assert_awaited_once_with(note_id)


@pytest.mark.parametrize(
    "exception,detail",
    [
        (NoteTitleRequiredException(), "Note title cannot be null"),
        (NoteTitleAlreadyExistsException(), "Note title must be unique"),
        (KeywordNotFoundException(), "Keyword not found"),
    ],
)
def test_create_note_errors(notes_api_client, exception, detail):
    # setup: configure interactor to raise an error
    client, mocks, _ = notes_api_client
    mocks.create_note.create_note = AsyncMock(side_effect=exception)

    # action: attempt to create an invalid note
    response = client.request(
        "POST",
        "/api/notes",
        json={"title": None, "text": "Body"},
    )

    # check: correct error response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == detail
