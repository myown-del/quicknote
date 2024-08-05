from quicknote.application.abstractions.repositories.users import IUsersRepository
from quicknote.domain.entities.user import UserDM


class UsersRepositoryMock(IUsersRepository):
    def __init__(self):
        self._users = []

    async def get_by_telegram_id(self, telegram_id: int) -> UserDM | None:
        for u in self._users:
            if u.telegram_id == telegram_id:
                return u

    async def create(self, entity) -> None:
        self._users.append(entity)

    async def update(self, entity) -> None:
        for i, u in enumerate(self._users):
            if u.id == entity.id:
                self._users[i] = entity

    async def get_by_id(self, user_id) -> UserDM | None:
        for u in self._users:
            if u.id == user_id:
                return u
