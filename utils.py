"""Utility module for the Local AI Telegram Assistant.

This module provides helper functions for formatting data and generating
common text responses like the help message.
"""

import datetime


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

    Returns:
        str: A Markdown-formatted string containing descriptions of available commands.
    """
    return """
🤖 *Local Assistant Help*

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

_Send any message to chat with the AI (if model is loaded)._
"""
