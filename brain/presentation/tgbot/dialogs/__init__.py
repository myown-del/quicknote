from aiogram import Dispatcher

from .menus import main_menu_dialog, view_notes_dialog


def register_dialogs(dp: Dispatcher):
    dp.include_router(main_menu_dialog)
    dp.include_router(view_notes_dialog)
