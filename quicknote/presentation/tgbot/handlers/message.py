from aiogram.types import Message
from dishka import AsyncContainer

from quicknote.application.interactors.notes.dto import CreateNote
from quicknote.application.interactors import NoteInteractor


async def handle_message(m: Message, dishka_container: AsyncContainer):
    interactor = await dishka_container.get(NoteInteractor)
    await interactor.create_note(
        CreateNote(
            by_user_telegram_id=m.from_user.id,
            text=m.text,
        )
    )

    await m.reply("Заметка сохранена")
