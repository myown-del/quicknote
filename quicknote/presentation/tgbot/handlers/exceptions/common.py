import logging

from aiogram.types import ErrorEvent

logger = logging.getLogger(__name__)


async def handle_exception(error: ErrorEvent):
    logger.error(f"Uncaught exception, exc: {error.exception}", exc_info=True)