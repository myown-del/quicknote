from unittest.mock import MagicMock, AsyncMock
import pytest
from fastapi.testclient import TestClient
from dishka import make_async_container, Provider, Scope, provide
from dishka.integrations.fastapi import setup_dishka
from uuid import uuid4
from datetime import datetime

from brain.presentation.api.factory import create_bare_app
from brain.config.models import Config, APIConfig, S3Config
from brain.application.interactors.notes.search_notes_by_title import SearchNotesByTitleInteractor
from brain.domain.entities.note import Note
from brain.domain.entities.user import User
from brain.presentation.api.dependencies.auth import get_user_from_request

@pytest.fixture
def mock_search_notes_interactor():
    return MagicMock(spec=SearchNotesByTitleInteractor)

@pytest.fixture
def client(mock_search_notes_interactor, event_loop):
    # Mock Config
    mock_config = MagicMock(spec=Config)
    mock_config.api = APIConfig(
        internal_host="0.0.0.0",
        external_host="localhost",
        port=8080
    )
    # Mock S3 Config
    mock_config.s3 = S3Config(
        external_host="http://localhost:9000",
        endpoint_url="http://test",
        access_key_id="test",
        secret_access_key="test",
        bucket_name="test-bucket"
    )

    # Provider
    class MockProvider(Provider):
        scope = Scope.APP

        @provide
        def get_interactor(self) -> SearchNotesByTitleInteractor:
            return mock_search_notes_interactor

    # App
    app = create_bare_app(mock_config.api)
    
    # Override auth dependency
    user = User(
        id=uuid4(),
        telegram_id=12345,
        created_at=datetime.utcnow(),
        first_name="Test User"
    )
    app.dependency_overrides[get_user_from_request] = lambda: user

    # Container
    container = make_async_container(MockProvider())
    setup_dishka(container, app)

    with TestClient(app) as client:
        yield client

    event_loop.run_until_complete(container.close())

def test_search_notes_default_exact_match(client, mock_search_notes_interactor):
    note_id = uuid4()
    title = "Test Note"
    note = Note(
        id=note_id,
        user_id=uuid4(),
        title=title,
        text="Content",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        represents_keyword_id=None
    )
    
    mock_search_notes_interactor.search = AsyncMock(return_value=[note])

    response = client.get(f"/api/notes/search/by-title?query={title}")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 1
    assert payload[0]["title"] == title
    args, kwargs = mock_search_notes_interactor.search.call_args
    assert kwargs['query'] == title
    assert kwargs['exact_match'] is False

def test_search_notes_exact_match_true(client, mock_search_notes_interactor):
    note_id = uuid4()
    title = "Test Note"
    note = Note(
        id=note_id,
        user_id=uuid4(),
        title=title,
        text="Content",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        represents_keyword_id=None
    )
    
    mock_search_notes_interactor.search = AsyncMock(return_value=[note])

    response = client.get(f"/api/notes/search/by-title?query={title}&exact_match=true")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["title"] == title
    args, kwargs = mock_search_notes_interactor.search.call_args
    assert kwargs['query'] == title
    assert kwargs['exact_match'] is True

def test_search_notes_exact_match_explicit_false(client, mock_search_notes_interactor):
    note_id = uuid4()
    title = "Test Note"
    note = Note(
        id=note_id,
        user_id=uuid4(),
        title=title,
        text="Content",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        represents_keyword_id=None
    )
    
    mock_search_notes_interactor.search = AsyncMock(return_value=[note])

    response = client.get(f"/api/notes/search/by-title?query={title}&exact_match=false")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["title"] == title
    args, kwargs = mock_search_notes_interactor.search.call_args
    assert kwargs['query'] == title
    assert kwargs['exact_match'] is False
