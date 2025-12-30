from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    main_menu = State()


class ViewNotes(StatesGroup):
    notes_list = State()
    choose_hashtag_filter = State()
    note_details = State()
