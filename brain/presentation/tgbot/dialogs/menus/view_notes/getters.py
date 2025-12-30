from uuid import UUID

from aiogram_dialog import DialogManager
from dishka import AsyncContainer

from brain.application.interactors import NoteInteractor


async def get_notes_list(dialog_manager: DialogManager, **kwargs):
    container: AsyncContainer = dialog_manager.middleware_data.get("dishka_container")
    notes_interactor: NoteInteractor = await container.get(NoteInteractor)

    user = dialog_manager.event.from_user
    notes = await notes_interactor.get_notes(user_telegram_id=user.id)

    return {"notes": notes}


async def get_note_details(dialog_manager: DialogManager, **kwargs):
    container: AsyncContainer = dialog_manager.middleware_data.get("dishka_container")
    notes_interactor: NoteInteractor = await container.get(NoteInteractor)

    chosen_note_id = dialog_manager.current_context().dialog_data.get("chosen_note_id")
    chosen_note_id = UUID(chosen_note_id)
    note = await notes_interactor.get_note_by_id(chosen_note_id)
    return {"note": note}
