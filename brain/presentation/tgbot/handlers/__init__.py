from aiogram import Dispatcher
from aiogram.filters import CommandStart

from .commands import handle_start_cmd
from .message import handle_message


def register_handlers(dp: Dispatcher):
    dp.message.register(handle_start_cmd, CommandStart())
    dp.message.register(handle_message)
