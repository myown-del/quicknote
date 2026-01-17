import pytest
from aiogram_dialog import StartMode

from brain.application.interactors import CreateNoteInteractor
from brain.application.interactors.auth.session_interactor import (
    TelegramBotAuthSessionInteractor,
)
from brain.application.interactors.notes.dto import CreateNote
from brain.application.interactors.users.exceptions import UserNotFoundException
from brain.presentation.tgbot.handlers.commands import handle_start_cmd
from brain.presentation.tgbot.handlers.message import handle_message
from brain.presentation.tgbot.states import MainMenu
from tests.unit.presentation.tgbot.fakes import (
    FakeAuthSessionInteractor,
    FakeCommand,
    FakeContainer,
    FakeCreateNoteInteractor,
    FakeDialogManager,
    FakeMessage,
    FakeUser,
)


@pytest.mark.asyncio
async def test_handle_start_cmd_attaches_user_when_session():
    # setup: command with session id and user
    message = FakeMessage(from_user=FakeUser(id=111))
    command = FakeCommand(args="tgauth_abc")
    interactor = FakeAuthSessionInteractor()
    container = FakeContainer({TelegramBotAuthSessionInteractor: interactor})
    dialog_manager = FakeDialogManager()

    # action: handle start command
    await handle_start_cmd(message, command, dialog_manager, container)

    # check: user attached and dialog started
    assert interactor.calls == [{"session_id": "abc", "telegram_id": 111}]
    assert dialog_manager.start_calls == [
        {"state": MainMenu.main_menu, "mode": StartMode.RESET_STACK}
    ]


@pytest.mark.asyncio
async def test_handle_start_cmd_skips_attach_without_session():
    # setup: command without session id
    message = FakeMessage(from_user=FakeUser(id=111))
    command = FakeCommand(args=None)
    container = FakeContainer({})
    dialog_manager = FakeDialogManager()

    # action: handle start command
    await handle_start_cmd(message, command, dialog_manager, container)

    # check: no interactor lookup and dialog started
    assert container.get_calls == []
    assert dialog_manager.start_calls == [
        {"state": MainMenu.main_menu, "mode": StartMode.RESET_STACK}
    ]


@pytest.mark.asyncio
async def test_handle_message_creates_note():
    # setup: message and create-note interactor
    message = FakeMessage(from_user=FakeUser(id=55), text="hello")
    interactor = FakeCreateNoteInteractor()
    container = FakeContainer({CreateNoteInteractor: interactor})

    # action: handle incoming message
    await handle_message(message, container)

    # check: note created and reply sent
    assert interactor.calls == [
        CreateNote(by_user_telegram_id=55, title=None, text="hello")
    ]
    assert message.replies == ["Заметка сохранена"]


@pytest.mark.asyncio
async def test_handle_message_replies_on_user_not_found():
    # setup: interactor raises user-not-found
    message = FakeMessage(from_user=FakeUser(id=55), text="hello")
    interactor = FakeCreateNoteInteractor(error=UserNotFoundException())
    container = FakeContainer({CreateNoteInteractor: interactor})

    # action: handle incoming message
    await handle_message(message, container)

    # check: error reply and success reply sent
    assert message.replies == [
        "Вы не авторизованы",
        "Заметка сохранена",
    ]


@pytest.mark.asyncio
async def test_handle_message_replies_on_generic_error():
    # setup: interactor raises generic error
    message = FakeMessage(from_user=FakeUser(id=55), text="hello")
    interactor = FakeCreateNoteInteractor(error=RuntimeError("boom"))
    container = FakeContainer({CreateNoteInteractor: interactor})

    # action: handle incoming message
    await handle_message(message, container)

    # check: error reply and success reply sent
    assert message.replies == [
        "Ошибка создания заметки",
        "Заметка сохранена",
    ]
