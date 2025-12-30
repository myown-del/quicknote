from quicknote.domain.entities.note import Note
from quicknote.infrastructure.db.models.note import NoteDB


def map_note_to_dm(note: NoteDB) -> Note:
    return Note(
        id=note.id,
        user_id=note.user_id,
        title=note.title,
        text=note.text,
        created_at=note.created_at,
        updated_at=note.updated_at
    )


def map_note_to_db(note: Note) -> NoteDB:
    return NoteDB(
        id=note.id,
        user_id=note.user_id,
        title=note.title,
        text=note.text,
        created_at=note.created_at,
        updated_at=note.updated_at
    )
