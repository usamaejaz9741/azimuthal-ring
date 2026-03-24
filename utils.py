import datetime

def format_time(ts_string: str):
    try:
        dt = datetime.datetime.fromisoformat(ts_string)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return ts_string

def get_help_text():
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
