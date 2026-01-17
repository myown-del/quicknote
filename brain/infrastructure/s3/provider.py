from dishka import Provider, Scope, provide

from brain.config.models import S3Config
from brain.application.abstractions.storage.user_profile_pictures import IProfilePictureStorage
from brain.infrastructure.s3.client import S3Client
from brain.infrastructure.s3.profile_picture_storage import S3ProfilePictureStorage


class S3Provider(Provider):
    scope = Scope.APP

    @provide
    def get_s3_client(self, config: S3Config) -> S3Client:
        return S3Client(config)

    @provide(provides=IProfilePictureStorage)
    def get_profile_picture_storage(self, s3_client: S3Client, config: S3Config) -> S3ProfilePictureStorage:
        return S3ProfilePictureStorage(s3_client=s3_client, s3_config=config)
