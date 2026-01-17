from uuid import UUID, uuid4

import pytest

from brain.application.interactors.notes.exceptions import (
    NoteTitleAlreadyExistsException,
    NoteTitleRequiredException,
)
from brain.application.services.note_titles import NoteTitleService


class DummyNotesRepository:
    def __init__(self, existing_titles: dict[UUID, set[str]]):
        self._existing_titles = existing_titles

    async def count_notes_by_user_and_title(
        self,
        user_id: UUID,
        title: str,
        exclude_note_id: UUID | None = None,
    ) -> int:
        return 1 if title in self._existing_titles.get(user_id, set()) else 0


@pytest.mark.asyncio
async def test_create_title_autogenerates_first_free_untitled():
    user_id = uuid4()
    repo = DummyNotesRepository(existing_titles={user_id: {"Untitled 1"}})
    service = NoteTitleService(repo)

    title = await service.resolve_create_title(user_id=user_id, title=None)

    assert title == "Untitled 2"


@pytest.mark.asyncio
async def test_update_title_requires_value():
    user_id = uuid4()
    repo = DummyNotesRepository(existing_titles={})
    service = NoteTitleService(repo)

    with pytest.raises(NoteTitleRequiredException):
        await service.ensure_update_title(user_id=user_id, title=None)


@pytest.mark.asyncio
async def test_unique_title_validation_rejects_duplicates():
    user_id = uuid4()
    repo = DummyNotesRepository(existing_titles={user_id: {"Dup"}})
    service = NoteTitleService(repo)

    with pytest.raises(NoteTitleAlreadyExistsException):
        await service.ensure_unique_title(user_id=user_id, title="Dup")
