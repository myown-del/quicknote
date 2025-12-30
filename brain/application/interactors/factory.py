from dishka import Provider, Scope, provide

from brain.application.interactors import (
    UserInteractor,
    NoteInteractor,
)
from brain.application.interactors.auth.interactor import AuthInteractor
from brain.application.interactors.auth.session_interactor import (
    TelegramBotAuthSessionInteractor,
)


class InteractorProvider(Provider):
    get_user_interactor = provide(UserInteractor, scope=Scope.REQUEST)
    get_note_interactor = provide(NoteInteractor, scope=Scope.REQUEST)
    get_auth_interactor = provide(AuthInteractor, scope=Scope.REQUEST)
    get_telegram_bot_auth_session_interactor = provide(
        TelegramBotAuthSessionInteractor, scope=Scope.REQUEST
    )
