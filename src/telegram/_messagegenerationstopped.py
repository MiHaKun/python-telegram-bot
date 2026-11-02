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
"""An event indicating that a user stopped message generation."""

from telegram._chat import Chat
from telegram._telegramobject import TelegramObject
from telegram._utils.types import JSONDict


class MessageGenerationStopped(TelegramObject):
    """A user stopped a message draft.

    Objects are equal if their chat, draft identifier and thread identifier are equal.
    The event contains no user or message object. Use its chat and draft identifier
    to find the generation task to stop.

    Args:
        chat (:class:`telegram.Chat`): Chat containing the draft.
        draft_id (:obj:`int`): Identifier of the stopped draft.
        message_thread_id (:obj:`int`, optional): Thread containing the draft.

    Attributes:
        chat (:class:`telegram.Chat`): Chat containing the draft.
        draft_id (:obj:`int`): Identifier of the stopped draft.
        message_thread_id (:obj:`int`): Optional. Thread containing the draft.
    """

    __slots__ = ("chat", "draft_id", "message_thread_id")

    def __init__(
        self,
        chat: Chat,
        draft_id: int,
        message_thread_id: int | None = None,
        *,
        api_kwargs: JSONDict | None = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        self.chat: Chat = chat
        self.draft_id: int = draft_id
        self.message_thread_id: int | None = message_thread_id
        self._id_attrs = (self.chat, self.draft_id, self.message_thread_id)
        self._freeze()
