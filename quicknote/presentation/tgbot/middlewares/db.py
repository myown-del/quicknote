from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from quicknote.infrastructure.db.repositories.hub import RepositoryHub


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        dishka = data["dishka_container"]
        repo_hub = await dishka.get(RepositoryHub)
        data["repo_hub"] = repo_hub
        result = await handler(event, data)
        return result
