import pytest
from dishka import AsyncContainer

from brain.application.interactors import NoteInteractor
from brain.application.interactors.notes.dto import CreateNote, UpdateNote
from brain.application.interactors.notes.exceptions import (
    KeywordNoteAlreadyExistsException,
    KeywordNoteTitleRequiredException,
)
from brain.application.interactors.users.exceptions import UserNotFoundException
from brain.domain.entities.user import User
from brain.infrastructure.db.repositories.hub import RepositoryHub


@pytest.mark.asyncio
async def test_note_creation(dishka_request: AsyncContainer, user: User, repo_hub: RepositoryHub):
    interactor = await dishka_request.get(NoteInteractor)

    data = CreateNote(
        by_user_telegram_id=user.telegram_id,
        title="Note title",
        text="Some note text",
    )
    note_id = await interactor.create_note(data)

    note = await repo_hub.notes.get_by_id(note_id)
    assert note is not None
    assert note.user_id == user.id
    assert note.title == data.title
    assert note.text == data.text
    assert note.represents_keyword is False


@pytest.mark.asyncio
async def test_keyword_note_requires_title(dishka_request: AsyncContainer, user: User):
    interactor = await dishka_request.get(NoteInteractor)

    data = CreateNote(
        by_user_telegram_id=user.telegram_id,
        title=None,
        text="Some note text",
        represents_keyword=True,
    )
    with pytest.raises(KeywordNoteTitleRequiredException):
        await interactor.create_note(data)


@pytest.mark.asyncio
async def test_keyword_note_unique_by_title(dishka_request: AsyncContainer, user: User):
    interactor = await dishka_request.get(NoteInteractor)

    await interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Keyword",
            text="First",
            represents_keyword=True,
        )
    )
    with pytest.raises(KeywordNoteAlreadyExistsException):
        await interactor.create_note(
            CreateNote(
                by_user_telegram_id=user.telegram_id,
                title="Keyword",
                text="Second",
                represents_keyword=True,
            )
        )

    note_id = await interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Keyword",
            text="Non keyword note",
            represents_keyword=False,
        )
    )
    note = await interactor.get_note_by_id(note_id)
    assert note is not None
    assert note.title == "Keyword"
    assert note.represents_keyword is False


@pytest.mark.asyncio
async def test_keyword_note_update_validation(dishka_request: AsyncContainer, user: User):
    interactor = await dishka_request.get(NoteInteractor)

    note_id = await interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Alpha",
            text="Note",
        )
    )
    with pytest.raises(KeywordNoteTitleRequiredException):
        await interactor.update_note(
            UpdateNote(
                note_id=note_id,
                title=None,
                text="Note",
                represents_keyword=True,
            )
        )


@pytest.mark.asyncio
async def test_note_creation_by_nonexistent_user(dishka_request: AsyncContainer):
    interactor = await dishka_request.get(NoteInteractor)

    data = CreateNote(
        by_user_telegram_id=-1,
        title=None,
        text="Some note text",
    )
    with pytest.raises(UserNotFoundException):
        await interactor.create_note(data)
