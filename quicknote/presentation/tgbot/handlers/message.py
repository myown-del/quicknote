from aiogram.types import Message
from dishka import AsyncContainer

from quicknote.application.interactors.hashtags.exceptions import (
    HashtagTooLongException,
)
from quicknote.application.interactors.notes.dto import CreateNote
from quicknote.application.interactors.notes.exceptions import NoteTooLongException
from quicknote.application.interactors import NoteInteractor


async def handle_message(m: Message, dishka_container: AsyncContainer):
    interactor = await dishka_container.get(NoteInteractor)
    try:
        await interactor.create_note(
            CreateNote(
                by_user_telegram_id=m.from_user.id,
                text=m.text,
            )
        )
    except NoteTooLongException:
        await m.reply("Заметка слишком длинная")
        return
    except HashtagTooLongException:
        await m.reply(f"Хэштег слишком длинный")
        return

    await m.reply("Заметка сохранена")
