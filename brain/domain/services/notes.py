from brain.domain.exceptions import (
    KeywordNoteAlreadyExistsError,
    KeywordNoteTitleRequiredError,
)


def ensure_keyword_note_valid(
    title: str | None,
    represents_keyword: bool,
    existing_keyword_count: int,
) -> None:
    if not represents_keyword:
        return
    if not title:
        raise KeywordNoteTitleRequiredError()
    if existing_keyword_count > 0:
        raise KeywordNoteAlreadyExistsError()
