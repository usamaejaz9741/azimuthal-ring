"""Utility module for the Local AI Telegram Assistant.

This module provides helper functions for formatting data and generating
common text responses like the help message.
"""

import datetime
import functools
import logging
import config


def restricted(func):
    """Decorator to restrict access to a specific user ID.

    This decorator checks if the incoming update's effective user ID matches
    the AUTHORIZED_USER_ID defined in the configuration. If they don't match,
    it logs the attempt and returns. If AUTHORIZED_USER_ID is not set,
    it allows all access.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function.
    """
    @functools.wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if config.AUTHORIZED_USER_ID is not None and user_id != config.AUTHORIZED_USER_ID:
            logging.warning(f"Unauthorized access attempt by user {user_id}")
            # Silently ignore unauthorized users for a personal bot to avoid bot spam/discovery
            return
        return await func(update, context, *args, **kwargs)
    return wrapped


def format_time(ts_string: str):
    """Format an ISO timestamp string into a more readable format.

    Args:
        ts_string (str): The ISO format timestamp string.

    Returns:
        str: The formatted date string (YYYY-MM-DD HH:MM) or the original string if parsing fails.
    """
    try:
        dt = datetime.datetime.fromisoformat(ts_string)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return ts_string


def get_help_text():
    """Retrieve the help message text.

    Args:
        None

    Returns:
        str: A Markdown-formatted string containing descriptions of available commands.
    """
    return """
🐱 *Choji AI Help*

*Notes*:
- `/note <text>`: Save a note.
- `/notes`: List last 10 notes.

*Tasks*:
- `/task <text>`: Add a to-do.
- `/tasks`: List all open tasks.
- `/done <id>`: Mark task as done.
- `/delete <id>`: Remove a task.

*Reminders*:
- `/remind <min> <text>`: Set a reminder in X minutes.

*Knowledge*:
- `/search <query>`: Search the web.
- `/memory <key> <val>`: Add a fact about yourself.
- `/memories`: List what I know about you.
- `/forget <key>`: Delete a stored fact.

_Send any message to chat with the AI (if model is loaded)._
"""
