from quicknote.domain.entities.note import NoteDM, HashtagDM
from quicknote.infrastructure.db.models import Note, Hashtag


def get_note_dm(note: Note) -> NoteDM:
    hashtags = []
    for hashtag in note.hashtags:
        hashtags.append(HashtagDM(id=hashtag.hashtag.id, name=hashtag.hashtag.name))

    return NoteDM(id=note.id, user_id=note.user_id, text=note.text, hashtags=hashtags)


def get_note_db(note_dm: NoteDM) -> Note:
    return Note(id=note_dm.id, user_id=note_dm.user_id, text=note_dm.text)


def get_hashtag_db(hashtag_dm: HashtagDM):
    return Hashtag(id=hashtag_dm.id, name=hashtag_dm.name)
