import pytest
from dishka import AsyncContainer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from brain.application.interactors import NoteInteractor
from brain.application.interactors.notes.dto import CreateNote
from brain.domain.entities.user import User
from brain.infrastructure.db.models.keyword import KeywordDB


@pytest.mark.asyncio
async def test_keywords_deleted_when_last_link_removed(
    dishka_request: AsyncContainer,
    user: User,
):
    interactor = await dishka_request.get(NoteInteractor)
    session = await dishka_request.get(AsyncSession)

    first_note_id = await interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="First",
            text="See [[Omega]]",
            represents_keyword=False,
        )
    )
    second_note_id = await interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Second",
            text="Linking [[Omega]] too",
            represents_keyword=False,
        )
    )

    result = await session.execute(
        select(KeywordDB).where(KeywordDB.user_id == user.id, KeywordDB.name == "Omega")
    )
    assert result.scalar() is not None

    await interactor.delete_note(first_note_id)
    result = await session.execute(
        select(KeywordDB).where(KeywordDB.user_id == user.id, KeywordDB.name == "Omega")
    )
    assert result.scalar() is not None

    await interactor.delete_note(second_note_id)
    result = await session.execute(
        select(KeywordDB).where(KeywordDB.user_id == user.id, KeywordDB.name == "Omega")
    )
    assert result.scalar() is None
