"""Offline wire-format regression tests for incremental Bot API 10.2/10.3 support."""

import json
from datetime import UTC, datetime

import pytest

from telegram import (
    Bot,
    BotCommand,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
    User,
)
from telegram.ext import Defaults, ExtBot
from telegram.request import BaseRequest


class RecordingRequest(BaseRequest):
    """Capture the final request without contacting Telegram."""

    def __init__(self):
        self.calls = []

    @property
    def read_timeout(self):
        return 5

    async def initialize(self):
        pass

    async def shutdown(self):
        pass

    async def do_request(self, url, method, request_data=None, **kwargs):
        endpoint = url.rsplit("/", 1)[-1]
        self.calls.append((endpoint, request_data.parameters))
        result = {"id": 123, "is_bot": True, "first_name": "Test"} if endpoint == "getMe" else True
        return 200, json.dumps({"ok": True, "result": result}).encode()


@pytest.mark.no_req
class TestBotAPIQuickWinsWithoutRequest:
    @pytest.mark.parametrize("value", [None, False, True])
    @pytest.mark.parametrize(
        ("cls", "payload", "field"),
        [
            (BotCommand, {"command": "help", "description": "Help"}, "is_ephemeral"),
            (
                InlineKeyboardMarkup,
                {"inline_keyboard": [[{"text": "OK", "callback_data": "ok"}]]},
                "force_reply",
            ),
            (ReplyKeyboardMarkup, {"keyboard": [[{"text": "OK"}]]}, "force_reply"),
        ],
    )
    def test_round_trip(self, cls, payload, field, value):
        data = {**payload, field: value, "future_field": 42}
        obj = cls.de_json(data)
        assert getattr(obj, field) is value
        assert obj.api_kwargs == {"future_field": 42}
        expected = {**payload, "future_field": 42}
        if value is not None:
            expected[field] = value
        assert obj.to_dict() == expected

    @pytest.mark.parametrize("factory", ["from_button", "from_row", "from_column"])
    @pytest.mark.parametrize("cls", [InlineKeyboardMarkup, ReplyKeyboardMarkup])
    def test_keyboard_shortcuts(self, factory, cls):
        button = (
            InlineKeyboardButton("OK", callback_data="ok") if cls is InlineKeyboardMarkup else "OK"
        )
        arg = button if factory == "from_button" else [button]
        assert getattr(cls, factory)(arg, force_reply=True).to_dict()["force_reply"] is True

    @pytest.mark.parametrize("ext", [False, True])
    @pytest.mark.parametrize("value", [None, False, True])
    async def test_draft_wire_and_shortcuts(self, ext, value):
        request = RecordingRequest()
        bot = (
            ExtBot("123:TEST", request=request, defaults=Defaults(parse_mode="HTML"))
            if ext
            else Bot("123:TEST", request=request)
        )
        async with bot:
            chat = Chat(123, "private")
            user = User(123, "Test", False)
            message = Message(1, datetime.now(UTC), chat)
            for obj in (chat, user, message):
                obj.set_bot(bot)
            calls = [
                (bot.send_message_draft, {"chat_id": 123}),
                (chat.send_message_draft, {}),
                (user.send_message_draft, {}),
                (message.reply_text_draft, {}),
            ]
            for method, extra in calls:
                assert await method(
                    draft_id=7, text="", can_stop=value, keep_on_stop=value, **extra
                )
                endpoint, payload = request.calls[-1]
                assert endpoint == "sendMessageDraft"
                assert payload["chat_id"] == 123
                assert payload["text"] == ""
                for field in ("can_stop", "keep_on_stop"):
                    if value is None:
                        assert field not in payload
                    else:
                        assert payload[field] is value
                if ext:
                    assert payload["parse_mode"] == "HTML"

    async def test_command_and_keyboard_wire(self):
        request = RecordingRequest()
        async with Bot("123:TEST", request=request) as bot:
            await bot.set_my_commands([BotCommand("help", "Help", is_ephemeral=True)])
            assert request.calls[-1][1]["commands"][0]["is_ephemeral"] is True
            await bot.send_message(
                123, "Reply", reply_markup=InlineKeyboardMarkup([], force_reply=True)
            )
            assert request.calls[-1][1]["reply_markup"]["force_reply"] is True
