from dishka import Provider, Scope, provide

from quicknote.application.interactors import (
    UserInteractor,
    NoteInteractor,
)


class InteractorProvider(Provider):
    get_user_interactor = provide(UserInteractor, scope=Scope.REQUEST)
    get_note_interactor = provide(NoteInteractor, scope=Scope.REQUEST)
