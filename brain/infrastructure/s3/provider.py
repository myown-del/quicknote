from dishka import Provider, Scope, provide

from brain.config.models import S3Config
from brain.infrastructure.s3.client import S3Client


class S3Provider(Provider):
    scope = Scope.APP

    @provide
    def get_s3_client(self, config: S3Config) -> S3Client:
        return S3Client(config)
