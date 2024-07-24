from aiogram.filters import CommandObject
from aiogram.types import Message


async def handle_start_cmd(message: Message, command: CommandObject):
    await message.answer(
        "Hello, I'm QuickNote bot. I can help you to save your notes. "
        "Just send me a message and I'll save it for you."
    )
