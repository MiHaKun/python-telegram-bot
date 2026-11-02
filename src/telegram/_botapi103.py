#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2026
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

"""Bot API 10.1-10.3 models, generated as static source from the official schema.

These reviewed model definitions are maintained directly as ordinary Python source.
"""

import datetime as dtm
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, ClassVar, TypeAlias

from telegram._inline.inputmessagecontent import InputMessageContent
from telegram._telegramobject import TelegramObject
from telegram._utils.de_json import get_telegram_namespace
from telegram._utils.types import JSONDict


def _tuples(value: Any) -> Any:
    """Normalize nested arrays without changing their elements."""
    if isinstance(value, (list, tuple)):
        return tuple(_tuples(item) for item in value)
    return value


def _rich_dict(value: Any) -> Any:
    """Serialize the arbitrary array depth allowed by RichTextValue."""
    if isinstance(value, TelegramObject):
        return value.to_dict()
    if isinstance(value, (list, tuple)):
        return [_rich_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: _rich_dict(item) for key, item in value.items()}
    return value


if TYPE_CHECKING:
    from telegram import (
        Animation,
        Audio,
        Bot,
        CopyTextButton,
        DisabledButton,
        Document,
        InputMediaAnimation,
        InputMediaAudio,
        InputMediaDocument,
        InputMediaPhoto,
        InputMediaVideo,
        InputMediaVoiceNote,
        Location,
        LoginUrl,
        PhotoSize,
        SwitchInlineQueryChosenChat,
        User,
        Video,
        Voice,
        WebAppInfo,
    )


class _RichObject(TelegramObject):
    """Add the two polymorphic input unions to the normal annotation-based parser."""

    __slots__ = ()

    def to_dict(self, recursive: bool = True) -> JSONDict:
        """Preserve the base conversion rules and support recursive rich-text arrays."""
        data = super().to_dict(recursive=recursive)
        return _rich_dict(data) if recursive else data

    @classmethod
    def _build_plan(cls) -> dict[str, Any]:
        plan = super()._build_plan()
        for name, annotation in cls.__init__.__annotations__.items():
            if isinstance(annotation, str) and "RichTextValue" in annotation:
                plan[name] = RichText
        if cls.__name__ == "InputRichMessageMedia":
            plan["media"] = get_telegram_namespace()["InputMedia"]
        return plan


class RichText(_RichObject):
    """This object represents a rich formatted text. Currently, it can be either a String for plain
    text, an Array of RichText , or any of the following types: Unknown entity kinds preserve
    their fields in api_kwargs.

    Args:
        type (:obj:`str`): Discriminator of the entity.

    Attributes:
        type (:obj:`str`): Discriminator of the entity.
    """

    __slots__ = ("type",)
    __DE_JSON_DISPATCH__: ClassVar[tuple[str, dict[str, str]] | None] = (
        "type",
        {
            "bold": "RichTextBold",
            "italic": "RichTextItalic",
            "underline": "RichTextUnderline",
            "strikethrough": "RichTextStrikethrough",
            "spoiler": "RichTextSpoiler",
            "date_time": "RichTextDateTime",
            "text_mention": "RichTextTextMention",
            "subscript": "RichTextSubscript",
            "superscript": "RichTextSuperscript",
            "marked": "RichTextMarked",
            "code": "RichTextCode",
            "custom_emoji": "RichTextCustomEmoji",
            "mathematical_expression": "RichTextMathematicalExpression",
            "url": "RichTextUrl",
            "email_address": "RichTextEmailAddress",
            "phone_number": "RichTextPhoneNumber",
            "bank_card_number": "RichTextBankCardNumber",
            "mention": "RichTextMention",
            "hashtag": "RichTextHashtag",
            "cashtag": "RichTextCashtag",
            "bot_command": "RichTextBotCommand",
            "button": "RichTextButton",
            "anchor": "RichTextAnchor",
            "anchor_link": "RichTextAnchorLink",
            "reference": "RichTextReference",
            "reference_link": "RichTextReferenceLink",
        },
    )

    def __init__(self, type: str, *, api_kwargs: JSONDict | None = None) -> None:
        super().__init__(api_kwargs=api_kwargs)
        self.type = type
        self._id_attrs = (type,)
        self._freeze()

    @classmethod
    def de_json(cls, data: Any, bot: "Bot | None" = None) -> Any:
        """Parse plain text, arrays, or typed rich text entities recursively."""
        if data is None or isinstance(data, str):
            return data
        if isinstance(data, (list, tuple)):
            return tuple(cls.de_json(item, bot) for item in data)
        return super().de_json(data, bot)


RichTextValue: TypeAlias = str | RichText | Sequence["RichTextValue"]
"""Recursive rich text: a string, a typed entity, or a sequence of either."""


class RichBlock(_RichObject):
    """This object represents a block in a rich formatted message. Currently, it can be any of the
    following types: Unknown entity kinds preserve their fields in api_kwargs.

    Args:
        type (:obj:`str`): Discriminator of the entity.

    Attributes:
        type (:obj:`str`): Discriminator of the entity.
    """

    __slots__ = ("type",)
    __DE_JSON_DISPATCH__: ClassVar[tuple[str, dict[str, str]] | None] = (
        "type",
        {
            "paragraph": "RichBlockParagraph",
            "heading": "RichBlockSectionHeading",
            "pre": "RichBlockPreformatted",
            "footer": "RichBlockFooter",
            "divider": "RichBlockDivider",
            "mathematical_expression": "RichBlockMathematicalExpression",
            "anchor": "RichBlockAnchor",
            "list": "RichBlockList",
            "blockquote": "RichBlockBlockQuotation",
            "expandable_blockquote": "RichBlockExpandableBlockQuotation",
            "pullquote": "RichBlockPullQuotation",
            "collage": "RichBlockCollage",
            "slideshow": "RichBlockSlideshow",
            "table": "RichBlockTable",
            "details": "RichBlockDetails",
            "map": "RichBlockMap",
            "buttons": "RichBlockButtons",
            "animation": "RichBlockAnimation",
            "audio": "RichBlockAudio",
            "document": "RichBlockDocument",
            "photo": "RichBlockPhoto",
            "video": "RichBlockVideo",
            "voice_note": "RichBlockVoiceNote",
            "thinking": "RichBlockThinking",
        },
    )

    def __init__(self, type: str, *, api_kwargs: JSONDict | None = None) -> None:
        super().__init__(api_kwargs=api_kwargs)
        self.type = type
        self._id_attrs = (type,)
        self._freeze()


class InputRichBlock(_RichObject):
    """This object represents a block in a rich formatted message to be sent. Currently, it can be
    any of the following types: Unknown entity kinds preserve their fields in api_kwargs.

    Args:
        type (:obj:`str`): Discriminator of the entity.

    Attributes:
        type (:obj:`str`): Discriminator of the entity.
    """

    __slots__ = ("type",)
    __DE_JSON_DISPATCH__: ClassVar[tuple[str, dict[str, str]] | None] = (
        "type",
        {
            "paragraph": "InputRichBlockParagraph",
            "heading": "InputRichBlockSectionHeading",
            "pre": "InputRichBlockPreformatted",
            "footer": "InputRichBlockFooter",
            "divider": "InputRichBlockDivider",
            "mathematical_expression": "InputRichBlockMathematicalExpression",
            "anchor": "InputRichBlockAnchor",
            "list": "InputRichBlockList",
            "blockquote": "InputRichBlockBlockQuotation",
            "expandable_blockquote": "InputRichBlockExpandableBlockQuotation",
            "pullquote": "InputRichBlockPullQuotation",
            "collage": "InputRichBlockCollage",
            "slideshow": "InputRichBlockSlideshow",
            "table": "InputRichBlockTable",
            "details": "InputRichBlockDetails",
            "map": "InputRichBlockMap",
            "buttons": "InputRichBlockButtons",
            "animation": "InputRichBlockAnimation",
            "audio": "InputRichBlockAudio",
            "document": "InputRichBlockDocument",
            "photo": "InputRichBlockPhoto",
            "video": "InputRichBlockVideo",
            "voice_note": "InputRichBlockVoiceNote",
            "thinking": "InputRichBlockThinking",
        },
    )

    def __init__(self, type: str, *, api_kwargs: JSONDict | None = None) -> None:
        super().__init__(api_kwargs=api_kwargs)
        self.type = type
        self._id_attrs = (type,)
        self._freeze()


