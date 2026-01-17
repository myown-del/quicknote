import pytest

from brain.application.interactors import UserInteractor
from brain.application.interactors.users.dto import CreateOrUpdateUser
from brain.presentation.tgbot.middlewares.user_info_updater import UserInfoUpdaterMiddleware
from tests.unit.presentation.tgbot.fakes import (
    FakeContainer,
    FakeEvent,
    FakeMessageEvent,
    FakeUser,
    FakeUserInteractor,
    HandlerRecorder,
)


@pytest.mark.asyncio
async def test_user_info_updater_updates_user():
    # setup: event with non-bot user
    user = FakeUser(
        id=123,
        username="tester",
        first_name="Test",
        last_name="User",
        is_bot=False,
    )
    event = FakeEvent(message=FakeMessageEvent(from_user=user))
    interactor = FakeUserInteractor()
    container = FakeContainer({UserInteractor: interactor})
    handler = HandlerRecorder(result="ok")
    middleware = UserInfoUpdaterMiddleware()

    # action: call middleware
    result = await middleware(handler, event, {"dishka_container": container})

    # check: user saved and handler called
    expected = CreateOrUpdateUser(
        telegram_id=123,
        username="tester",
        first_name="Test",
        last_name="User",
    )
    assert interactor.calls == [expected]
    assert handler.calls == [(event, {"dishka_container": container})]
    assert result == "ok"


@pytest.mark.asyncio
async def test_user_info_updater_skips_bot_user():
    # setup: event with bot user
    user = FakeUser(
        id=1,
        username="bot",
        first_name="Bot",
        last_name=None,
        is_bot=True,
    )
    event = FakeEvent(message=FakeMessageEvent(from_user=user))
    interactor = FakeUserInteractor()
    container = FakeContainer({UserInteractor: interactor})
    handler = HandlerRecorder(result="ok")
    middleware = UserInfoUpdaterMiddleware()

    # action: call middleware
    result = await middleware(handler, event, {"dishka_container": container})

    # check: user save skipped
    assert interactor.calls == []
    assert result == "ok"


@pytest.mark.asyncio
async def test_user_info_updater_skips_when_no_user():
    # setup: event without user info
    event = FakeEvent(message=None, callback_query=None)
    interactor = FakeUserInteractor()
    container = FakeContainer({UserInteractor: interactor})
    handler = HandlerRecorder(result="ok")
    middleware = UserInfoUpdaterMiddleware()

    # action: call middleware
    result = await middleware(handler, event, {"dishka_container": container})

    # check: user save skipped
    assert interactor.calls == []
    assert result == "ok"
