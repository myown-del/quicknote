from brain.domain.entities.s3_file import S3File
from brain.infrastructure.db.models.user import S3FileDB


def map_s3_file_to_dm(file_db: S3FileDB) -> S3File:
    return S3File(
        id=file_db.id,
        object_name=file_db.object_name,
        url=file_db.url,
        content_type=file_db.content_type,
        created_at=file_db.created_at,
        updated_at=file_db.updated_at,
    )


def map_s3_file_to_db(file_dm: S3File) -> S3FileDB:
    return S3FileDB(
        id=file_dm.id,
        object_name=file_dm.object_name,
        url=file_dm.url,
        content_type=file_dm.content_type,
        created_at=file_dm.created_at,
        updated_at=file_dm.updated_at,
    )