class EphemeralMessageParameters(_RichObject):
    """Parameters for EphemeralMessageParameters.

    Args:
        receiver_user_id (:obj:`int`): Identifier of the user who will receive the message. It is
            not guaranteed that the user will receive the message, especially if they are offline.
            See here for more details.
        callback_query_id (:obj:`str`, optional): Identifier of the callback query which triggered
            the message, if any
        replace_callback_query_message (:obj:`bool`, optional): Pass True if the ephemeral message
            must be shown in place of the original message. Must be False for callback queries
            from ephemeral messages, which must be edited using regular editEphemeralMessage…
            methods.

    Attributes:
        receiver_user_id (:obj:`int`): Identifier of the user who will receive the message. It is
            not guaranteed that the user will receive the message, especially if they are offline.
            See here for more details.
        callback_query_id (:obj:`str`): Optional. Identifier of the callback query which triggered
            the message, if any
        replace_callback_query_message (:obj:`bool`): Optional. Pass True if the ephemeral message
            must be shown in place of the original message. Must be False for callback queries
            from ephemeral messages, which must be edited using regular editEphemeralMessage…
            methods.
    """

    __slots__ = ("callback_query_id", "receiver_user_id", "replace_callback_query_message")

    def __init__(
        self,
        receiver_user_id: "int",
        callback_query_id: "str | None" = None,
        replace_callback_query_message: "bool | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.receiver_user_id = receiver_user_id
            self.callback_query_id = callback_query_id
            self.replace_callback_query_message = replace_callback_query_message
        self._id_attrs = (
            self.receiver_user_id,
            self.callback_query_id,
            self.replace_callback_query_message,
        )
        self._freeze()


class Link(_RichObject):
    """Represents an HTTP link.

    Args:
        url (:obj:`str`): URL of the link

    Attributes:
        url (:obj:`str`): URL of the link
    """

    __slots__ = ("url",)

    def __init__(
        self,
        url: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.url = url
        self._id_attrs = (self.url,)
        self._freeze()


class BotSubscriptionUpdated(_RichObject):
    """This object contains information about changes to a user payment subscription toward the
    current bot.

    Args:
        user (:class:`telegram.User`): User who subscribed for payments toward the bot
        invoice_payload (:obj:`str`): Bot-specified invoice payload
        state (:obj:`str`): The new state of the subscription. Currently, it can be one of
            “canceled” if the user canceled the subscription, “active” if the user re-enabled a
            previously canceled subscription, or “failed” if payment for the subscription failed.

    Attributes:
        user (:class:`telegram.User`): User who subscribed for payments toward the bot
        invoice_payload (:obj:`str`): Bot-specified invoice payload
        state (:obj:`str`): The new state of the subscription. Currently, it can be one of
            “canceled” if the user canceled the subscription, “active” if the user re-enabled a
            previously canceled subscription, or “failed” if payment for the subscription failed.
    """

    __slots__ = ("invoice_payload", "state", "user")

    def __init__(
        self,
        user: "User",
        invoice_payload: "str",
        state: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.user = user
            self.invoice_payload = invoice_payload
            self.state = state
        self._id_attrs = (
            self.user,
            self.invoice_payload,
            self.state,
        )
        self._freeze()


class Community(_RichObject):
    """Represents a community (a group of chats).

    Args:
        id (:obj:`int`): Unique identifier for this community. This number may have more than 32
            significant bits and some programming languages may have difficulty/silent defects in
            interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or
            double-precision float type are safe for storing this identifier.
        name (:obj:`str`): Name of the community

    Attributes:
        id (:obj:`int`): Unique identifier for this community. This number may have more than 32
            significant bits and some programming languages may have difficulty/silent defects in
            interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or
            double-precision float type are safe for storing this identifier.
        name (:obj:`str`): Name of the community
    """

    __slots__ = ("id", "name")

    def __init__(
        self,
        id: "int",
        name: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.id = id
            self.name = name
        self._id_attrs = (
            self.id,
            self.name,
        )
        self._freeze()


class CommunityChatAdded(_RichObject):
    """Describes a service message about a chat or a bot being added to a community.

    Args:
        community (:class:`telegram.Community`): The new community to which the chat or the bot
            belongs

    Attributes:
        community (:class:`telegram.Community`): The new community to which the chat or the bot
            belongs
    """

    __slots__ = ("community",)

    def __init__(
        self,
        community: "Community",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.community = community
        self._id_attrs = (self.community,)
        self._freeze()


class CommunityChatJoined(_RichObject):
    """Describes a service message about a chat being joined by a user from a community.

    Args:
        community (:class:`telegram.Community`): The community from which the chat was joined

    Attributes:
        community (:class:`telegram.Community`): The community from which the chat was joined
    """

    __slots__ = ("community",)

    def __init__(
        self,
        community: "Community",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.community = community
        self._id_attrs = (self.community,)
        self._freeze()


class CommunityChatRemoved(_RichObject):
    """Describes a service message about a chat or a bot being removed from a community. Currently
    holds no information.
    """

    __slots__ = ()

    def __init__(
        self,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        self._freeze()


class RichMessage(_RichObject):
    """Rich formatted message.

    Args:
        blocks (Sequence[:class:`telegram.RichBlock`]): Content of the message
        is_rtl (:obj:`bool`, optional): True , if the rich message must be shown right-to-left

    Attributes:
        blocks (tuple[:class:`telegram.RichBlock`]): Content of the message
        is_rtl (:obj:`bool`): Optional. True , if the rich message must be shown right-to-left
    """

    __slots__ = ("blocks", "is_rtl")

    def __init__(
        self,
        blocks: "Sequence[RichBlock]",
        is_rtl: "bool | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.is_rtl = is_rtl
        self._id_attrs = (
            self.blocks,
            self.is_rtl,
        )
        self._freeze()


class InputRichMessage(_RichObject):
    """Describes a rich message to be sent. Exactly one of the fields html , markdown , or blocks
    must be used.

    Args:
        blocks (Sequence[:class:`telegram.InputRichBlock`], optional): Content of the rich message
            to send described as a list of blocks
        html (:obj:`str`, optional): Content of the rich message to send described using HTML
            formatting. See rich message formatting options for more details. Use media field to
            specify the media used in the message.
        markdown (:obj:`str`, optional): Content of the rich message to send described using
            Markdown formatting. See rich message formatting options for more details. Use media
            field to specify the media used in the message.
        media (Sequence[:class:`telegram.InputRichMessageMedia`], optional): List of media that
            are specified in the markdown or html fields using tg://photo?id= , tg://video?id= ,
            tg://document?id= , and tg://audio?id= links
        is_rtl (:obj:`bool`, optional): Pass True if the rich message must be shown right-to-left
        skip_entity_detection (:obj:`bool`, optional): Pass True to skip automatic detection of
            entities (e.g., URLs, email addresses, username mentions, hashtags, cashtags, bot
            commands, or phone numbers) in the text

    Attributes:
        blocks (tuple[:class:`telegram.InputRichBlock`]): Optional. Content of the rich message to
            send described as a list of blocks
        html (:obj:`str`): Optional. Content of the rich message to send described using HTML
            formatting. See rich message formatting options for more details. Use media field to
            specify the media used in the message.
        markdown (:obj:`str`): Optional. Content of the rich message to send described using
            Markdown formatting. See rich message formatting options for more details. Use media
            field to specify the media used in the message.
        media (tuple[:class:`telegram.InputRichMessageMedia`]): Optional. List of media that are
            specified in the markdown or html fields using tg://photo?id= , tg://video?id= ,
            tg://document?id= , and tg://audio?id= links
        is_rtl (:obj:`bool`): Optional. Pass True if the rich message must be shown right-to-left
        skip_entity_detection (:obj:`bool`): Optional. Pass True to skip automatic detection of
            entities (e.g., URLs, email addresses, username mentions, hashtags, cashtags, bot
            commands, or phone numbers) in the text
    """

    __slots__ = ("blocks", "html", "is_rtl", "markdown", "media", "skip_entity_detection")

    def __init__(
        self,
        blocks: "Sequence[InputRichBlock] | None" = None,
        html: "str | None" = None,
        markdown: "str | None" = None,
        media: "Sequence[InputRichMessageMedia] | None" = None,
        is_rtl: "bool | None" = None,
        skip_entity_detection: "bool | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.html = html
            self.markdown = markdown
            self.media = _tuples(media) if media is not None else ()
            self.is_rtl = is_rtl
            self.skip_entity_detection = skip_entity_detection
        self._id_attrs = (
            self.blocks,
            self.html,
            self.markdown,
            self.media,
            self.is_rtl,
            self.skip_entity_detection,
        )
        self._freeze()


class InputRichMessageMedia(_RichObject):
    """Describes a media element embedded in an outgoing rich message.

    Args:
        id (:obj:`str`): Unique identifier of the media used in a tg://photo?id= , tg://video?id=
            , tg://document?id= , or tg://audio?id= link. 1-64 characters, only A-Z , a-z , 0-9 ,
            _ and - are allowed.
        media (:class:`telegram.InputMedia`): The media to be sent. Everything except the media
            itself and its properties is ignored.

    Attributes:
        id (:obj:`str`): Unique identifier of the media used in a tg://photo?id= , tg://video?id=
            , tg://document?id= , or tg://audio?id= link. 1-64 characters, only A-Z , a-z , 0-9 ,
            _ and - are allowed.
        media (:class:`telegram.InputMedia`): The media to be sent. Everything except the media
            itself and its properties is ignored.
    """

    __slots__ = ("id", "media")

    def __init__(
        self,
        id: "str",
        media: (
            "InputMediaAnimation | InputMediaAudio | InputMediaDocument | "
            "InputMediaPhoto | InputMediaVideo | InputMediaVoiceNote"
        ),
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.id = id
            self.media = media
        self._id_attrs = (
            self.id,
            self.media,
        )
        self._freeze()


class RichMessageButton(_RichObject):
    """This object represents a button in a RichMessage . Exactly one of the fields other than text
    and style must be used to specify the type of the button.

    Args:
        text (:data:`telegram.RichTextValue`): Text of the button. May contain only plain text,
            RichTextCustomEmoji and RichTextDateTime entities.
        style (:obj:`str`, optional): Style of the button. Must be one of “danger”, “success”,
            “primary”, or “link” (the button is shown as a regular link without borders). Apps may
            use theme-specific colors for the button background and text based on the style. The
            style “link” is allowed only for callback buttons.
        url (:obj:`str`, optional): HTTP or tg:// URL to be opened when the button is pressed.
            Links tg://user?id=<user_id> can be used to mention a user by their identifier without
            using a username, if this is allowed by their privacy settings.
        callback_data (:obj:`str`, optional): Data to be sent in a callback query to the bot when
            the button is pressed, 1-64 bytes
        web_app (:class:`telegram.WebAppInfo`, optional): Description of the Web App that will be
            launched when the user presses the button. The Web App will be able to send an
            arbitrary message on behalf of the user using the method answerWebAppQuery . Available
            only in private chats between a user and the bot. Not supported for messages sent on
            behalf of a business account.
        login_url (:class:`telegram.LoginUrl`, optional): An HTTPS URL used to automatically
            authorize the user. Can be used as a replacement for the Telegram Login Widget . Not
            supported for ephemeral messages.
        switch_inline_query (:obj:`str`, optional): If set, pressing the button will prompt the
            user to select one of their chats, open that chat and insert the bot's username and
            the specified inline query in the input field. May be empty, in which case just the
            bot's username will be inserted. Not supported for messages sent in channel direct
            messages chats and on behalf of a business account.
        switch_inline_query_current_chat (:obj:`str`, optional): If set, pressing the button will
            insert the bot's username and the specified inline query in the current chat's input
            field. May be empty, in which case only the bot's username will be inserted. Not
            supported in channels and for messages sent in channel direct messages chats and on
            behalf of a business account.
        switch_inline_query_chosen_chat (:class:`telegram.SwitchInlineQueryChosenChat`, optional):
            If set, pressing the button will prompt the user to select one of their chats of the
            specified type, open that chat and insert the bot's username and the specified inline
            query in the input field. Not supported for messages sent in channel direct messages
            chats and on behalf of a business account.
        copy_text (:class:`telegram.CopyTextButton`, optional): A button that copies the specified
            text to the clipboard
        disabled (:class:`telegram.DisabledButton`, optional): If set, then the button is disabled
            and does nothing

    Attributes:
        text (:data:`telegram.RichTextValue`): Text of the button. May contain only plain text,
            RichTextCustomEmoji and RichTextDateTime entities.
        style (:obj:`str`): Optional. Style of the button. Must be one of “danger”, “success”,
            “primary”, or “link” (the button is shown as a regular link without borders). Apps may
            use theme-specific colors for the button background and text based on the style. The
            style “link” is allowed only for callback buttons.
        url (:obj:`str`): Optional. HTTP or tg:// URL to be opened when the button is pressed.
            Links tg://user?id=<user_id> can be used to mention a user by their identifier without
            using a username, if this is allowed by their privacy settings.
        callback_data (:obj:`str`): Optional. Data to be sent in a callback query to the bot when
            the button is pressed, 1-64 bytes
        web_app (:class:`telegram.WebAppInfo`): Optional. Description of the Web App that will be
            launched when the user presses the button. The Web App will be able to send an
            arbitrary message on behalf of the user using the method answerWebAppQuery . Available
            only in private chats between a user and the bot. Not supported for messages sent on
            behalf of a business account.
        login_url (:class:`telegram.LoginUrl`): Optional. An HTTPS URL used to automatically
            authorize the user. Can be used as a replacement for the Telegram Login Widget . Not
            supported for ephemeral messages.
        switch_inline_query (:obj:`str`): Optional. If set, pressing the button will prompt the
            user to select one of their chats, open that chat and insert the bot's username and
            the specified inline query in the input field. May be empty, in which case just the
            bot's username will be inserted. Not supported for messages sent in channel direct
            messages chats and on behalf of a business account.
        switch_inline_query_current_chat (:obj:`str`): Optional. If set, pressing the button will
            insert the bot's username and the specified inline query in the current chat's input
            field. May be empty, in which case only the bot's username will be inserted. Not
            supported in channels and for messages sent in channel direct messages chats and on
            behalf of a business account.
        switch_inline_query_chosen_chat (:class:`telegram.SwitchInlineQueryChosenChat`): Optional.
            If set, pressing the button will prompt the user to select one of their chats of the
            specified type, open that chat and insert the bot's username and the specified inline
            query in the input field. Not supported for messages sent in channel direct messages
            chats and on behalf of a business account.
        copy_text (:class:`telegram.CopyTextButton`): Optional. A button that copies the specified
            text to the clipboard
        disabled (:class:`telegram.DisabledButton`): Optional. If set, then the button is disabled
            and does nothing
    """

    __slots__ = (
        "callback_data",
        "copy_text",
        "disabled",
        "login_url",
        "style",
        "switch_inline_query",
        "switch_inline_query_chosen_chat",
        "switch_inline_query_current_chat",
        "text",
        "url",
        "web_app",
    )

    def __init__(
        self,
        text: "RichTextValue",
        style: "str | None" = None,
        url: "str | None" = None,
        callback_data: "str | None" = None,
        web_app: "WebAppInfo | None" = None,
        login_url: "LoginUrl | None" = None,
        switch_inline_query: "str | None" = None,
        switch_inline_query_current_chat: "str | None" = None,
        switch_inline_query_chosen_chat: "SwitchInlineQueryChosenChat | None" = None,
        copy_text: "CopyTextButton | None" = None,
        disabled: "DisabledButton | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.style = style
            self.url = url
            self.callback_data = callback_data
            self.web_app = web_app
            self.login_url = login_url
            self.switch_inline_query = switch_inline_query
            self.switch_inline_query_current_chat = switch_inline_query_current_chat
            self.switch_inline_query_chosen_chat = switch_inline_query_chosen_chat
            self.copy_text = copy_text
            self.disabled = disabled
        self._id_attrs = (
            self.text,
            self.style,
            self.url,
            self.callback_data,
            self.web_app,
            self.login_url,
            self.switch_inline_query,
            self.switch_inline_query_current_chat,
            self.switch_inline_query_chosen_chat,
            self.copy_text,
            self.disabled,
        )
        self._freeze()


class RichTextBold(RichText):
    """A bold text.

    Args:
        text (:data:`telegram.RichTextValue`): The text

    Attributes:
        type (:obj:`str`): Type of the rich text, always “bold”
        text (:data:`telegram.RichTextValue`): The text
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="bold", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichTextItalic(RichText):
    """An italicized text.

    Args:
        text (:data:`telegram.RichTextValue`): The text

    Attributes:
        type (:obj:`str`): Type of the rich text, always “italic”
        text (:data:`telegram.RichTextValue`): The text
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="italic", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichTextUnderline(RichText):
    """An underlined text.

    Args:
        text (:data:`telegram.RichTextValue`): The text

    Attributes:
        type (:obj:`str`): Type of the rich text, always “underline”
        text (:data:`telegram.RichTextValue`): The text
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="underline", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichTextStrikethrough(RichText):
    """A strikethrough text.

    Args:
        text (:data:`telegram.RichTextValue`): The text

    Attributes:
        type (:obj:`str`): Type of the rich text, always “strikethrough”
        text (:data:`telegram.RichTextValue`): The text
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="strikethrough", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichTextSpoiler(RichText):
    """A text covered by a spoiler.

    Args:
        text (:data:`telegram.RichTextValue`): The text

    Attributes:
        type (:obj:`str`): Type of the rich text, always “spoiler”
        text (:data:`telegram.RichTextValue`): The text
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="spoiler", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichTextDateTime(RichText):
    """Formatted date and time.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        unix_time (:class:`datetime.datetime`): The Unix time associated with the entity
        date_time_format (:obj:`str`): The string that defines the formatting of the date and
            time. See date-time entity formatting for more details.

    Attributes:
        type (:obj:`str`): Type of the rich text, always “date_time”
        text (:data:`telegram.RichTextValue`): The text
        unix_time (:class:`datetime.datetime`): The Unix time associated with the entity
        date_time_format (:obj:`str`): The string that defines the formatting of the date and
            time. See date-time entity formatting for more details.
    """

    __slots__ = ("date_time_format", "text", "unix_time")

    def __init__(
        self,
        text: "RichTextValue",
        unix_time: dtm.datetime,
        date_time_format: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="date_time", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.unix_time = unix_time
            self.date_time_format = date_time_format
        self._id_attrs = (
            self.type,
            self.text,
            self.unix_time,
            self.date_time_format,
        )
        self._freeze()


class RichTextTextMention(RichText):
    """A mention of a Telegram user by their identifier.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        user (:class:`telegram.User`): The mentioned user

    Attributes:
        type (:obj:`str`): Type of the rich text, always “text_mention”
        text (:data:`telegram.RichTextValue`): The text
        user (:class:`telegram.User`): The mentioned user
    """

    __slots__ = ("text", "user")

    def __init__(
        self,
        text: "RichTextValue",
        user: "User",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="text_mention", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.user = user
        self._id_attrs = (
            self.type,
            self.text,
            self.user,
        )
        self._freeze()


class RichTextSubscript(RichText):
    """A subscript text.

    Args:
        text (:data:`telegram.RichTextValue`): The text

    Attributes:
        type (:obj:`str`): Type of the rich text, always “subscript”
        text (:data:`telegram.RichTextValue`): The text
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="subscript", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichTextSuperscript(RichText):
    """A superscript text.

    Args:
        text (:data:`telegram.RichTextValue`): The text

    Attributes:
        type (:obj:`str`): Type of the rich text, always “superscript”
        text (:data:`telegram.RichTextValue`): The text
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="superscript", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichTextMarked(RichText):
    """A marked text.

    Args:
        text (:data:`telegram.RichTextValue`): The text

    Attributes:
        type (:obj:`str`): Type of the rich text, always “marked”
        text (:data:`telegram.RichTextValue`): The text
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="marked", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichTextCode(RichText):
    """A monowidth text.

    Args:
        text (:data:`telegram.RichTextValue`): The text

    Attributes:
        type (:obj:`str`): Type of the rich text, always “code”
        text (:data:`telegram.RichTextValue`): The text
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="code", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichTextCustomEmoji(RichText):
    """A custom emoji.

    Args:
        custom_emoji_id (:obj:`str`): Unique identifier of the custom emoji. Use
            getCustomEmojiStickers to get full information about the sticker.
        alternative_text (:obj:`str`): Alternative emoji for the custom emoji

    Attributes:
        type (:obj:`str`): Type of the rich text, always “custom_emoji”
        custom_emoji_id (:obj:`str`): Unique identifier of the custom emoji. Use
            getCustomEmojiStickers to get full information about the sticker.
        alternative_text (:obj:`str`): Alternative emoji for the custom emoji
    """

    __slots__ = ("alternative_text", "custom_emoji_id")

    def __init__(
        self,
        custom_emoji_id: "str",
        alternative_text: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="custom_emoji", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.custom_emoji_id = custom_emoji_id
            self.alternative_text = alternative_text
        self._id_attrs = (
            self.type,
            self.custom_emoji_id,
            self.alternative_text,
        )
        self._freeze()


class RichTextMathematicalExpression(RichText):
    """A mathematical expression.

    Args:
        expression (:obj:`str`): The expression in LaTeX format

    Attributes:
        type (:obj:`str`): Type of the rich text, always “mathematical_expression”
        expression (:obj:`str`): The expression in LaTeX format
    """

    __slots__ = ("expression",)

    def __init__(
        self,
        expression: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="mathematical_expression", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.expression = expression
        self._id_attrs = (
            self.type,
            self.expression,
        )
        self._freeze()


class RichTextUrl(RichText):
    """A text with a link.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        url (:obj:`str`): URL of the link

    Attributes:
        type (:obj:`str`): Type of the rich text, always “url”
        text (:data:`telegram.RichTextValue`): The text
        url (:obj:`str`): URL of the link
    """

    __slots__ = ("text", "url")

    def __init__(
        self,
        text: "RichTextValue",
        url: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="url", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.url = url
        self._id_attrs = (
            self.type,
            self.text,
            self.url,
        )
        self._freeze()


class RichTextEmailAddress(RichText):
    """A text with an email address.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        email_address (:obj:`str`): The email address

    Attributes:
        type (:obj:`str`): Type of the rich text, always “email_address”
        text (:data:`telegram.RichTextValue`): The text
        email_address (:obj:`str`): The email address
    """

    __slots__ = ("email_address", "text")

    def __init__(
        self,
        text: "RichTextValue",
        email_address: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="email_address", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.email_address = email_address
        self._id_attrs = (
            self.type,
            self.text,
            self.email_address,
        )
        self._freeze()


class RichTextPhoneNumber(RichText):
    """A text with a phone number.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        phone_number (:obj:`str`): The phone number

    Attributes:
        type (:obj:`str`): Type of the rich text, always “phone_number”
        text (:data:`telegram.RichTextValue`): The text
        phone_number (:obj:`str`): The phone number
    """

    __slots__ = ("phone_number", "text")

    def __init__(
        self,
        text: "RichTextValue",
        phone_number: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="phone_number", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.phone_number = phone_number
        self._id_attrs = (
            self.type,
            self.text,
            self.phone_number,
        )
        self._freeze()


class RichTextBankCardNumber(RichText):
    """A text with a bank card number.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        bank_card_number (:obj:`str`): The bank card number

    Attributes:
        type (:obj:`str`): Type of the rich text, always “bank_card_number”
        text (:data:`telegram.RichTextValue`): The text
        bank_card_number (:obj:`str`): The bank card number
    """

    __slots__ = ("bank_card_number", "text")

    def __init__(
        self,
        text: "RichTextValue",
        bank_card_number: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="bank_card_number", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.bank_card_number = bank_card_number
        self._id_attrs = (
            self.type,
            self.text,
            self.bank_card_number,
        )
        self._freeze()


class RichTextMention(RichText):
    """A mention by a username.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        username (:obj:`str`): The username

    Attributes:
        type (:obj:`str`): Type of the rich text, always “mention”
        text (:data:`telegram.RichTextValue`): The text
        username (:obj:`str`): The username
    """

    __slots__ = ("text", "username")

    def __init__(
        self,
        text: "RichTextValue",
        username: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="mention", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.username = username
        self._id_attrs = (
            self.type,
            self.text,
            self.username,
        )
        self._freeze()


class RichTextHashtag(RichText):
    """A hashtag.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        hashtag (:obj:`str`): The hashtag

    Attributes:
        type (:obj:`str`): Type of the rich text, always “hashtag”
        text (:data:`telegram.RichTextValue`): The text
        hashtag (:obj:`str`): The hashtag
    """

    __slots__ = ("hashtag", "text")

    def __init__(
        self,
        text: "RichTextValue",
        hashtag: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="hashtag", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.hashtag = hashtag
        self._id_attrs = (
            self.type,
            self.text,
            self.hashtag,
        )
        self._freeze()


class RichTextCashtag(RichText):
    """A cashtag.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        cashtag (:obj:`str`): The cashtag

    Attributes:
        type (:obj:`str`): Type of the rich text, always “cashtag”
        text (:data:`telegram.RichTextValue`): The text
        cashtag (:obj:`str`): The cashtag
    """

    __slots__ = ("cashtag", "text")

    def __init__(
        self,
        text: "RichTextValue",
        cashtag: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="cashtag", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.cashtag = cashtag
        self._id_attrs = (
            self.type,
            self.text,
            self.cashtag,
        )
        self._freeze()


class RichTextBotCommand(RichText):
    """A bot command.

    Args:
        text (:data:`telegram.RichTextValue`): The text
        bot_command (:obj:`str`): The bot command

    Attributes:
        type (:obj:`str`): Type of the rich text, always “bot_command”
        text (:data:`telegram.RichTextValue`): The text
        bot_command (:obj:`str`): The bot command
    """

    __slots__ = ("bot_command", "text")

    def __init__(
        self,
        text: "RichTextValue",
        bot_command: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="bot_command", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.bot_command = bot_command
        self._id_attrs = (
            self.type,
            self.text,
            self.bot_command,
        )
        self._freeze()


class RichTextButton(RichText):
    """A button.

    Args:
        button (:class:`telegram.RichMessageButton`): The button

    Attributes:
        type (:obj:`str`): Type of the rich text, always “button”
        button (:class:`telegram.RichMessageButton`): The button
    """

    __slots__ = ("button",)

    def __init__(
        self,
        button: "RichMessageButton",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="button", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.button = button
        self._id_attrs = (
            self.type,
            self.button,
        )
        self._freeze()


class RichTextAnchor(RichText):
    """An anchor.

    Args:
        name (:obj:`str`): The name of the anchor

    Attributes:
        type (:obj:`str`): Type of the rich text, always “anchor”
        name (:obj:`str`): The name of the anchor
    """

    __slots__ = ("name",)

    def __init__(
        self,
        name: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="anchor", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.name = name
        self._id_attrs = (
            self.type,
            self.name,
        )
        self._freeze()


class RichTextAnchorLink(RichText):
    """A link to an anchor.

    Args:
        text (:data:`telegram.RichTextValue`): The link text
        anchor_name (:obj:`str`): The name of the anchor. If the name is empty, then the link
            brings back to the top of the message.

    Attributes:
        type (:obj:`str`): Type of the rich text, always “anchor_link”
        text (:data:`telegram.RichTextValue`): The link text
        anchor_name (:obj:`str`): The name of the anchor. If the name is empty, then the link
            brings back to the top of the message.
    """

    __slots__ = ("anchor_name", "text")

    def __init__(
        self,
        text: "RichTextValue",
        anchor_name: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="anchor_link", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.anchor_name = anchor_name
        self._id_attrs = (
            self.type,
            self.text,
            self.anchor_name,
        )
        self._freeze()


class RichTextReference(RichText):
    """A reference.

    Args:
        text (:data:`telegram.RichTextValue`): Text of the reference
        name (:obj:`str`): The name of the reference

    Attributes:
        type (:obj:`str`): Type of the rich text, always “reference”
        text (:data:`telegram.RichTextValue`): Text of the reference
        name (:obj:`str`): The name of the reference
    """

    __slots__ = ("name", "text")

    def __init__(
        self,
        text: "RichTextValue",
        name: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="reference", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.name = name
        self._id_attrs = (
            self.type,
            self.text,
            self.name,
        )
        self._freeze()


class RichTextReferenceLink(RichText):
    """A link to a reference.

    Args:
        text (:data:`telegram.RichTextValue`): The link text
        reference_name (:obj:`str`): The name of the reference

    Attributes:
        type (:obj:`str`): Type of the rich text, always “reference_link”
        text (:data:`telegram.RichTextValue`): The link text
        reference_name (:obj:`str`): The name of the reference
    """

    __slots__ = ("reference_name", "text")

    def __init__(
        self,
        text: "RichTextValue",
        reference_name: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="reference_link", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.reference_name = reference_name
        self._id_attrs = (
            self.type,
            self.text,
            self.reference_name,
        )
        self._freeze()


class RichBlockCaption(_RichObject):
    """Caption of a rich formatted block.

    Args:
        text (:data:`telegram.RichTextValue`): Block caption
        credit (:data:`telegram.RichTextValue`, optional): Block credit which corresponds to the
            HTML tag <cite>

    Attributes:
        text (:data:`telegram.RichTextValue`): Block caption
        credit (:data:`telegram.RichTextValue`): Optional. Block credit which corresponds to the
            HTML tag <cite>
    """

    __slots__ = ("credit", "text")

    def __init__(
        self,
        text: "RichTextValue",
        credit: "RichTextValue | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.credit = _tuples(credit)
        self._id_attrs = (
            self.text,
            self.credit,
        )
        self._freeze()


class RichBlockTableCell(_RichObject):
    """Cell in a table.

    Args:
        text (:data:`telegram.RichTextValue`, optional): Text in the cell. If omitted, then the
            cell is invisible.
        is_header (:obj:`bool`, optional): True , if the cell is a header cell
        colspan (:obj:`int`, optional): The number of columns the cell spans if it is bigger than
            1
        rowspan (:obj:`int`, optional): The number of rows the cell spans if it is bigger than 1
        align (:obj:`str`): Horizontal cell content alignment. Currently, must be one of “left”,
            “center”, or “right”.
        valign (:obj:`str`): Vertical cell content alignment. Currently, must be one of “top”,
            “middle”, or “bottom”.

    Attributes:
        text (:data:`telegram.RichTextValue`): Optional. Text in the cell. If omitted, then the
            cell is invisible.
        is_header (:obj:`bool`): Optional. True , if the cell is a header cell
        colspan (:obj:`int`): Optional. The number of columns the cell spans if it is bigger than
            1
        rowspan (:obj:`int`): Optional. The number of rows the cell spans if it is bigger than 1
        align (:obj:`str`): Horizontal cell content alignment. Currently, must be one of “left”,
            “center”, or “right”.
        valign (:obj:`str`): Vertical cell content alignment. Currently, must be one of “top”,
            “middle”, or “bottom”.
    """

    __slots__ = ("align", "colspan", "is_header", "rowspan", "text", "valign")

    def __init__(
        self,
        align: "str",
        valign: "str",
        text: "RichTextValue | None" = None,
        is_header: "bool | None" = None,
        colspan: "int | None" = None,
        rowspan: "int | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.align = align
            self.valign = valign
            self.text = _tuples(text)
            self.is_header = is_header
            self.colspan = colspan
            self.rowspan = rowspan
        self._id_attrs = (
            self.align,
            self.valign,
            self.text,
            self.is_header,
            self.colspan,
            self.rowspan,
        )
        self._freeze()


class RichBlockListItem(_RichObject):
    """An item of a list.

    Args:
        label (:obj:`str`): Label of the item
        blocks (Sequence[:class:`telegram.RichBlock`]): The content of the item
        has_checkbox (:obj:`bool`, optional): True , if the item has a checkbox
        is_checked (:obj:`bool`, optional): True , if the item has a checked checkbox
        value (:obj:`int`, optional): For ordered lists, the numeric value of the item label
        type (:obj:`str`, optional): For ordered lists, the type of the item label; must be one of
            “a” for lowercase letters, “A” for uppercase letters, “i” for lowercase Roman
            numerals, “I” for uppercase Roman numerals, or “1” for decimal numbers

    Attributes:
        label (:obj:`str`): Label of the item
        blocks (tuple[:class:`telegram.RichBlock`]): The content of the item
        has_checkbox (:obj:`bool`): Optional. True , if the item has a checkbox
        is_checked (:obj:`bool`): Optional. True , if the item has a checked checkbox
        value (:obj:`int`): Optional. For ordered lists, the numeric value of the item label
        type (:obj:`str`): Optional. For ordered lists, the type of the item label; must be one of
            “a” for lowercase letters, “A” for uppercase letters, “i” for lowercase Roman
            numerals, “I” for uppercase Roman numerals, or “1” for decimal numbers
    """

    __slots__ = ("blocks", "has_checkbox", "is_checked", "label", "type", "value")

    def __init__(
        self,
        label: str,
        blocks: "Sequence[RichBlock]",
        has_checkbox: bool | None = None,
        is_checked: bool | None = None,
        value: int | None = None,
        type: str | None = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        self.label = label
        self.blocks = tuple(blocks)
        self.has_checkbox = has_checkbox
        self.is_checked = is_checked
        self.value = value
        self.type = type
        self._id_attrs = (
            self.label,
            self.blocks,
            self.has_checkbox,
            self.is_checked,
            self.value,
            self.type,
        )
        self._freeze()


class RichBlockParagraph(RichBlock):
    """A text paragraph, corresponding to the HTML tag <p> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “paragraph”
        text (:data:`telegram.RichTextValue`): Text of the block
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="paragraph", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichBlockSectionHeading(RichBlock):
    """A section heading, corresponding to the HTML tags <h1> , <h2> , <h3> , <h4> , <h5> , or
    <h6> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block
        size (:obj:`int`): Relative size of the text font; 1-6, 1 is the largest, 6 is the
            smallest

    Attributes:
        type (:obj:`str`): Type of the block, always “heading”
        text (:data:`telegram.RichTextValue`): Text of the block
        size (:obj:`int`): Relative size of the text font; 1-6, 1 is the largest, 6 is the
            smallest
    """

    __slots__ = ("size", "text")

    def __init__(
        self,
        text: "RichTextValue",
        size: "int",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="heading", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.size = size
        self._id_attrs = (
            self.type,
            self.text,
            self.size,
        )
        self._freeze()


class RichBlockPreformatted(RichBlock):
    """A preformatted text block, corresponding to the nested HTML tags <pre> and <code> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block
        language (:obj:`str`, optional): The programming language of the text

    Attributes:
        type (:obj:`str`): Type of the block, always “pre”
        text (:data:`telegram.RichTextValue`): Text of the block
        language (:obj:`str`): Optional. The programming language of the text
    """

    __slots__ = ("language", "text")

    def __init__(
        self,
        text: "RichTextValue",
        language: "str | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="pre", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.language = language
        self._id_attrs = (
            self.type,
            self.text,
            self.language,
        )
        self._freeze()


class RichBlockFooter(RichBlock):
    """A footer, corresponding to the HTML tag <footer> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “footer”
        text (:data:`telegram.RichTextValue`): Text of the block
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="footer", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class RichBlockDivider(RichBlock):
    """A divider, corresponding to the HTML tag <hr/> .

    Attributes:
        type (:obj:`str`): Type of the block, always “divider”
    """

    __slots__ = ()

    def __init__(
        self,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="divider", api_kwargs=api_kwargs)
        self._id_attrs = (self.type,)
        self._freeze()


class RichBlockMathematicalExpression(RichBlock):
    """A block with a mathematical expression in LaTeX format, corresponding to the custom HTML tag
    <tg-math-block> .

    Args:
        expression (:obj:`str`): The mathematical expression in LaTeX format

    Attributes:
        type (:obj:`str`): Type of the block, always “mathematical_expression”
        expression (:obj:`str`): The mathematical expression in LaTeX format
    """

    __slots__ = ("expression",)

    def __init__(
        self,
        expression: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="mathematical_expression", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.expression = expression
        self._id_attrs = (
            self.type,
            self.expression,
        )
        self._freeze()


class RichBlockAnchor(RichBlock):
    """A block with an anchor, corresponding to the HTML tag <a> with the attribute name .

    Args:
        name (:obj:`str`): The name of the anchor

    Attributes:
        type (:obj:`str`): Type of the block, always “anchor”
        name (:obj:`str`): The name of the anchor
    """

    __slots__ = ("name",)

    def __init__(
        self,
        name: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="anchor", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.name = name
        self._id_attrs = (
            self.type,
            self.name,
        )
        self._freeze()


class RichBlockList(RichBlock):
    """A list of blocks, corresponding to the HTML tag <ul> or <ol> with multiple nested tags <li>
    .

    Args:
        items (Sequence[:class:`telegram.RichBlockListItem`]): Items of the list

    Attributes:
        type (:obj:`str`): Type of the block, always “list”
        items (tuple[:class:`telegram.RichBlockListItem`]): Items of the list
    """

    __slots__ = ("items",)

    def __init__(
        self,
        items: "Sequence[RichBlockListItem]",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="list", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.items = _tuples(items) if items is not None else ()
        self._id_attrs = (
            self.type,
            self.items,
        )
        self._freeze()


class RichBlockBlockQuotation(RichBlock):
    """A block quotation, corresponding to the HTML tag <blockquote> .

    Args:
        blocks (Sequence[:class:`telegram.RichBlock`]): Content of the block
        credit (:data:`telegram.RichTextValue`, optional): Credit of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “blockquote”
        blocks (tuple[:class:`telegram.RichBlock`]): Content of the block
        credit (:data:`telegram.RichTextValue`): Optional. Credit of the block
    """

    __slots__ = ("blocks", "credit")

    def __init__(
        self,
        blocks: "Sequence[RichBlock]",
        credit: "RichTextValue | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="blockquote", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.credit = _tuples(credit)
        self._id_attrs = (
            self.type,
            self.blocks,
            self.credit,
        )
        self._freeze()


class RichBlockExpandableBlockQuotation(RichBlock):
    """A block quotation, corresponding to the HTML tag <blockquote> with custom attribute
    "expandable" .

    Args:
        text (:data:`telegram.RichTextValue`): Content of the block
        credit (:data:`telegram.RichTextValue`, optional): Credit of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “expandable_blockquote”
        text (:data:`telegram.RichTextValue`): Content of the block
        credit (:data:`telegram.RichTextValue`): Optional. Credit of the block
    """

    __slots__ = ("credit", "text")

    def __init__(
        self,
        text: "RichTextValue",
        credit: "RichTextValue | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="expandable_blockquote", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.credit = _tuples(credit)
        self._id_attrs = (
            self.type,
            self.text,
            self.credit,
        )
        self._freeze()


class RichBlockPullQuotation(RichBlock):
    """A quotation with centered text, loosely corresponding to the HTML tag <aside> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block
        credit (:data:`telegram.RichTextValue`, optional): Credit of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “pullquote”
        text (:data:`telegram.RichTextValue`): Text of the block
        credit (:data:`telegram.RichTextValue`): Optional. Credit of the block
    """

    __slots__ = ("credit", "text")

    def __init__(
        self,
        text: "RichTextValue",
        credit: "RichTextValue | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="pullquote", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.credit = _tuples(credit)
        self._id_attrs = (
            self.type,
            self.text,
            self.credit,
        )
        self._freeze()


class RichBlockCollage(RichBlock):
    """A collage, corresponding to the custom HTML tag <tg-collage> .

    Args:
        blocks (Sequence[:class:`telegram.RichBlock`]): Elements of the collage
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “collage”
        blocks (tuple[:class:`telegram.RichBlock`]): Elements of the collage
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("blocks", "caption")

    def __init__(
        self,
        blocks: "Sequence[RichBlock]",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="collage", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.blocks,
            self.caption,
        )
        self._freeze()


class RichBlockSlideshow(RichBlock):
    """A slideshow, corresponding to the custom HTML tag <tg-slideshow> .

    Args:
        blocks (Sequence[:class:`telegram.RichBlock`]): Elements of the slideshow
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “slideshow”
        blocks (tuple[:class:`telegram.RichBlock`]): Elements of the slideshow
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("blocks", "caption")

    def __init__(
        self,
        blocks: "Sequence[RichBlock]",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="slideshow", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.blocks,
            self.caption,
        )
        self._freeze()


class RichBlockTable(RichBlock):
    """A table, corresponding to the HTML tag <table> .

    Args:
        cells (Sequence[Sequence[:class:`telegram.RichBlockTableCell`]]): Cells of the table
        is_bordered (:obj:`bool`, optional): True , if the table has borders
        is_striped (:obj:`bool`, optional): True , if the table is striped
        is_compact (:obj:`bool`, optional): True , if table cells have smaller indents
        caption (:data:`telegram.RichTextValue`, optional): Caption of the table

    Attributes:
        type (:obj:`str`): Type of the block, always “table”
        cells (tuple[tuple[:class:`telegram.RichBlockTableCell`]]): Cells of the table
        is_bordered (:obj:`bool`): Optional. True , if the table has borders
        is_striped (:obj:`bool`): Optional. True , if the table is striped
        is_compact (:obj:`bool`): Optional. True , if table cells have smaller indents
        caption (:data:`telegram.RichTextValue`): Optional. Caption of the table
    """

    __slots__ = ("caption", "cells", "is_bordered", "is_compact", "is_striped")

    def __init__(
        self,
        cells: "Sequence[Sequence[RichBlockTableCell]]",
        is_bordered: "bool | None" = None,
        is_striped: "bool | None" = None,
        is_compact: "bool | None" = None,
        caption: "RichTextValue | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="table", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.cells = _tuples(cells) if cells is not None else ()
            self.is_bordered = is_bordered
            self.is_striped = is_striped
            self.is_compact = is_compact
            self.caption = _tuples(caption)
        self._id_attrs = (
            self.type,
            self.cells,
            self.is_bordered,
            self.is_striped,
            self.is_compact,
            self.caption,
        )
        self._freeze()


class RichBlockDetails(RichBlock):
    """An expandable block for details disclosure, corresponding to the HTML tag <details> .

    Args:
        summary (:data:`telegram.RichTextValue`): Always shown summary of the block
        blocks (Sequence[:class:`telegram.RichBlock`]): Content of the block
        is_open (:obj:`bool`, optional): True , if the content of the block is visible by default

    Attributes:
        type (:obj:`str`): Type of the block, always “details”
        summary (:data:`telegram.RichTextValue`): Always shown summary of the block
        blocks (tuple[:class:`telegram.RichBlock`]): Content of the block
        is_open (:obj:`bool`): Optional. True , if the content of the block is visible by default
    """

    __slots__ = ("blocks", "is_open", "summary")

    def __init__(
        self,
        summary: "RichTextValue",
        blocks: "Sequence[RichBlock]",
        is_open: "bool | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="details", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.summary = _tuples(summary)
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.is_open = is_open
        self._id_attrs = (
            self.type,
            self.summary,
            self.blocks,
            self.is_open,
        )
        self._freeze()


class RichBlockMap(RichBlock):
    """A block with a map, corresponding to the custom HTML tag <tg-map> .

    Args:
        location (:class:`telegram.Location`): Location of the center of the map
        zoom (:obj:`int`): Map zoom level
        width (:obj:`int`): Expected width of the map
        height (:obj:`int`): Expected height of the map
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “map”
        location (:class:`telegram.Location`): Location of the center of the map
        zoom (:obj:`int`): Map zoom level
        width (:obj:`int`): Expected width of the map
        height (:obj:`int`): Expected height of the map
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "height", "location", "width", "zoom")

    def __init__(
        self,
        location: "Location",
        zoom: "int",
        width: "int",
        height: "int",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="map", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.location = location
            self.zoom = zoom
            self.width = width
            self.height = height
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.location,
            self.zoom,
            self.width,
            self.height,
            self.caption,
        )
        self._freeze()


class RichBlockButtons(RichBlock):
    """A block containing a list of buttons that are shown in one row, corresponding to the custom
    HTML tag <tg-button-row> .

    Args:
        buttons (Sequence[:class:`telegram.RichMessageButton`]): The buttons
        align (:obj:`str`, optional): Horizontal alignment of the buttons. Currently, must be one
            of “left”, “center”, or “right”.

    Attributes:
        type (:obj:`str`): Type of the block, always “buttons”
        buttons (tuple[:class:`telegram.RichMessageButton`]): The buttons
        align (:obj:`str`): Optional. Horizontal alignment of the buttons. Currently, must be one
            of “left”, “center”, or “right”.
    """

    __slots__ = ("align", "buttons")

    def __init__(
        self,
        buttons: "Sequence[RichMessageButton]",
        align: "str | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="buttons", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.buttons = _tuples(buttons) if buttons is not None else ()
            self.align = align
        self._id_attrs = (
            self.type,
            self.buttons,
            self.align,
        )
        self._freeze()


class RichBlockAnimation(RichBlock):
    """A block with an animation, corresponding to the HTML tag <video> .

    Args:
        animation (:class:`telegram.Animation`): The animation
        has_spoiler (:obj:`bool`, optional): True , if the media preview is covered by a spoiler
            animation
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “animation”
        animation (:class:`telegram.Animation`): The animation
        has_spoiler (:obj:`bool`): Optional. True , if the media preview is covered by a spoiler
            animation
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("animation", "caption", "has_spoiler")

    def __init__(
        self,
        animation: "Animation",
        has_spoiler: "bool | None" = None,
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="animation", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.animation = animation
            self.has_spoiler = has_spoiler
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.animation,
            self.has_spoiler,
            self.caption,
        )
        self._freeze()


class RichBlockAudio(RichBlock):
    """A block with a music file, corresponding to the HTML tag <audio> .

    Args:
        audio (:class:`telegram.Audio`): The audio
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “audio”
        audio (:class:`telegram.Audio`): The audio
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("audio", "caption")

    def __init__(
        self,
        audio: "Audio",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="audio", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.audio = audio
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.audio,
            self.caption,
        )
        self._freeze()


class RichBlockDocument(RichBlock):
    """A block with a general file, corresponding to the custom HTML tag <tg-document> .

    Args:
        document (:class:`telegram.Document`): The document
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “document”
        document (:class:`telegram.Document`): The document
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "document")

    def __init__(
        self,
        document: "Document",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="document", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.document = document
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.document,
            self.caption,
        )
        self._freeze()


class RichBlockPhoto(RichBlock):
    """A block with a photo, corresponding to the HTML tag <img> .

    Args:
        photo (Sequence[:class:`telegram.PhotoSize`]): Available sizes of the photo
        has_spoiler (:obj:`bool`, optional): True , if the media preview is covered by a spoiler
            animation
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “photo”
        photo (tuple[:class:`telegram.PhotoSize`]): Available sizes of the photo
        has_spoiler (:obj:`bool`): Optional. True , if the media preview is covered by a spoiler
            animation
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "has_spoiler", "photo")

    def __init__(
        self,
        photo: "Sequence[PhotoSize]",
        has_spoiler: "bool | None" = None,
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="photo", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.photo = _tuples(photo) if photo is not None else ()
            self.has_spoiler = has_spoiler
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.photo,
            self.has_spoiler,
            self.caption,
        )
        self._freeze()


class RichBlockVideo(RichBlock):
    """A block with a video, corresponding to the HTML tag <video> .

    Args:
        video (:class:`telegram.Video`): The video
        has_spoiler (:obj:`bool`, optional): True , if the media preview is covered by a spoiler
            animation
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “video”
        video (:class:`telegram.Video`): The video
        has_spoiler (:obj:`bool`): Optional. True , if the media preview is covered by a spoiler
            animation
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "has_spoiler", "video")

    def __init__(
        self,
        video: "Video",
        has_spoiler: "bool | None" = None,
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="video", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.video = video
            self.has_spoiler = has_spoiler
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.video,
            self.has_spoiler,
            self.caption,
        )
        self._freeze()


class RichBlockVoiceNote(RichBlock):
    """A block with a voice note, corresponding to the HTML tag <audio> .

    Args:
        voice_note (:class:`telegram.Voice`): The voice note
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “voice_note”
        voice_note (:class:`telegram.Voice`): The voice note
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "voice_note")

    def __init__(
        self,
        voice_note: "Voice",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="voice_note", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.voice_note = voice_note
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.voice_note,
            self.caption,
        )
        self._freeze()


class RichBlockThinking(RichBlock):
    """A block with a “Thinking…” placeholder, corresponding to the custom HTML tag <tg-thinking> .
    The block may be used only in sendRichMessageDraft , therefore it can't be received in
    messages. See https://t.me/addemoji/AIActions for examples of custom emoji that are
    recommended for usage in the block.

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block. See
            https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for
            usage in the block.

    Attributes:
        type (:obj:`str`): Type of the block, always “thinking”
        text (:data:`telegram.RichTextValue`): Text of the block. See
            https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for
            usage in the block.
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="thinking", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class InputRichBlockListItem(_RichObject):
    """An item of a list to be sent.

    Args:
        blocks (Sequence[:class:`telegram.InputRichBlock`]): The content of the item
        has_checkbox (:obj:`bool`, optional): Pass True if the item has a checkbox
        is_checked (:obj:`bool`, optional): Pass True if the item has a checked checkbox
        value (:obj:`int`, optional): For ordered lists, the numeric value of the item label
        type (:obj:`str`, optional): For ordered lists, the type of the item label; must be one of
            “a” for lowercase letters, “A” for uppercase letters, “i” for lowercase Roman
            numerals, “I” for uppercase Roman numerals, or “1” for decimal numbers

    Attributes:
        blocks (tuple[:class:`telegram.InputRichBlock`]): The content of the item
        has_checkbox (:obj:`bool`): Optional. Pass True if the item has a checkbox
        is_checked (:obj:`bool`): Optional. Pass True if the item has a checked checkbox
        value (:obj:`int`): Optional. For ordered lists, the numeric value of the item label
        type (:obj:`str`): Optional. For ordered lists, the type of the item label; must be one of
            “a” for lowercase letters, “A” for uppercase letters, “i” for lowercase Roman
            numerals, “I” for uppercase Roman numerals, or “1” for decimal numbers
    """

    __slots__ = ("blocks", "has_checkbox", "is_checked", "type", "value")

    def __init__(
        self,
        blocks: "Sequence[InputRichBlock]",
        has_checkbox: bool | None = None,
        is_checked: bool | None = None,
        value: int | None = None,
        type: str | None = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        self.blocks = tuple(blocks)
        self.has_checkbox = has_checkbox
        self.is_checked = is_checked
        self.value = value
        self.type = type
        self._id_attrs = (self.blocks, self.has_checkbox, self.is_checked, self.value, self.type)
        self._freeze()


class InputRichBlockParagraph(InputRichBlock):
    """A text paragraph, corresponding to the HTML tag <p> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “paragraph”
        text (:data:`telegram.RichTextValue`): Text of the block
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="paragraph", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class InputRichBlockSectionHeading(InputRichBlock):
    """A section heading, corresponding to the HTML tags <h1> , <h2> , <h3> , <h4> , <h5> , or
    <h6> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block
        size (:obj:`int`): Relative size of the text font; 1-6, 1 is the largest, 6 is the
            smallest

    Attributes:
        type (:obj:`str`): Type of the block, always “heading”
        text (:data:`telegram.RichTextValue`): Text of the block
        size (:obj:`int`): Relative size of the text font; 1-6, 1 is the largest, 6 is the
            smallest
    """

    __slots__ = ("size", "text")

    def __init__(
        self,
        text: "RichTextValue",
        size: "int",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="heading", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.size = size
        self._id_attrs = (
            self.type,
            self.text,
            self.size,
        )
        self._freeze()


class InputRichBlockPreformatted(InputRichBlock):
    """A preformatted text block, corresponding to the nested HTML tags <pre> and <code> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block
        language (:obj:`str`, optional): The programming language of the text

    Attributes:
        type (:obj:`str`): Type of the block, always “pre”
        text (:data:`telegram.RichTextValue`): Text of the block
        language (:obj:`str`): Optional. The programming language of the text
    """

    __slots__ = ("language", "text")

    def __init__(
        self,
        text: "RichTextValue",
        language: "str | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="pre", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.language = language
        self._id_attrs = (
            self.type,
            self.text,
            self.language,
        )
        self._freeze()


class InputRichBlockFooter(InputRichBlock):
    """A footer, corresponding to the HTML tag <footer> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “footer”
        text (:data:`telegram.RichTextValue`): Text of the block
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="footer", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class InputRichBlockDivider(InputRichBlock):
    """A divider, corresponding to the HTML tag <hr/> .

    Attributes:
        type (:obj:`str`): Type of the block, always “divider”
    """

    __slots__ = ()

    def __init__(
        self,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="divider", api_kwargs=api_kwargs)
        self._id_attrs = (self.type,)
        self._freeze()


class InputRichBlockMathematicalExpression(InputRichBlock):
    """A block with a mathematical expression in LaTeX format, corresponding to the custom HTML tag
    <tg-math-block> .

    Args:
        expression (:obj:`str`): The mathematical expression in LaTeX format

    Attributes:
        type (:obj:`str`): Type of the block, always “mathematical_expression”
        expression (:obj:`str`): The mathematical expression in LaTeX format
    """

    __slots__ = ("expression",)

    def __init__(
        self,
        expression: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="mathematical_expression", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.expression = expression
        self._id_attrs = (
            self.type,
            self.expression,
        )
        self._freeze()


class InputRichBlockAnchor(InputRichBlock):
    """A block with an anchor, corresponding to the HTML tag <a> with the attribute name .

    Args:
        name (:obj:`str`): The name of the anchor

    Attributes:
        type (:obj:`str`): Type of the block, always “anchor”
        name (:obj:`str`): The name of the anchor
    """

    __slots__ = ("name",)

    def __init__(
        self,
        name: "str",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="anchor", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.name = name
        self._id_attrs = (
            self.type,
            self.name,
        )
        self._freeze()


class InputRichBlockList(InputRichBlock):
    """A list of blocks, corresponding to the HTML tag <ul> or <ol> with multiple nested tags <li>
    .

    Args:
        items (Sequence[:class:`telegram.InputRichBlockListItem`]): Items of the list

    Attributes:
        type (:obj:`str`): Type of the block, always “list”
        items (tuple[:class:`telegram.InputRichBlockListItem`]): Items of the list
    """

    __slots__ = ("items",)

    def __init__(
        self,
        items: "Sequence[InputRichBlockListItem]",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="list", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.items = _tuples(items) if items is not None else ()
        self._id_attrs = (
            self.type,
            self.items,
        )
        self._freeze()


class InputRichBlockBlockQuotation(InputRichBlock):
    """A block quotation, corresponding to the HTML tag <blockquote> .

    Args:
        blocks (Sequence[:class:`telegram.InputRichBlock`]): Content of the block
        credit (:data:`telegram.RichTextValue`, optional): Credit of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “blockquote”
        blocks (tuple[:class:`telegram.InputRichBlock`]): Content of the block
        credit (:data:`telegram.RichTextValue`): Optional. Credit of the block
    """

    __slots__ = ("blocks", "credit")

    def __init__(
        self,
        blocks: "Sequence[InputRichBlock]",
        credit: "RichTextValue | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="blockquote", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.credit = _tuples(credit)
        self._id_attrs = (
            self.type,
            self.blocks,
            self.credit,
        )
        self._freeze()


class InputRichBlockExpandableBlockQuotation(InputRichBlock):
    """A block quotation, corresponding to the HTML tag <blockquote> with custom attribute
    "expandable" .

    Args:
        text (:data:`telegram.RichTextValue`): Content of the block
        credit (:data:`telegram.RichTextValue`, optional): Credit of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “expandable_blockquote”
        text (:data:`telegram.RichTextValue`): Content of the block
        credit (:data:`telegram.RichTextValue`): Optional. Credit of the block
    """

    __slots__ = ("credit", "text")

    def __init__(
        self,
        text: "RichTextValue",
        credit: "RichTextValue | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="expandable_blockquote", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.credit = _tuples(credit)
        self._id_attrs = (
            self.type,
            self.text,
            self.credit,
        )
        self._freeze()


class InputRichBlockPullQuotation(InputRichBlock):
    """A quotation with centered text, loosely corresponding to the HTML tag <aside> .

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block
        credit (:data:`telegram.RichTextValue`, optional): Credit of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “pullquote”
        text (:data:`telegram.RichTextValue`): Text of the block
        credit (:data:`telegram.RichTextValue`): Optional. Credit of the block
    """

    __slots__ = ("credit", "text")

    def __init__(
        self,
        text: "RichTextValue",
        credit: "RichTextValue | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="pullquote", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
            self.credit = _tuples(credit)
        self._id_attrs = (
            self.type,
            self.text,
            self.credit,
        )
        self._freeze()


class InputRichBlockCollage(InputRichBlock):
    """A collage, corresponding to the custom HTML tag <tg-collage> .

    Args:
        blocks (Sequence[:class:`telegram.InputRichBlock`]): Elements of the collage
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “collage”
        blocks (tuple[:class:`telegram.InputRichBlock`]): Elements of the collage
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("blocks", "caption")

    def __init__(
        self,
        blocks: "Sequence[InputRichBlock]",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="collage", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.blocks,
            self.caption,
        )
        self._freeze()


class InputRichBlockSlideshow(InputRichBlock):
    """A slideshow, corresponding to the custom HTML tag <tg-slideshow> .

    Args:
        blocks (Sequence[:class:`telegram.InputRichBlock`]): Elements of the slideshow
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “slideshow”
        blocks (tuple[:class:`telegram.InputRichBlock`]): Elements of the slideshow
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("blocks", "caption")

    def __init__(
        self,
        blocks: "Sequence[InputRichBlock]",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="slideshow", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.blocks,
            self.caption,
        )
        self._freeze()


class InputRichBlockTable(InputRichBlock):
    """A table, corresponding to the HTML tag <table> .

    Args:
        cells (Sequence[Sequence[:class:`telegram.RichBlockTableCell`]]): Cells of the table
        is_bordered (:obj:`bool`, optional): Pass True if the table has borders
        is_striped (:obj:`bool`, optional): Pass True if the table is striped
        is_compact (:obj:`bool`, optional): Pass True if table cells must have smaller indents
        caption (:data:`telegram.RichTextValue`, optional): Caption of the table

    Attributes:
        type (:obj:`str`): Type of the block, always “table”
        cells (tuple[tuple[:class:`telegram.RichBlockTableCell`]]): Cells of the table
        is_bordered (:obj:`bool`): Optional. Pass True if the table has borders
        is_striped (:obj:`bool`): Optional. Pass True if the table is striped
        is_compact (:obj:`bool`): Optional. Pass True if table cells must have smaller indents
        caption (:data:`telegram.RichTextValue`): Optional. Caption of the table
    """

    __slots__ = ("caption", "cells", "is_bordered", "is_compact", "is_striped")

    def __init__(
        self,
        cells: "Sequence[Sequence[RichBlockTableCell]]",
        is_bordered: "bool | None" = None,
        is_striped: "bool | None" = None,
        is_compact: "bool | None" = None,
        caption: "RichTextValue | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="table", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.cells = _tuples(cells) if cells is not None else ()
            self.is_bordered = is_bordered
            self.is_striped = is_striped
            self.is_compact = is_compact
            self.caption = _tuples(caption)
        self._id_attrs = (
            self.type,
            self.cells,
            self.is_bordered,
            self.is_striped,
            self.is_compact,
            self.caption,
        )
        self._freeze()


class InputRichBlockDetails(InputRichBlock):
    """An expandable block for details disclosure, corresponding to the HTML tag <details> .

    Args:
        summary (:data:`telegram.RichTextValue`): Always shown summary of the block
        blocks (Sequence[:class:`telegram.InputRichBlock`]): Content of the block
        is_open (:obj:`bool`, optional): Pass True if the content of the block is visible by
            default

    Attributes:
        type (:obj:`str`): Type of the block, always “details”
        summary (:data:`telegram.RichTextValue`): Always shown summary of the block
        blocks (tuple[:class:`telegram.InputRichBlock`]): Content of the block
        is_open (:obj:`bool`): Optional. Pass True if the content of the block is visible by
            default
    """

    __slots__ = ("blocks", "is_open", "summary")

    def __init__(
        self,
        summary: "RichTextValue",
        blocks: "Sequence[InputRichBlock]",
        is_open: "bool | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="details", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.summary = _tuples(summary)
            self.blocks = _tuples(blocks) if blocks is not None else ()
            self.is_open = is_open
        self._id_attrs = (
            self.type,
            self.summary,
            self.blocks,
            self.is_open,
        )
        self._freeze()


class InputRichBlockMap(InputRichBlock):
    """A block with a map, corresponding to the custom HTML tag <tg-map> . The map's width and
    height
    must not exceed 10000 in total. The width and height ratio must be at most 20.

    Args:
        location (:class:`telegram.Location`): Location of the center of the map
        zoom (:obj:`int`, optional): Map zoom level; 0-24
        width (:obj:`int`, optional): Map width; 0-10000
        height (:obj:`int`, optional): Map height; 0-10000
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “map”
        location (:class:`telegram.Location`): Location of the center of the map
        zoom (:obj:`int`): Optional. Map zoom level; 0-24
        width (:obj:`int`): Optional. Map width; 0-10000
        height (:obj:`int`): Optional. Map height; 0-10000
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "height", "location", "width", "zoom")

    def __init__(
        self,
        location: "Location",
        zoom: "int | None" = None,
        width: "int | None" = None,
        height: "int | None" = None,
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="map", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.location = location
            self.zoom = zoom
            self.width = width
            self.height = height
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.location,
            self.zoom,
            self.width,
            self.height,
            self.caption,
        )
        self._freeze()


class InputRichBlockButtons(InputRichBlock):
    """A block containing a list of buttons that are shown in one row, corresponding to the custom
    HTML tag <tg-button-row> .

    Args:
        buttons (Sequence[:class:`telegram.RichMessageButton`]): List of 1-8 buttons to send
        align (:obj:`str`, optional): Horizontal alignment of the buttons. Currently, must be one
            of “left”, “center”, or “right”.

    Attributes:
        type (:obj:`str`): Type of the block, always “buttons”
        buttons (tuple[:class:`telegram.RichMessageButton`]): List of 1-8 buttons to send
        align (:obj:`str`): Optional. Horizontal alignment of the buttons. Currently, must be one
            of “left”, “center”, or “right”.
    """

    __slots__ = ("align", "buttons")

    def __init__(
        self,
        buttons: "Sequence[RichMessageButton]",
        align: "str | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="buttons", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.buttons = _tuples(buttons) if buttons is not None else ()
            self.align = align
        self._id_attrs = (
            self.type,
            self.buttons,
            self.align,
        )
        self._freeze()


class InputRichBlockAnimation(InputRichBlock):
    """A block with an animation, corresponding to the HTML tag <video> .

    Args:
        animation (:class:`telegram.InputMediaAnimation`): The animation. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “animation”
        animation (:class:`telegram.InputMediaAnimation`): The animation. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("animation", "caption")

    def __init__(
        self,
        animation: "InputMediaAnimation",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="animation", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.animation = animation
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.animation,
            self.caption,
        )
        self._freeze()


class InputRichBlockAudio(InputRichBlock):
    """A block with a music file, corresponding to the HTML tag <audio> .

    Args:
        audio (:class:`telegram.InputMediaAudio`): The audio. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “audio”
        audio (:class:`telegram.InputMediaAudio`): The audio. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("audio", "caption")

    def __init__(
        self,
        audio: "InputMediaAudio",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="audio", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.audio = audio
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.audio,
            self.caption,
        )
        self._freeze()


class InputRichBlockDocument(InputRichBlock):
    """A block with a general file, corresponding to the custom HTML tag <tg-document> .

    Args:
        document (:class:`telegram.InputMediaDocument`): The document. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “document”
        document (:class:`telegram.InputMediaDocument`): The document. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "document")

    def __init__(
        self,
        document: "InputMediaDocument",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="document", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.document = document
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.document,
            self.caption,
        )
        self._freeze()


class InputRichBlockPhoto(InputRichBlock):
    """A block with a photo, corresponding to the HTML tag <img> .

    Args:
        photo (:class:`telegram.InputMediaPhoto`): The photo. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “photo”
        photo (:class:`telegram.InputMediaPhoto`): The photo. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "photo")

    def __init__(
        self,
        photo: "InputMediaPhoto",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="photo", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.photo = photo
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.photo,
            self.caption,
        )
        self._freeze()


class InputRichBlockVideo(InputRichBlock):
    """A block with a video, corresponding to the HTML tag <video> .

    Args:
        video (:class:`telegram.InputMediaVideo`): The video. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “video”
        video (:class:`telegram.InputMediaVideo`): The video. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "video")

    def __init__(
        self,
        video: "InputMediaVideo",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="video", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.video = video
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.video,
            self.caption,
        )
        self._freeze()


class InputRichBlockVoiceNote(InputRichBlock):
    """A block with a voice note, corresponding to the HTML tag <audio> .

    Args:
        voice_note (:class:`telegram.InputMediaVoiceNote`): The voice note. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`, optional): Caption of the block

    Attributes:
        type (:obj:`str`): Type of the block, always “voice_note”
        voice_note (:class:`telegram.InputMediaVoiceNote`): The voice note. Caption is ignored.
        caption (:class:`telegram.RichBlockCaption`): Optional. Caption of the block
    """

    __slots__ = ("caption", "voice_note")

    def __init__(
        self,
        voice_note: "InputMediaVoiceNote",
        caption: "RichBlockCaption | None" = None,
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="voice_note", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.voice_note = voice_note
            self.caption = caption
        self._id_attrs = (
            self.type,
            self.voice_note,
            self.caption,
        )
        self._freeze()


class InputRichBlockThinking(InputRichBlock):
    """A block with a “Thinking…” placeholder, corresponding to the custom HTML tag <tg-thinking> .
    The block may be used only in sendRichMessageDraft , therefore it can't be received in
    messages. See https://t.me/addemoji/AIActions for examples of custom emoji that are
    recommended for usage in the block.

    Args:
        text (:data:`telegram.RichTextValue`): Text of the block. See
            https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for
            usage in the block.

    Attributes:
        type (:obj:`str`): Type of the block, always “thinking”
        text (:data:`telegram.RichTextValue`): Text of the block. See
            https://t.me/addemoji/AIActions for examples of custom emoji that are recommended for
            usage in the block.
    """

    __slots__ = ("text",)

    def __init__(
        self,
        text: "RichTextValue",
        *,
        api_kwargs: JSONDict | None = None,
    ) -> None:
        super().__init__(type="thinking", api_kwargs=api_kwargs)
        with self._unfrozen():
            self.text = _tuples(text)
        self._id_attrs = (
            self.type,
            self.text,
        )
        self._freeze()


class InputRichMessageContent(InputMessageContent):
    """Represents the content of a rich message to be sent as the result of an inline query.

    Args:
        rich_message (:class:`telegram.InputRichMessage`): The message to be sent. Only previously
            uploaded files may be used in the message.

    Attributes:
        rich_message (:class:`telegram.InputRichMessage`): The message to be sent. Only previously
            uploaded files may be used in the message.
    """

    __slots__ = ("rich_message",)

    def __init__(
        self, rich_message: InputRichMessage, *, api_kwargs: JSONDict | None = None
    ) -> None:
        super().__init__(api_kwargs=api_kwargs)
        with self._unfrozen():
            self.rich_message = rich_message
        self._id_attrs = (self.rich_message,)
