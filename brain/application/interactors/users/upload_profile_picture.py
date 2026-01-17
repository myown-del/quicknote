from uuid import uuid4

from brain.application.abstractions.repositories.s3_files import (
    IS3FilesRepository,
)
from brain.application.abstractions.repositories.users import IUsersRepository
from brain.application.abstractions.storage.user_profile_pictures import IProfilePictureStorage
from brain.application.interactors.users.exceptions import UserNotFoundException
from brain.domain.entities.s3_file import S3File


class UploadUserProfilePictureInteractor:
    def __init__(
        self,
        users_repo: IUsersRepository,
        s3_files_repo: IS3FilesRepository,
        profile_picture_storage: IProfilePictureStorage,
    ):
        self._users_repo = users_repo
        self._s3_files_repo = s3_files_repo
        self._profile_picture_storage = profile_picture_storage

    async def upload_profile_picture(
        self,
        telegram_id: int,
        image_content: bytes,
        content_type: str | None = None,
    ) -> S3File:
        user = await self._users_repo.get_by_telegram_id(telegram_id)
        if not user:
            raise UserNotFoundException

        extension = self._get_extension(content_type)
        object_name = f"profile_pictures/{user.id}/{uuid4()}.{extension}"
        url = self._profile_picture_storage.upload(
            content=image_content,
            object_name=object_name,
            content_type=content_type,
        )
        profile_picture = S3File(
            id=uuid4(),
            object_name=object_name,
            url=url,
            content_type=content_type,
        )
        existing = await self._s3_files_repo.get_by_user_id(user.id)
        if existing:
            profile_picture.id = existing.id
            await self._s3_files_repo.update(profile_picture)
        else:
            await self._s3_files_repo.create(profile_picture)

        user.profile_picture_file_id = profile_picture.id
        await self._users_repo.update(user)

        return profile_picture

    def _get_extension(self, content_type: str | None) -> str:
        if content_type == "image/png":
            return "png"
        if content_type == "image/webp":
            return "webp"
        return "jpg"
