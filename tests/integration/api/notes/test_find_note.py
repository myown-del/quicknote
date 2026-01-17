import pytest
from starlette import status

from brain.infrastructure.db.repositories.hub import RepositoryHub
from tests.integration.api.notes.helpers import create_keyword_note


@pytest.mark.asyncio
async def test_search_notes_default_exact_match(
    notes_app,
    api_client,
    repo_hub: RepositoryHub,
    user,
):
    # setup: create notes with similar titles
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Test Note",
        text="Content",
    )
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Test Note Extended",
        text="Content",
    )

    # action: request search without exact_match
    async with api_client(notes_app) as client:
        response = await client.request(
            method="GET",
            url="/api/notes/search/by-title?query=Test Note",
        )

    # check: both notes are returned
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    titles = {item["title"] for item in payload}
    assert titles == {"Test Note", "Test Note Extended"}


@pytest.mark.asyncio
async def test_search_notes_exact_match_true(
    notes_app,
    api_client,
    repo_hub: RepositoryHub,
    user,
):
    # setup: create notes with similar titles
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Test Note",
        text="Content",
    )
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Test Note Extended",
        text="Content",
    )

    # action: request search with exact_match=true
    async with api_client(notes_app) as client:
        response = await client.request(
            method="GET",
            url="/api/notes/search/by-title?query=Test Note&exact_match=true",
        )

    # check: only exact title match returned
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert [item["title"] for item in payload] == ["Test Note"]


@pytest.mark.asyncio
async def test_search_notes_exact_match_explicit_false(
    notes_app,
    api_client,
    repo_hub: RepositoryHub,
    user,
):
    # setup: create notes with similar titles
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Test Note",
        text="Content",
    )
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Test Note Extended",
        text="Content",
    )

    # action: request search with exact_match=false
    async with api_client(notes_app) as client:
        response = await client.request(
            method="GET",
            url="/api/notes/search/by-title?query=Test Note&exact_match=false",
        )

    # check: both notes are returned
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    titles = {item["title"] for item in payload}
    assert titles == {"Test Note", "Test Note Extended"}
