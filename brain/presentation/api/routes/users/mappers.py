from dataclasses import asdict

from brain.domain.entities.user import User
from brain.presentation.api.routes.users.models import ReadUserSchema


def map_user_to_read_schema(user: User) -> ReadUserSchema:
    return ReadUserSchema.model_validate(asdict(user))