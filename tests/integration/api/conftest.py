from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

import pytest
from dishka import Provider, Scope, provide, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient

from brain.application.interactors import (
    CreateNoteInteractor,
    DeleteNoteInteractor,
    ExportNotesInteractor,
    GetNoteInteractor,
    GetNotesInteractor,
    ImportNotesInteractor,
    SearchNotesByTitleInteractor,
    SearchWikilinkSuggestionsInteractor,
    UpdateNoteInteractor,
)
from brain.config.models import APIConfig
from brain.domain.entities.user import User
from brain.presentation.api.dependencies.auth import get_user_from_request
from brain.presentation.api.factory import create_bare_app


class NotesApiMocks:
    def __init__(self) -> None:
        self.get_notes = MagicMock(spec=GetNotesInteractor)
        self.get_notes.get_notes = AsyncMock(return_value=[])

        self.search_wikilinks = MagicMock(spec=SearchWikilinkSuggestionsInteractor)
        self.search_wikilinks.search_wikilink_suggestions = AsyncMock(return_value=[])

        self.search_by_title = MagicMock(spec=SearchNotesByTitleInteractor)
        self.search_by_title.search = AsyncMock(return_value=[])

        self.create_note = MagicMock(spec=CreateNoteInteractor)
        self.create_note.create_note = AsyncMock()

        self.get_note = MagicMock(spec=GetNoteInteractor)
        self.get_note.get_note_by_id = AsyncMock()

        self.delete_note = MagicMock(spec=DeleteNoteInteractor)
        self.delete_note.delete_note = AsyncMock()

        self.update_note = MagicMock(spec=UpdateNoteInteractor)
        self.update_note.update_note = AsyncMock()

        self.export_notes = MagicMock(spec=ExportNotesInteractor)
        self.export_notes.export_notes = AsyncMock()

        self.import_notes = MagicMock(spec=ImportNotesInteractor)
        self.import_notes.import_notes = AsyncMock()


class NotesApiProvider(Provider):
    scope = Scope.APP

    def __init__(self, mocks: NotesApiMocks) -> None:
        super().__init__()
        self._mocks = mocks

    @provide
    def provide_get_notes(self) -> GetNotesInteractor:
        return self._mocks.get_notes

    @provide
    def provide_search_wikilinks(self) -> SearchWikilinkSuggestionsInteractor:
        return self._mocks.search_wikilinks

    @provide
    def provide_search_by_title(self) -> SearchNotesByTitleInteractor:
        return self._mocks.search_by_title

    @provide
    def provide_create_note(self) -> CreateNoteInteractor:
        return self._mocks.create_note

    @provide
    def provide_get_note(self) -> GetNoteInteractor:
        return self._mocks.get_note

    @provide
    def provide_delete_note(self) -> DeleteNoteInteractor:
        return self._mocks.delete_note

    @provide
    def provide_update_note(self) -> UpdateNoteInteractor:
        return self._mocks.update_note

    @provide
    def provide_export_notes(self) -> ExportNotesInteractor:
        return self._mocks.export_notes

    @provide
    def provide_import_notes(self) -> ImportNotesInteractor:
        return self._mocks.import_notes


@pytest.fixture
def notes_api_client(event_loop):
    mocks = NotesApiMocks()
    user = User(
        id=uuid4(),
        telegram_id=12345,
        first_name="Test",
        last_name="User",
        created_at=datetime.utcnow(),
    )

    app = create_bare_app(
        APIConfig(
            internal_host="0.0.0.0",
            external_host="localhost",
            port=8000,
        )
    )

    async def override_user():
        return user

    app.dependency_overrides[get_user_from_request] = override_user

    container = make_async_container(NotesApiProvider(mocks))
    setup_dishka(container, app)

    with TestClient(app) as client:
        yield client, mocks, user

    event_loop.run_until_complete(container.close())
