import pytest

from brain.application.abstractions.repositories.notes_graph import (
    INotesGraphRepository,
)
from brain.application.interactors.notes.dto import CreateNote, UpdateNote
from brain.application.interactors.notes.interactor import NoteInteractor
from brain.domain.entities.user import User


@pytest.mark.asyncio
async def test_note_graph_links_only_to_keyword_notes(dishka_request, user: User):
    interactor = await dishka_request.get(NoteInteractor)
    notes_graph_repo = await dishka_request.get(INotesGraphRepository)

    child_id = await interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Child",
            text="leaf",
        )
    )
    await interactor.create_note(
        CreateNote(
            by_user_telegram_id=user.telegram_id,
            title="Root",
            text="see [[Child]] and [[Child|alias]]",
        )
    )

    count = await notes_graph_repo.count_notes_by_user_and_title(
        user_id=user.id, title="Root"
    )
    assert count == 1

    link_count = await notes_graph_repo.count_links_between_notes(
        user_id=user.id, from_title="Root", to_title="Child"
    )
    assert link_count == 0

    await interactor.update_note(
        UpdateNote(
            note_id=child_id,
            title="Child",
            text="leaf",
            represents_keyword=True,
        )
    )

    link_count = await notes_graph_repo.count_links_between_notes(
        user_id=user.id, from_title="Root", to_title="Child"
    )
    assert link_count == 1
