"""Shared fixtures and configuration for the test suite.

This module provides common pytest fixtures used across different test files,
such as mocked Telegram Update and Context objects.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, User, Chat, Message
from telegram.ext import Application, ContextTypes


@pytest.fixture
def mock_update():
    """Create a mocked Telegram Update object.

    Args:
        None

    Returns:
        MagicMock: A mocked Update object with pre-configured message and chat attributes.
    """
    update = MagicMock(spec=Update)
    update.message = MagicMock(spec=Message)
    update.message.reply_text = AsyncMock()
    update.effective_chat = MagicMock(spec=Chat)
    update.effective_chat.id = 12345
    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = 12345
    update.message.text = "test message"
    update.message.message_id = 1
    return update

@pytest.fixture
def mock_context():
    """Create a mocked Telegram Context object.

    Args:
        None

    Returns:
        MagicMock: A mocked Context object with pre-configured args, application, and bot attributes.
    """
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []
    context.application = MagicMock(spec=Application)
    context.bot = MagicMock()
    context.bot.edit_message_text = AsyncMock()
    context.bot.send_chat_action = AsyncMock()
    return context
