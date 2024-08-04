import logging
from contextlib import suppress

from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.api.exceptions import OutdatedIntent, UnknownIntent

from quicknote.presentation.tgbot.states import MainMenu

logger = logging.getLogger(__name__)


async def handle_exception(error: ErrorEvent, dialog_manager: DialogManager):
    logger.info(f"Handling exception: {error.exception}")
    if isinstance(error.exception, (UnknownIntent, OutdatedIntent)):
        # with suppress(Exception):
        #     await error.update.callback_query.message.delete()
        user = error.update.callback_query.from_user
        await dialog_manager.start(state=MainMenu.main_menu, mode=StartMode.RESET_STACK)
        logger.info(f"Restart dialog for user '{user.full_name}' (tg_id: {user.id})")
        return False

    logger.error(f"Uncaught exception, exc: {error.exception}", exc_info=True)
