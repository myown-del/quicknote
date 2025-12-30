from quicknote.domain.entities.note import NoteDM
from quicknote.infrastructure.db.models import Note


def get_note_dm(note: Note) -> NoteDM:
    return NoteDM(
        id=note.id,
        user_id=note.user_id,
        title=note.title,
        text=note.text,
        created_at=note.created_at,
        updated_at=note.updated_at
    )


def get_note_db(note_dm: NoteDM) -> Note:
    return Note(
        id=note_dm.id,
        user_id=note_dm.user_id,
        title=note_dm.title,
        text=note_dm.text,
        created_at=note_dm.created_at,
        updated_at=note_dm.updated_at
    )
