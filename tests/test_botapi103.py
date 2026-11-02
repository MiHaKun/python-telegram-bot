"""Integration coverage for the complete Bot API 10.1-10.3 adaptation."""

import datetime as dtm
import inspect
import json
import pickle
import re
from copy import deepcopy
from pathlib import Path

import pytest

import telegram as tg
from telegram.ext import BaseRateLimiter, Defaults, ExtBot, filters
from telegram.request._requestparameter import RequestParameter
from tests.test_bot_api_quick_wins import RecordingRequest

SCHEMA = json.loads(
    (Path(__file__).parent / "data/bot_api_10_3_schema.json").read_text(encoding="utf-8")
)
MODEL_NAMES = [
    n
    for n in tg.__all__
    if inspect.isclass(c := getattr(tg, n)) and c.__module__ == "telegram._botapi103"
]


def sample(name, optional=False):
    """Build independent API-shaped payloads from the official response tables."""
    if name == "RichText":
        return ["plain", {"type": "bold", "text": "bold"}]
    if name in ("RichBlock", "InputRichBlock"):
        return {"type": "paragraph", "text": "paragraph"}
    if name == "InputMedia":
        return {"type": "photo", "media": "file_id"}
    if name == "Chat":
        return {"id": 123, "type": "private"}
    if name == "User":
        return {"id": 123, "is_bot": False, "first_name": "Test"}
    if name == "MessageEntity":
        return {"type": "bold", "offset": 0, "length": 1}
    primitive = {"String": "test", "Integer": 1, "Float": 1.5, "Boolean": True, "True": True}
    if name in primitive:
        return primitive[name]
    if name.startswith("Array of "):
        return [sample(name[9:], optional)]
    if " or " in name:
        return sample(name.split(" or ")[0], optional)
    result = {}
    for field in SCHEMA[name]["fields"]:
        if not field["required"] and not optional:
            continue
        if field["name"] == "type" and field["required"]:
            result["type"] = re.search(
                r'(?:always|must be) [“"\']?([a-z_]+)', field["description"]
            )[1]
        else:
            result[field["name"]] = sample(field["type"], optional)
    return result


class RichRequest(RecordingRequest):
    """Return API-shaped messages and capture multipart data."""

    async def do_request(self, url, method, request_data=None, **kwargs):
        self.multipart = request_data.multipart_data
        endpoint = url.rsplit("/", 1)[-1]
        self.calls.append((endpoint, request_data.parameters))
        if endpoint == "getMe":
            result = {"id": 123, "is_bot": True, "first_name": "Test"}
        elif endpoint in ("sendRichMessage", "editMessageText"):
            result = {
                "message_id": 1,
                "date": 1,
                "chat": {"id": 123, "type": "private"},
                "rich_message": {"blocks": [{"type": "paragraph", "text": "ok"}]},
            }
        else:
            result = True
        return 200, json.dumps({"ok": True, "result": result}).encode()


class RecordingLimiter(BaseRateLimiter):
    """Record passage through the ExtBot limiter."""

    def __init__(self):
        self.calls = []

    async def initialize(self):
        pass

    async def shutdown(self):
        pass

    async def process_request(self, callback, args, kwargs, endpoint, data, rate_limit_args):
        self.calls.append((endpoint, rate_limit_args))
        return await callback(*args, **kwargs)


