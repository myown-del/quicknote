from datetime import datetime

import pytest
from starlette import status

from brain.infrastructure.db.repositories.hub import RepositoryHub
from tests.integration.api.notes.helpers import create_keyword_note


@pytest.mark.asyncio
async def test_get_notes_with_date_filters(
    notes_app,
    api_client,
    repo_hub: RepositoryHub,
    user,
):
    # setup: create notes with different timestamps
    in_range_created = datetime(
        year=2024,
        month=1,
        day=2,
        hour=3,
        minute=4,
        second=5,
    )
    out_range_created = datetime(
        year=2024,
        month=2,
        day=2,
        hour=3,
        minute=4,
        second=5,
    )
    in_range_note = await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="In Range",
        text="Note text",
        created_at=in_range_created,
        updated_at=in_range_created,
    )
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Out Range",
        text="Note text",
        created_at=out_range_created,
        updated_at=out_range_created,
    )

    # action: request notes with date filters
    from_date = "2024-01-01T10:11:12"
    to_date = "2024-01-03T12:13:14"
    async with api_client(notes_app) as client:
        response = await client.request(
            method="GET",
            url=f"/api/notes?from_date={from_date}&to_date={to_date}",
        )

    # check: only notes inside the range are returned
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    returned_ids = {item["id"] for item in payload}
    assert returned_ids == {str(in_range_note.id)}
