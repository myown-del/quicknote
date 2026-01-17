import logging
from io import BytesIO

from aiogram import Bot
from dishka.integrations.taskiq import FromDishka, inject

from brain.application.interactors import UploadUserProfilePictureInteractor
from brain.application.interactors.users.update_all_profile_pictures import (
    UpdateAllUsersProfilePicturesInteractor,
)
from brain.domain.services.media import guess_image_content_type
from brain.main.entrypoints.taskiq.broker import broker

logger = logging.getLogger(__name__)


@broker.task
@inject(patch_module=True)
async def upload_user_profile_picture_task(
    telegram_id: int,
    bot: FromDishka[Bot],
    interactor: FromDishka[UploadUserProfilePictureInteractor],
) -> None:
    photos = await bot.get_user_profile_photos(user_id=telegram_id, limit=1)
    if not photos.photos:
        return

    photo = photos.photos[0][-1]
    file = await bot.get_file(photo.file_id)
    buffer = BytesIO()
    await bot.download_file(file.file_path, destination=buffer)
    content = buffer.getvalue()
    if not content:
        return

    await interactor.upload_profile_picture(
        telegram_id=telegram_id,
        image_content=content,
        content_type=guess_image_content_type(file.file_path),
    )


@broker.task(schedule=[{"cron": "0 0 * * *"}])
@inject(patch_module=True)
async def update_all_users_profile_pictures_task(
    interactor: FromDishka[UpdateAllUsersProfilePicturesInteractor],
) -> None:
    await interactor.execute()
