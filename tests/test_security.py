"""Tests for the security features of the Local AI Telegram Assistant."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import config
from utils import restricted

@pytest.mark.asyncio
async def test_restricted_decorator_allowed(mock_update, mock_context):
    """Test that the restricted decorator allows access when IDs match.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.

    Returns:
        None
    """
    mock_handler = AsyncMock()
    decorated_handler = restricted(mock_handler)

    with patch('config.AUTHORIZED_USER_ID', 12345):
        mock_update.effective_user.id = 12345
        await decorated_handler(mock_update, mock_context)
        mock_handler.assert_called_once_with(mock_update, mock_context)

@pytest.mark.asyncio
async def test_restricted_decorator_denied(mock_update, mock_context):
    """Test that the restricted decorator denies access when IDs don't match.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.

    Returns:
        None
    """
    mock_handler = AsyncMock()
    decorated_handler = restricted(mock_handler)

    with patch('config.AUTHORIZED_USER_ID', 12345):
        mock_update.effective_user.id = 99999
        await decorated_handler(mock_update, mock_context)
        mock_handler.assert_not_called()

@pytest.mark.asyncio
async def test_restricted_decorator_no_restriction(mock_update, mock_context):
    """Test that the restricted decorator allows access when AUTHORIZED_USER_ID is not set.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.

    Returns:
        None
    """
    mock_handler = AsyncMock()
    decorated_handler = restricted(mock_handler)

    with patch('config.AUTHORIZED_USER_ID', None):
        mock_update.effective_user.id = 99999
        await decorated_handler(mock_update, mock_context)
        mock_handler.assert_called_once_with(mock_update, mock_context)
