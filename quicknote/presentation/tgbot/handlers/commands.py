from aiogram.filters import CommandObject
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from quicknote.presentation.tgbot.states import MainMenu


async def handle_start_cmd(
    message: Message, command: CommandObject, dialog_manager: DialogManager
):
    await dialog_manager.start(state=MainMenu.main_menu, mode=StartMode.RESET_STACK)
