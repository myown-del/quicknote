from dataclasses import dataclass
from uuid import uuid4

import pytest

from brain.application.interactors import GetNoteInteractor, GetNotesInteractor
from brain.presentation.tgbot.dialogs.menus.view_notes.getters import (
    get_notes_list,
    get_note_details,
)
from tests.unit.presentation.tgbot.fakes import (
    FakeContainer,
    FakeFromUserEvent,
    FakeGetNoteInteractor,
    FakeGetNotesInteractor,
    FakeUser,
)


@dataclass
class FakeDialogContext:
    dialog_data: dict


@dataclass
class FakeDialogManager:
    middleware_data: dict
    event: object | None = None
    _context: FakeDialogContext | None = None

    def current_context(self):
        return self._context


@pytest.mark.asyncio
async def test_get_notes_list_fetches_for_user():
    # setup: dialog manager with user and notes interactor
    user = FakeUser(id=99)
    event = FakeFromUserEvent(from_user=user)
    interactor = FakeGetNotesInteractor(notes=["note-1"])
    container = FakeContainer({GetNotesInteractor: interactor})
    dialog_manager = FakeDialogManager(
        middleware_data={"dishka_container": container},
        event=event,
    )

    # action: fetch notes list data
    result = await get_notes_list(dialog_manager)

    # check: interactor called with user id and notes returned
    assert interactor.calls == [{"user_telegram_id": 99}]
    assert result == {"notes": ["note-1"]}


@pytest.mark.asyncio
async def test_get_note_details_uses_selected_id():
    # setup: dialog manager with chosen note id
    chosen_id = uuid4()
    interactor = FakeGetNoteInteractor(note="note")
    container = FakeContainer({GetNoteInteractor: interactor})
    context = FakeDialogContext(dialog_data={"chosen_note_id": str(chosen_id)})
    dialog_manager = FakeDialogManager(
        middleware_data={"dishka_container": container},
        _context=context,
    )

    # action: fetch note details data
    result = await get_note_details(dialog_manager)

    # check: interactor called with uuid and note returned
    assert interactor.calls == [chosen_id]
    assert result == {"note": "note"}
