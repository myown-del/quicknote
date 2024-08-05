from quicknote.domain.entities.note import NoteDM
from quicknote.infrastructure.db.models import Note


def get_note_dm(note: Note) -> NoteDM:
    return NoteDM(id=note.id, user_id=note.user_id, text=note.text)


def get_note_db(note_dm: NoteDM) -> Note:
    return Note(id=note_dm.id, user_id=note_dm.user_id, text=note_dm.text)
