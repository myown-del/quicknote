from aiogram_dialog import DialogManager

from brain.presentation.tgbot.states import ViewNotes


async def handle_note_chosen(cq, select, dialog_manager: DialogManager, note_id: str):
    dialog_manager.current_context().dialog_data["chosen_note_id"] = note_id
    await dialog_manager.switch_to(state=ViewNotes.note_details)
