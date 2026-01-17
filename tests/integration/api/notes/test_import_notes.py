from unittest.mock import AsyncMock

from starlette import status


def test_import_notes_success(notes_api_client):
    # setup: mock import interactor
    client, mocks, user = notes_api_client
    mocks.import_notes.import_notes = AsyncMock(return_value=None)

    # action: upload zip file
    response = client.request(
        "POST",
        "/api/notes/import",
        files={"file": ("notes.zip", b"zip-contents", "application/zip")},
    )

    # check: response and interactor args
    assert response.status_code == status.HTTP_204_NO_CONTENT
    args = mocks.import_notes.import_notes.call_args[0]
    assert args[0] == user.telegram_id
    assert args[1] == b"zip-contents"


def test_import_notes_invalid_extension(notes_api_client):
    # setup: no interactor call expected
    client, mocks, _ = notes_api_client

    # action: upload non-zip file
    response = client.request(
        "POST",
        "/api/notes/import",
        files={"file": ("notes.txt", b"content", "text/plain")},
    )

    # check: validation error and no interactor calls
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "File must be a .zip extension"
    assert mocks.import_notes.import_notes.call_count == 0


def test_import_notes_invalid_zip(notes_api_client):
    # setup: mock interactor zip failure
    client, mocks, _ = notes_api_client
    mocks.import_notes.import_notes = AsyncMock(side_effect=ValueError())

    # action: upload invalid zip
    response = client.request(
        "POST",
        "/api/notes/import",
        files={"file": ("notes.zip", b"bad-zip", "application/zip")},
    )

    # check: error response for invalid zip
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Invalid zip file"
