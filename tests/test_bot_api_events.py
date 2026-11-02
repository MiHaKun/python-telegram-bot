"""Offline integration tests for disabled buttons and stopped generation updates."""

import json
import pickle
from copy import deepcopy

import pytest

from telegram import (
    Bot,
    Chat,
    DisabledButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MessageGenerationStopped,
    Update,
)
from telegram.ext import Application, ExtBot, TypeHandler
from tests.test_bot_api_quick_wins import RecordingRequest


@pytest.mark.no_req
class TestBotAPIEventsWithoutRequest:
    def test_disabled_empty_object_round_trip(self):
        data = {"inline_keyboard": [[{"text": "Unavailable", "disabled": {}}]]}
        keyboard = InlineKeyboardMarkup.de_json(data)
        button = keyboard.inline_keyboard[0][0]
        assert isinstance(button.disabled, DisabledButton)
        assert not button.api_kwargs
        assert keyboard.to_dict() == data
        assert json.loads(keyboard.to_json()) == data
        assert deepcopy(keyboard).to_dict() == data
        assert pickle.loads(pickle.dumps(keyboard)).to_dict() == data
        with pytest.raises(AttributeError):
            button.disabled = None

    def test_disabled_button_equality(self):
        first = InlineKeyboardButton("Wait", disabled=DisabledButton())
        second = InlineKeyboardButton("Wait", disabled=DisabledButton())
        enabled = InlineKeyboardButton("Wait")
        assert first == second
        assert hash(first) == hash(second)
        assert first != enabled
        assert DisabledButton.de_json({"future": 1}).to_dict() == {"future": 1}

    async def test_disabled_button_wire(self):
        request = RecordingRequest()
        async with Bot("123:TEST", request=request) as bot:
            await bot.send_message(
                123,
                "Waiting",
                reply_markup=InlineKeyboardMarkup.from_button(
                    InlineKeyboardButton("Wait", disabled=DisabledButton())
                ),
            )
        assert request.calls[-1][1]["reply_markup"]["inline_keyboard"][0][0]["disabled"] == {}

    @pytest.mark.parametrize("thread_id", [None, 42])
    def test_stopped_event_round_trip(self, thread_id):
        event = {"chat": {"id": 123, "type": "private"}, "draft_id": 7, "future": True}
        if thread_id is not None:
            event["message_thread_id"] = thread_id
        data = {"update_id": 99, "stopped_message_generation": event}
        original = deepcopy(data)
        bot = Bot("123:TEST")
        update = Update.de_json(data, bot)
        stopped = update.stopped_message_generation
        assert isinstance(stopped, MessageGenerationStopped)
        assert isinstance(stopped.chat, Chat)
        assert stopped.get_bot() is bot
        assert stopped.chat.get_bot() is bot
        assert stopped.message_thread_id == thread_id
        assert stopped.api_kwargs == {"future": True}
        assert update.effective_chat is stopped.chat
        assert update.effective_user is None
        assert update.effective_sender is None
        assert update.effective_message is None
        assert update.to_dict() == original
        assert data == original
        assert pickle.loads(pickle.dumps(update)).to_dict() == original
        assert deepcopy(update).to_dict() == original
        assert Update.STOPPED_MESSAGE_GENERATION in Update.ALL_TYPES

    def test_event_identity(self):
        chat = Chat(1, "private")
        first = MessageGenerationStopped(chat, 7, 42)
        second = MessageGenerationStopped(chat, 7, 42)
        assert first == second
        assert hash(first) == hash(second)
        assert first != MessageGenerationStopped(chat, 8, 42)
        assert first != MessageGenerationStopped(chat, 7, 43)
        with pytest.raises(AttributeError):
            first.draft_id = 9

    async def test_application_dispatch(self):
        seen = []

        async def on_update(update, context):
            if event := update.stopped_message_generation:
                seen.append((event.chat.id, event.message_thread_id, event.draft_id))
                context.chat_data["stopped_draft"] = event.draft_id
                assert context.user_data is None

        bot = ExtBot("123:TEST", request=RecordingRequest())
        app = Application.builder().bot(bot).updater(None).build()
        app.add_handler(TypeHandler(Update, on_update), group=-1)
        async with app:
            update = Update.de_json(
                {
                    "update_id": 100,
                    "stopped_message_generation": {
                        "chat": {"id": 123, "type": "private"},
                        "message_thread_id": 42,
                        "draft_id": 7,
                    },
                },
                bot,
            )
            await app.process_update(update)
        assert seen == [(123, 42, 7)]
        assert app.chat_data[123]["stopped_draft"] == 7
