from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock

from starlette import status

from brain.domain.entities.note import Note


def make_note(user_id, title):
    now = datetime(2024, 1, 2, 3, 4, 5)
    return Note(
        id=uuid4(),
        user_id=user_id,
        title=title,
        text="Content",
        represents_keyword_id=uuid4(),
        created_at=now,
        updated_at=now,
    )


def test_search_notes_by_title_default_exact_match(notes_api_client):
    # setup: mock interactor result
    client, mocks, user = notes_api_client
    note = make_note(user.id, title="Test Note")
    mocks.search_by_title.search = AsyncMock(return_value=[note])

    # action: request search without exact_match
    response = client.request(
        "GET",
        "/api/notes/search/by-title?query=Test Note",
    )

    # check: response payload and interactor args
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["title"] == "Test Note"
    args, kwargs = mocks.search_by_title.search.call_args
    assert kwargs["user_id"] == user.id
    assert kwargs["query"] == "Test Note"
    assert kwargs["exact_match"] is False


def test_search_notes_by_title_exact_match_true(notes_api_client):
    # setup: mock interactor result
    client, mocks, user = notes_api_client
    note = make_note(user.id, title="Test Note")
    mocks.search_by_title.search = AsyncMock(return_value=[note])

    # action: request search with exact_match=true
    response = client.request(
        "GET",
        "/api/notes/search/by-title?query=Test Note&exact_match=true",
    )

    # check: response payload and interactor args
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload[0]["title"] == "Test Note"
    args, kwargs = mocks.search_by_title.search.call_args
    assert kwargs["user_id"] == user.id
    assert kwargs["query"] == "Test Note"
    assert kwargs["exact_match"] is True
