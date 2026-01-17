import pytest

from brain.domain.exceptions import (
    KeywordNoteAlreadyExistsError,
    KeywordNoteTitleRequiredError,
)
from brain.domain.services.notes import ensure_keyword_note_valid, sanitize_filename


def test_ensure_keyword_note_valid_skips_non_keyword_note():
    # setup: prepare non-keyword note data
    title = None
    represents_keyword = False
    existing_keyword_count = 2

    # action: run validation
    ensure_keyword_note_valid(
        title=title,
        represents_keyword=represents_keyword,
        existing_keyword_count=existing_keyword_count,
    )

    # check: no exception means validation is skipped
    assert True


def test_ensure_keyword_note_valid_requires_title_for_keyword_note():
    # setup: prepare keyword note without title
    title = None
    represents_keyword = True
    existing_keyword_count = 0

    # action: run validation for missing title
    # check: validation rejects missing title
    with pytest.raises(KeywordNoteTitleRequiredError):
        ensure_keyword_note_valid(
            title=title,
            represents_keyword=represents_keyword,
            existing_keyword_count=existing_keyword_count,
        )


def test_ensure_keyword_note_valid_rejects_existing_keyword():
    # setup: prepare keyword note with existing keyword
    title = "Keyword"
    represents_keyword = True
    existing_keyword_count = 1

    # action: run validation for duplicate keyword
    # check: validation rejects duplicate keyword note
    with pytest.raises(KeywordNoteAlreadyExistsError):
        ensure_keyword_note_valid(
            title=title,
            represents_keyword=represents_keyword,
            existing_keyword_count=existing_keyword_count,
        )


def test_sanitize_filename_removes_disallowed_characters_and_trims():
    # setup: filename with disallowed chars and outer spaces
    filename = "  my*weird?file.txt  "

    # action: sanitize filename
    sanitized = sanitize_filename(filename)

    # check: only allowed characters remain and spacing is trimmed
    assert sanitized == "myweirdfiletxt"
