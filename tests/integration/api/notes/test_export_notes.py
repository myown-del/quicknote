from unittest.mock import AsyncMock

from starlette import status


def test_export_notes(notes_api_client):
    # setup: mock export interactor
    client, mocks, user = notes_api_client
    zip_bytes = b"fake-zip"
    mocks.export_notes.export_notes = AsyncMock(return_value=zip_bytes)

    # action: request export
    response = client.request("GET", "/api/notes/export")

    # check: response headers and content
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/zip"
    assert response.headers["content-disposition"] == "attachment; filename=notes_export.zip"
    assert response.content == zip_bytes
    mocks.export_notes.export_notes.assert_awaited_once_with(user.telegram_id)
