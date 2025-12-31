from aiogram.types import Message
from dishka import AsyncContainer

from brain.application.interactors.notes.dto import CreateNote
from brain.application.interactors import CreateNoteInteractor
from brain.application.interactors.users.exceptions import UserNotFoundException


async def handle_message(m: Message, dishka_container: AsyncContainer):
    interactor = await dishka_container.get(CreateNoteInteractor)
    try:
        await interactor.create_note(
            CreateNote(
                by_user_telegram_id=m.from_user.id,
                title=None,
                text=m.text,
            )
        )
    except UserNotFoundException:
        await m.reply(f"Вы не авторизованы")
    except Exception as e:
        await m.reply(f"Ошибка создания заметки")

    await m.reply("Заметка сохранена")
