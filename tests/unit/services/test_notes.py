import pytest

from brain.domain.exceptions import (
    KeywordNoteAlreadyExistsError,
    KeywordNoteTitleRequiredError,
)
from brain.domain.services.notes import ensure_keyword_note_valid


def test_non_keyword_note_passes():
    ensure_keyword_note_valid(
        title=None,
        represents_keyword=False,
        existing_keyword_count=0,
    )


def test_keyword_note_requires_title():
    with pytest.raises(KeywordNoteTitleRequiredError):
        ensure_keyword_note_valid(
            title=None,
            represents_keyword=True,
            existing_keyword_count=0,
        )


def test_keyword_note_must_be_unique():
    with pytest.raises(KeywordNoteAlreadyExistsError):
        ensure_keyword_note_valid(
            title="Keyword",
            represents_keyword=True,
            existing_keyword_count=1,
        )


def test_keyword_note_ok_when_unique():
    ensure_keyword_note_valid(
        title="Keyword",
        represents_keyword=True,
        existing_keyword_count=0,
    )
