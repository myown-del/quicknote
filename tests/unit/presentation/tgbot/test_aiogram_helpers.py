from datetime import datetime, timezone

from aiogram.types import CallbackQuery, Chat, Message, Update, User

from brain.presentation.tgbot.utils.aiogram_helpers import extract_user_from_event


def _user(user_id: int) -> User:
    return User(id=user_id, is_bot=False, first_name="Test")


def _chat(chat_id: int) -> Chat:
    return Chat(id=chat_id, type="private")


def _message(user: User) -> Message:
    return Message(
        message_id=1,
        date=datetime.now(timezone.utc),
        chat=_chat(user.id),
        from_user=user,
        text="hi",
    )


def test_extract_user_from_message():
    # setup: build update with message user
    user = _user(1)
    event = Update(update_id=1, message=_message(user))

    # action: extract user from event
    result = extract_user_from_event(event)

    # check: user is returned from message
    assert result == user


def test_extract_user_from_callback_query():
    # setup: build update with callback query user
    user = _user(2)
    callback = CallbackQuery(
        id="cbq",
        from_user=user,
        chat_instance="inst",
        data="x",
        message=_message(user),
    )
    event = Update(update_id=2, callback_query=callback)

    # action: extract user from event
    result = extract_user_from_event(event)

    # check: user is returned from callback query
    assert result == user


def test_extract_user_from_event_handles_errors():
    # setup: event with broken message property
    class BadEvent:
        @property
        def message(self):
            raise RuntimeError("boom")

    event = BadEvent()

    # action: extract user from event
    result = extract_user_from_event(event)

    # check: errors are swallowed and None returned
    assert result is None
