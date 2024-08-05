from uuid import uuid4

import pytest
from dishka import AsyncContainer

from quicknote.application.abstractions.repositories.notes import INotesRepository
from quicknote.application.abstractions.repositories.users import IUsersRepository
from quicknote.application.interactors import NoteInteractor
from quicknote.application.interactors.notes.dto import CreateNote
from quicknote.application.interactors.notes.exceptions import NoteTooLongException
from quicknote.application.interactors.notes.rules import MAX_NOTE_LENGTH
from quicknote.application.interactors.users.exceptions import UserNotFoundException
from quicknote.domain.entities.user import UserDM


@pytest.mark.asyncio
async def test_note_creation(dishka: AsyncContainer):
    async with dishka() as container:
        interactor = await container.get(NoteInteractor)
        notes_repo = await container.get(INotesRepository)
        users_repo = await container.get(IUsersRepository)

        user_telegram_id = 123
        user_id = uuid4()
        await users_repo.create(UserDM(
            id=user_id,
            telegram_id=user_telegram_id,
            username="test_username",
            first_name="John",
            last_name="Smith",
        ))

        data = CreateNote(
            by_user_telegram_id=user_telegram_id,
            text="Some note text",
        )
        note_id = await interactor.create_note(data)

        note = await notes_repo.get_by_id(note_id)
        assert note is not None
        assert note.user_id == user_id
        assert note.text == data.text


@pytest.mark.asyncio
async def test_note_too_long_exception(dishka: AsyncContainer):
    async with dishka() as container:
        interactor = await container.get(NoteInteractor)
        users_repo = await container.get(IUsersRepository)

        user_telegram_id = 123
        await users_repo.create(UserDM(
            id=uuid4(),
            telegram_id=user_telegram_id,
            username="test_username",
            first_name="John",
            last_name="Smith",
        ))

        data = CreateNote(
            by_user_telegram_id=123,
            text="a" * (MAX_NOTE_LENGTH + 1)
        )
        with pytest.raises(NoteTooLongException):
            await interactor.create_note(data)


@pytest.mark.asyncio
async def test_note_creation_by_nonexistent_user(dishka: AsyncContainer):
    async with dishka() as container:
        interactor = await container.get(NoteInteractor)

        data = CreateNote(
            by_user_telegram_id=123,
            text="Some note text",
        )
        with pytest.raises(UserNotFoundException):
            await interactor.create_note(data)
