from aiogram_dialog import Dialog

from .widgets import notes_list_window, note_details_window


view_notes_dialog = Dialog(
    notes_list_window,
    note_details_window,
)