@pytest.mark.no_req
class TestBotAPI103WithoutRequest:
    @pytest.mark.parametrize("name", MODEL_NAMES)
    @pytest.mark.parametrize("optional", [False, True])
    def test_native_model_round_trip(self, name, optional):
        data = sample(name, optional)
        original = deepcopy(data)
        result = getattr(tg, name).de_json(data)
        assert data == original
        if isinstance(result, tg.TelegramObject):
            assert json.loads(result.to_json()) == original
            assert deepcopy(result).to_dict() == result.to_dict()

    async def test_rich_upload_defaults_limiter_and_edit(self):
        request = RichRequest()
        limiter = RecordingLimiter()
        bot = ExtBot(
            "123:TEST",
            request=request,
            rate_limiter=limiter,
            defaults=Defaults(disable_notification=True, parse_mode="HTML"),
        )
        photo = tg.InputMediaPhoto(b"image")
        rich = tg.InputRichMessage(
            blocks=[
                tg.InputRichBlockDetails(summary="Details", blocks=[tg.InputRichBlockPhoto(photo)])
            ]
        )
        async with bot:
            message = await bot.send_rich_message(123, rich, rate_limit_args="test")
            assert isinstance(message.rich_message, tg.RichMessage)
            assert isinstance(message.rich_message.blocks[0], tg.RichBlockParagraph)
            endpoint, payload = request.calls[-1]
            assert endpoint == "sendRichMessage"
            assert payload["disable_notification"] is True
            assert "parse_mode" not in payload
            assert request.multipart
            assert photo.media.attach_name in request.multipart
            assert isinstance(photo.media, tg.InputFile)
            assert limiter.calls[-1] == ("sendRichMessage", "test")
            await bot.edit_message_text(
                chat_id=123, message_id=1, rich_message=tg.InputRichMessage(html="<p>edited</p>")
            )
            assert request.calls[-1][1]["rich_message"] == {"html": "<p>edited</p>"}
            assert "text" not in request.calls[-1][1]
            assert "parse_mode" not in request.calls[-1][1]
            with pytest.raises(ValueError, match="uploads"):
                await bot.send_rich_message_draft(123, 1, rich)

    async def test_ephemeral_requests(self):
        request = RichRequest()
        async with tg.Bot("123:TEST", request=request) as bot:
            await bot.send_message(
                123,
                "private",
                ephemeral_message_parameters=tg.EphemeralMessageParameters(
                    456, replace_callback_query_message=False
                ),
            )
            assert request.calls[-1][1]["ephemeral_message_parameters"] == {
                "receiver_user_id": 456,
                "replace_callback_query_message": False,
            }
            for name in (
                "edit_ephemeral_message_text",
                "edit_ephemeral_message_caption",
                "edit_ephemeral_message_reply_markup",
                "delete_ephemeral_message",
            ):
                await getattr(bot, name)(123, 456, 7)
                assert request.calls[-1][1]["ephemeral_message_id"] == 7
            await bot.edit_ephemeral_message_media(123, 456, 7, tg.InputMediaPhoto(b"image"))
            assert request.multipart

    def test_rich_file_validation(self):
        with pytest.raises(ValueError, match="attach=True"):
            RequestParameter.from_input(
                "rich_message",
                tg.InputRichMessage(
                    blocks=[tg.InputRichBlockPhoto(tg.InputMediaPhoto(tg.InputFile(b"x")))]
                ),
            )

    def test_subscription_and_community(self):
        update = tg.Update.de_json(
            {
                "update_id": 1,
                "subscription": {
                    "user": sample("User"),
                    "invoice_payload": "sub",
                    "state": "canceled",
                },
            }
        )
        assert update.effective_user.id == 123
        assert update.effective_chat is None
        assert tg.Update.SUBSCRIPTION in tg.Update.ALL_TYPES
        message = tg.Message.de_json(
            {
                "message_id": 1,
                "date": 1,
                "chat": sample("Chat"),
                "community_chat_added": {"community": {"id": 77, "name": "Test"}},
            }
        )
        assert isinstance(message.community_chat_added.community, tg.Community)
        assert tg.ReplyParameters(ephemeral_message_id=7).to_dict() == {"ephemeral_message_id": 7}

    def test_recursive_entities_media_dispatch_and_persistence(self):
        deep = tg.RichTextBold(["a", ["b", [tg.RichTextItalic("c")]]])
        assert tg.RichText.de_json(json.loads(deep.to_json())).text[1][1][0].text == "c"
        voice = tg.InputMediaVoiceNote("file_id", duration=dtm.timedelta(seconds=7))
        assert voice.to_dict()["duration"] == 7
        rich = tg.RichMessage.de_json(
            {
                "blocks": [
                    {
                        "type": "table",
                        "cells": [
                            [
                                {
                                    "align": "left",
                                    "valign": "top",
                                    "text": [
                                        "plain",
                                        {
                                            "type": "bold",
                                            "text": [
                                                {"type": "italic", "text": "nested"},
                                                {
                                                    "type": "date_time",
                                                    "text": "date",
                                                    "unix_time": 1,
                                                    "date_time_format": "d",
                                                },
                                            ],
                                        },
                                    ],
                                }
                            ]
                        ],
                        "caption": {"type": "url", "text": "link", "url": "https://telegram.org"},
                    }
                ]
            }
        )
        cell = rich.blocks[0].cells[0][0]
        assert isinstance(cell.text[1].text[0], tg.RichTextItalic)
        assert cell.text[1].text[1].unix_time == dtm.datetime.fromtimestamp(1, dtm.UTC)
        assert pickle.loads(pickle.dumps(rich)).to_dict() == rich.to_dict()
        for kind, expected in [
            ("photo", tg.InputMediaPhoto),
            ("voice_note", tg.InputMediaVoiceNote),
        ]:
            media = tg.InputRichMessageMedia.de_json(
                {"id": "x", "media": {"type": kind, "media": "file_id"}}
            )
            assert isinstance(media.media, expected)
        unknown = tg.RichBlock.de_json({"type": "future", "new_field": 42})
        assert unknown.to_dict() == {"type": "future", "new_field": 42}

    async def test_shortcuts_filters_and_ephemeral_identity(self):
        request = RichRequest()
        async with tg.Bot("123:TEST", request=request) as bot:
            message = tg.Message.de_json(
                {
                    "message_id": 0,
                    "date": 1,
                    "chat": {"id": -123, "type": "supergroup"},
                    "ephemeral_message_id": 7,
                    "receiver_user": sample("User"),
                    "rich_message": {"blocks": []},
                },
                bot,
            )
            other = tg.Message.de_json({**message.to_dict(), "ephemeral_message_id": 8}, bot)
            assert message != other
            assert filters.RICH_MESSAGE.check_update(tg.Update(1, message=message))
            assert message.effective_attachment is message.rich_message
            await message.edit_text(rich_message=tg.InputRichMessage(markdown="Edited"))
            assert request.calls[-1][0] == "editEphemeralMessageText"
            assert request.calls[-1][1]["receiver_user_id"] == 123
            for method, endpoint in [
                (message.edit_caption, "editEphemeralMessageCaption"),
                (message.edit_reply_markup, "editEphemeralMessageReplyMarkup"),
                (message.delete, "deleteEphemeralMessage"),
            ]:
                await method()
                assert request.calls[-1][0] == endpoint
            await message.edit_media(tg.InputMediaPhoto(b"image"))
            assert request.calls[-1][0] == "editEphemeralMessageMedia"
            assert request.multipart
            reply = message.build_reply_arguments()["reply_parameters"].to_dict()
            assert reply["ephemeral_message_id"] == 7
            assert "message_id" not in reply
            await message.reply_rich_message(
                tg.InputRichMessage(markdown="Reply"),
                ephemeral_message_parameters=tg.EphemeralMessageParameters(123),
                do_quote=True,
            )
            assert request.calls[-1][1]["reply_parameters"]["ephemeral_message_id"] == 7
            await message.reply_rich_message_draft(1, tg.InputRichMessage(markdown="Draft"))
            assert request.calls[-1][0] == "sendRichMessageDraft"
        for field in ("community_chat_added", "community_chat_joined", "community_chat_removed"):
            message = tg.Message.de_json(
                {
                    "message_id": 1,
                    "date": 1,
                    "chat": sample("Chat"),
                    field: sample("".join(p.title() for p in field.split("_"))),
                }
            )
            update = tg.Update(1, message=message)
            assert getattr(filters.StatusUpdate, field.upper()).check_update(update)
            assert filters.StatusUpdate.ALL.check_update(update)

    async def test_inline_join_and_callback_cache(self):
        request = RichRequest()
        async with ExtBot("123:TEST", request=request, arbitrary_callback_data=True) as bot:
            markup = tg.InlineKeyboardMarkup.from_button(
                tg.InlineKeyboardButton("x", callback_data={"x": 1}), force_reply=True
            )
            await bot.send_rich_message(
                123, tg.InputRichMessage(markdown="test"), reply_markup=markup
            )
            assert request.calls[-1][1]["reply_markup"]["force_reply"] is True
            assert isinstance(markup.inline_keyboard[0][0].callback_data, dict)
            content = tg.InputRichMessageContent(tg.InputRichMessage(markdown="inline"))
            result = tg.InlineQueryResultArticle("1", "Title", content)
            await bot.answer_inline_query("query", [result])
            assert request.calls[-1][1]["results"][0]["input_message_content"]["rich_message"] == {
                "markdown": "inline"
            }
            parsed = tg.InlineQueryResultArticle.de_json(result.to_dict(), bot)
            assert isinstance(parsed.input_message_content, tg.InputRichMessageContent)
            bad = tg.InputRichMessageContent(
                tg.InputRichMessage(blocks=[tg.InputRichBlockPhoto(tg.InputMediaPhoto(b"file"))])
            )
            with pytest.raises(ValueError, match="inline rich content"):
                await bot.answer_inline_query(
                    "query", [tg.InlineQueryResultArticle("1", "Title", bad)]
                )
            join = tg.ChatJoinRequest.de_json(
                {
                    "chat": sample("Chat"),
                    "from": sample("User"),
                    "date": 1,
                    "user_chat_id": 123,
                    "query_id": "join-query",
                },
                bot,
            )
            await join.answer_query("queue")
            assert request.calls[-1] == (
                "answerChatJoinRequestQuery",
                {"chat_join_request_query_id": "join-query", "result": "queue"},
            )
            await join.send_web_app("https://example.com")
            assert request.calls[-1][0] == "sendChatJoinRequestWebApp"
