import pytest
from dishka import AsyncContainer
from brain.application.interactors import CreateNoteInteractor
from brain.application.interactors.notes.dto import CreateNote
from brain.domain.entities.user import User
from brain.infrastructure.db.repositories.hub import RepositoryHub


@pytest.mark.asyncio
async def test_wikilink_suggestions_include_keyword_notes_and_missing_keywords(
    dishka_request: AsyncContainer,
    repo_hub: RepositoryHub,
    user: User,
):
    create_interactor = await dishka_request.get(CreateNoteInteractor)

    await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Alpha",
            text="Alpha text",
            represents_keyword=True,
        )
    )
    await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Beta",
            text="Non keyword note",
        )
    )
    await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Zeta",
            text="Zeta text",
            represents_keyword=True,
        )
    )

    await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Links",
            text="See [[Beta]] and [[Gamma]] and [[Delta]]",
        )
    )
    await create_interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Delta",
            text="Delta text",
            represents_keyword=True,
        )
    )

    suggestions = await repo_hub.notes.search_wikilink_suggestions(
        user_id=user.id,
        query="ta",
    )

    assert [s.title for s in suggestions] == ["Delta", "Zeta", "Beta"]
    assert [s.represents_keyword for s in suggestions] == [True, True, False]
