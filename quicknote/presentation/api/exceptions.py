import logging

from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)


async def validation_exception_handler(request, exc):
    logger.info("Validation error=%s", {"url": request.url, "err": exc})
    return await request_validation_exception_handler(request, exc)


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=validation_exception_handler,
    )
