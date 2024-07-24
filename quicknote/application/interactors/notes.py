from uuid import uuid4

from quicknote.application.abstractions.repositories.hub import IRepositoryHub
from quicknote.application.interactors.dto import CreateNote
from quicknote.domain.entities.note import NoteDM


class NoteInteractor:
    def __init__(
            self,
            repo_hub: IRepositoryHub,
    ):
        self._repo_hub = repo_hub

    async def create_note(self, note_data: CreateNote):
        user = await self._repo_hub.users.get_by_telegram_id(note_data.by_user_telegram_id)
        note = NoteDM(
            id=uuid4(),
            user_id=user.id,
            text=note_data.text
        )
        await self._repo_hub.notes.create(note)
