from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.kbd import Select, Button, Cancel, SwitchTo

from .getters import get_notes_list, get_note_details
from .handlers import handle_note_chosen
from quicknote.presentation.tgbot.states import ViewNotes
from ...custom_widgets.scrolling_group import SimpleScrollingGroup

notes_list_window = Window(
    Case(
        {
            True: Const("<b>Your notes 👇</b>"),
            False: Const("<b>You have no notes yet</b>"),
        },
        selector=F["notes"].len() > 0,
    ),
    SimpleScrollingGroup(
        Select(
            Format("{item.text}"),
            id="notes_list_select",
            item_id_getter=lambda x: str(x.id),
            items="notes",
            on_click=handle_note_chosen,
        ),
        id="notes_list_sgroup",
        width=1,
        height=6,
    ),
    Cancel(
        text=Const("<< Back"),
        id="back_to_main_menu",
    ),
    getter=get_notes_list,
    state=ViewNotes.notes_list,
)

note_details_window = Window(
    Format("{note.text}"),
    Button(
        text=Format("Created: {note.created_at}"),
        id="note_details_created",
    ),
    Button(
        text=Format("Updated: {note.updated_at}"),
        id="note_details_updated",
    ),
    SwitchTo(
        text=Const("<< Back"),
        id="back_to_notes_list",
        state=ViewNotes.notes_list,
    ),
    getter=get_note_details,
    state=ViewNotes.note_details,
)
