from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock

from starlette import status

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


def test_get_notes_with_date_filters(notes_api_client):
    # setup: prepare note and mock interactor result
    client, mocks, user = notes_api_client
    note = make_note(user.id)
    mocks.get_notes.get_notes = AsyncMock(return_value=[note])

    # action: request notes with date filters
    from_date = "2024-01-01T10:11:12"
    to_date = "2024-01-03T12:13:14"
    response = client.request(
        "GET",
        f"/api/notes?from_date={from_date}&to_date={to_date}",
    )

    # check: response payload and interactor call
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload[0]["id"] == str(note.id)
    assert payload[0]["title"] == note.title
    assert payload[0]["text"] == note.text
    assert payload[0]["created_at"] == note.created_at.isoformat()
    assert payload[0]["updated_at"] == note.updated_at.isoformat()

    args, kwargs = mocks.get_notes.get_notes.call_args
    assert args[0] == user.telegram_id
    assert kwargs["from_date"].isoformat() == from_date
    assert kwargs["to_date"].isoformat() == to_date
