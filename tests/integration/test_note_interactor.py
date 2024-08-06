import pytest
from dishka import AsyncContainer

from quicknote.application.interactors import NoteInteractor
from quicknote.application.interactors.notes.dto import CreateNote
from quicknote.application.interactors.notes.exceptions import NoteTooLongException
from quicknote.application.interactors.notes.rules import MAX_NOTE_LENGTH
from quicknote.application.interactors.users.exceptions import UserNotFoundException
from quicknote.domain.entities.user import UserDM
from quicknote.infrastructure.db.repositories.hub import RepositoryHub


@pytest.mark.asyncio
async def test_note_creation(dishka_request: AsyncContainer, user: UserDM, repo_hub: RepositoryHub):
    interactor = await dishka_request.get(NoteInteractor)

    data = CreateNote(
        by_user_telegram_id=user.telegram_id,
        text="Some note text",
    )
    note_id = await interactor.create_note(data)

    note = await repo_hub.notes.get_by_id(note_id)
    assert note is not None
    assert note.user_id == user.id
    assert note.text == data.text


@pytest.mark.asyncio
async def test_note_too_long_exception(dishka_request: AsyncContainer, user: UserDM):
    interactor = await dishka_request.get(NoteInteractor)

    data = CreateNote(
        by_user_telegram_id=user.telegram_id,
        text="a" * (MAX_NOTE_LENGTH + 1)
    )
    with pytest.raises(NoteTooLongException):
        await interactor.create_note(data)


@pytest.mark.asyncio
async def test_note_creation_by_nonexistent_user(dishka_request: AsyncContainer):
    interactor = await dishka_request.get(NoteInteractor)

    data = CreateNote(
        by_user_telegram_id=-1,
        text="Some note text",
    )
    with pytest.raises(UserNotFoundException):
        await interactor.create_note(data)
