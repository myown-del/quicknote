from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock

from starlette import status

from brain.application.interactors.notes.exceptions import NoteNotFoundException
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


def test_delete_note_success(notes_api_client):
    # setup: mock get and delete interactors
    client, mocks, user = notes_api_client
    note = make_note(user.id)
    note_id = note.id
    mocks.get_note.get_note_by_id = AsyncMock(return_value=note)
    mocks.delete_note.delete_note = AsyncMock(return_value=None)

    # action: delete existing note
    response = client.request("DELETE", f"/api/notes/{note_id}")

    # check: successful delete and interactor call
    assert response.status_code == status.HTTP_204_NO_CONTENT
    mocks.delete_note.delete_note.assert_awaited_once_with(note_id)


def test_delete_note_not_found(notes_api_client):
    # setup: mock missing note
    client, mocks, _ = notes_api_client
    note_id = uuid4()
    mocks.get_note.get_note_by_id = AsyncMock(return_value=None)

    # action: delete a missing note
    response = client.request("DELETE", f"/api/notes/{note_id}")

    # check: not found response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Note not found"


def test_delete_note_forbidden(notes_api_client):
    # setup: mock note belonging to another user
    client, mocks, user = notes_api_client
    note = make_note(uuid4())
    note_id = note.id
    mocks.get_note.get_note_by_id = AsyncMock(return_value=note)

    # action: delete note not owned by user
    response = client.request("DELETE", f"/api/notes/{note_id}")

    # check: forbidden response
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Forbidden"


def test_delete_note_interactor_not_found(notes_api_client):
    # setup: mock get note and delete interactor error
    client, mocks, user = notes_api_client
    note = make_note(user.id)
    note_id = note.id
    mocks.get_note.get_note_by_id = AsyncMock(return_value=note)
    mocks.delete_note.delete_note = AsyncMock(side_effect=NoteNotFoundException())

    # action: delete note that interactor cannot find
    response = client.request("DELETE", f"/api/notes/{note_id}")

    # check: not found response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Note not found"
