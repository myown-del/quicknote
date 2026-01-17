from unittest.mock import AsyncMock

from starlette import status

from brain.application.abstractions.repositories.models import WikilinkSuggestion


def test_get_wikilink_suggestions(notes_api_client):
    # setup: mock suggestions returned by interactor
    client, mocks, user = notes_api_client
    suggestions = [
        WikilinkSuggestion(title="Alpha", represents_keyword=True),
        WikilinkSuggestion(title="Beta", represents_keyword=False),
    ]
    mocks.search_wikilinks.search_wikilink_suggestions = AsyncMock(
        return_value=suggestions
    )

    # action: request wikilink suggestions
    response = client.request(
        "GET",
        "/api/notes/wikilink-suggestions?query=Al",
    )

    # check: response and interactor call
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload == [
        {"title": "Alpha", "represents_keyword": True},
        {"title": "Beta", "represents_keyword": False},
    ]
    mocks.search_wikilinks.search_wikilink_suggestions.assert_awaited_once_with(
        user_id=user.id,
        query="Al",
    )
