from dishka import Provider, Scope, provide

from quicknote.application.interactors import (
    UserInteractor,
    NoteInteractor,
)
from quicknote.application.interactors.auth.interactor import AuthInteractor


class InteractorProvider(Provider):
    get_user_interactor = provide(UserInteractor, scope=Scope.REQUEST)
    get_note_interactor = provide(NoteInteractor, scope=Scope.REQUEST)
    get_auth_interactor = provide(AuthInteractor, scope=Scope.REQUEST)
