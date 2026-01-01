import pytest
from dishka import AsyncContainer

from brain.application.interactors import (
    CreateNoteInteractor,
    UpdateNoteInteractor,
)
from brain.application.interactors.notes.dto import CreateNote, UpdateNote
from brain.application.interactors.notes.exceptions import (
    NoteTitleAlreadyExistsException,
    NoteTitleRequiredException,
)
from brain.application.interactors.users.exceptions import UserNotFoundException
from brain.domain.entities.user import User
from brain.infrastructure.db.repositories.hub import RepositoryHub


@pytest.mark.asyncio
async def test_note_creation(dishka_request: AsyncContainer, user: User, repo_hub: RepositoryHub):
    create_interactor = await dishka_request.get(CreateNoteInteractor)

    data = CreateNote(
        by_user_telegram_id=user.telegram_id,
        title="Note title",
        text="Some note text",
    )
    note_id = await create_interactor.create_note(data)

    note = await repo_hub.notes.get_by_id(note_id)
    assert note is not None
    assert note.user_id == user.id
    assert note.title == data.title
    assert note.text == data.text
    assert note.represents_keyword_id is not None


@pytest.mark.asyncio
async def test_note_autogenerates_title_when_missing(
    dishka_request: AsyncContainer,
    user: User,
    repo_hub: RepositoryHub,
):
    create_interactor = await dishka_request.get(CreateNoteInteractor)

    data = CreateNote(
        by_user_telegram_id=user.telegram_id,
        title=None,
        text="Some note text",
    )
    note_id = await create_interactor.create_note(data)
    note = await repo_hub.notes.get_by_id(note_id)
    assert note is not None
    assert note.title.startswith("Untitled ")
    assert note.represents_keyword_id is not None


@pytest.mark.asyncio
async def test_note_unique_by_title(
    dishka_request: AsyncContainer,
    user: User,
    repo_hub: RepositoryHub,
):
    create_interactor = await dishka_request.get(CreateNoteInteractor)

    await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Keyword",
            text="First",
        )
    )
    with pytest.raises(NoteTitleAlreadyExistsException):
        await create_interactor.create_note(
            CreateNote(
                by_user_telegram_id=user.telegram_id,
                title="Keyword",
                text="Second",
            )
        )

    notes = await repo_hub.notes.get_by_user_telegram_id(user.telegram_id)
    assert [note.title for note in notes].count("Keyword") == 1


@pytest.mark.asyncio
async def test_note_update_requires_title(
    dishka_request: AsyncContainer,
    user: User,
    repo_hub: RepositoryHub,
):
    create_interactor = await dishka_request.get(CreateNoteInteractor)
    update_interactor = await dishka_request.get(UpdateNoteInteractor)

    note_id = await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Alpha",
            text="Note",
        )
    )
    with pytest.raises(NoteTitleRequiredException):
        await update_interactor.update_note(
            UpdateNote(
                note_id=note_id,
                title=None,
                text="Note",
            )
        )


@pytest.mark.asyncio
async def test_note_duplicate_title_conflict(
    dishka_request: AsyncContainer,
    user: User,
    repo_hub: RepositoryHub,
):
    create_interactor = await dishka_request.get(CreateNoteInteractor)
    update_interactor = await dishka_request.get(UpdateNoteInteractor)

    await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Omega",
            text="Keyword note",
        )
    )

    note_id = await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Sigma",
            text="Regular note",
        )
    )

    with pytest.raises(NoteTitleAlreadyExistsException):
        await update_interactor.update_note(
            UpdateNote(
                note_id=note_id,
                title="Omega",
                text="Regular note",
            )
        )


@pytest.mark.asyncio
async def test_note_creation_by_nonexistent_user(dishka_request: AsyncContainer):
    create_interactor = await dishka_request.get(CreateNoteInteractor)

    data = CreateNote(
        by_user_telegram_id=-1,
        title=None,
        text="Some note text",
    )
    with pytest.raises(UserNotFoundException):
        await create_interactor.create_note(data)
