import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka import AsyncContainer

from brain.application.interactors import UserInteractor
from brain.application.interactors.users.dto import CreateOrUpdateUser
from brain.presentation.tgbot.utils.aiogram_helpers import extract_user_from_event

logger = logging.getLogger(__name__)


class UserInfoUpdaterMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        container: AsyncContainer = data["dishka_container"]
        user_interactor = await container.get(UserInteractor)

        user = extract_user_from_event(event)
        if user is not None and not user.is_bot:
            interactor_data = CreateOrUpdateUser(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            await user_interactor.create_or_update_user(interactor_data)
            logger.debug(f"Updated user info: {interactor_data}")

        return await handler(event, data)
