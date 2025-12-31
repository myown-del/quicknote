from dishka import Provider, Scope, provide

from brain.application.interactors import (
    CreateNoteInteractor,
    DeleteNoteInteractor,
    GetUserInteractor,
    GetNoteInteractor,
    GetNotesInteractor,
    SearchWikilinkSuggestionsInteractor,
    UpdateNoteInteractor,
    UserInteractor,
)
from brain.application.services.keyword_notes import KeywordNoteService
from brain.application.services.note_keyword_sync import NoteKeywordSyncService
from brain.application.interactors.auth.interactor import AuthInteractor
from brain.application.interactors.auth.session_interactor import (
    TelegramBotAuthSessionInteractor,
)


class InteractorProvider(Provider):
    get_user_interactor = provide(UserInteractor, scope=Scope.REQUEST)
    get_get_user_interactor = provide(GetUserInteractor, scope=Scope.REQUEST)
    get_keyword_note_service = provide(KeywordNoteService, scope=Scope.REQUEST)
    get_note_keyword_sync_service = provide(NoteKeywordSyncService, scope=Scope.REQUEST)
    get_create_note_interactor = provide(CreateNoteInteractor, scope=Scope.REQUEST)
    get_update_note_interactor = provide(UpdateNoteInteractor, scope=Scope.REQUEST)
    get_delete_note_interactor = provide(DeleteNoteInteractor, scope=Scope.REQUEST)
    get_get_notes_interactor = provide(GetNotesInteractor, scope=Scope.REQUEST)
    get_get_note_interactor = provide(GetNoteInteractor, scope=Scope.REQUEST)
    get_search_wikilink_suggestions_interactor = provide(
        SearchWikilinkSuggestionsInteractor, scope=Scope.REQUEST
    )
    get_auth_interactor = provide(AuthInteractor, scope=Scope.REQUEST)
    get_telegram_bot_auth_session_interactor = provide(
        TelegramBotAuthSessionInteractor, scope=Scope.REQUEST
    )
