import pytest
from dishka import AsyncContainer

from brain.application.interactors import (
    CreateNoteInteractor,
    GetNoteInteractor,
    UpdateNoteInteractor,
)
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
    assert note.represents_keyword_id is None


@pytest.mark.asyncio
async def test_keyword_note_requires_title(
    dishka_request: AsyncContainer,
    user: User,
    repo_hub: RepositoryHub,
):
    create_interactor = await dishka_request.get(CreateNoteInteractor)

    data = CreateNote(
        by_user_telegram_id=user.telegram_id,
        title=None,
        text="Some note text",
        represents_keyword=True,
    )
    with pytest.raises(KeywordNoteTitleRequiredException):
        await create_interactor.create_note(data)


@pytest.mark.asyncio
async def test_keyword_note_unique_by_title(
    dishka_request: AsyncContainer,
    user: User,
    repo_hub: RepositoryHub,
):
    create_interactor = await dishka_request.get(CreateNoteInteractor)
    get_note_interactor = await dishka_request.get(GetNoteInteractor)

    await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Keyword",
            text="First",
            represents_keyword=True,
        )
    )
    with pytest.raises(KeywordNoteAlreadyExistsException):
        await create_interactor.create_note(
            CreateNote(
                by_user_telegram_id=user.telegram_id,
                title="Keyword",
                text="Second",
                represents_keyword=True,
            )
        )

    note_id = await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Keyword",
            text="Non keyword note",
        )
    )
    note = await get_note_interactor.get_note_by_id(note_id)
    assert note is not None
    assert note.title == "Keyword"
    assert note.represents_keyword_id is None


@pytest.mark.asyncio
async def test_keyword_note_update_validation(
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
    with pytest.raises(KeywordNoteTitleRequiredException):
        await update_interactor.update_note(
            UpdateNote(
                note_id=note_id,
                title=None,
                text="Note",
                represents_keyword=True,
            )
        )


@pytest.mark.asyncio
async def test_keyword_note_duplicate_title_conflict(
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
            represents_keyword=True,
        )
    )

    note_id = await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Omega",
            text="Regular note",
        )
    )

    with pytest.raises(KeywordNoteAlreadyExistsException):
        await update_interactor.update_note(
            UpdateNote(
                note_id=note_id,
                title="Omega",
                text="Regular note",
                represents_keyword=True,
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
