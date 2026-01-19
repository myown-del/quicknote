from datetime import datetime

from tests.integration.api.notes.helpers import create_keyword_note


async def test_get_note_creation_stats(notes_app, api_client, repo_hub, user):
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Note 1",
        created_at=datetime(2024, 1, 1, 10, 0, 0),
        updated_at=datetime(2024, 1, 1, 10, 0, 0),
    )
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Note 2",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        updated_at=datetime(2024, 1, 1, 12, 0, 0),
    )
    await create_keyword_note(
        repo_hub=repo_hub,
        user=user,
        title="Note 3",
        created_at=datetime(2024, 1, 2, 9, 0, 0),
        updated_at=datetime(2024, 1, 2, 9, 0, 0),
    )

    async with api_client(notes_app) as client:
        response = await client.get("/api/notes/creation-stats")

    assert response.status_code == 200
    assert response.json() == [
        {"date": "2024-01-01", "count": 2},
        {"date": "2024-01-02", "count": 1},
    ]
