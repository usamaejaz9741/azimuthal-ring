"""Tests for the handlers.py module.

This module contains unit tests for all Telegram command and message handlers.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from handlers import (
    start, note_cmd, list_notes, task_cmd, list_tasks,
    complete_task_cmd, delete_task_cmd, remind_cmd, search_cmd,
    memory_cmd, list_memories, chat_handler
)


@pytest.mark.asyncio
async def test_start(mock_update, mock_context):
    """Test the /start handler.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    await start(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()
    assert "Local Assistant Help" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_note_cmd_no_args(mock_update, mock_context):
    """Test the /note handler with no arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = []
    await note_cmd(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("Usage: /note <content>")

@pytest.mark.asyncio
async def test_note_cmd_success(mock_update, mock_context):
    """Test the /note handler with valid arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["Hello", "world"]
    with patch('database.add_note') as mock_add_note:
        await note_cmd(mock_update, mock_context)
        mock_add_note.assert_called_with("Hello world")
        mock_update.message.reply_text.assert_called_with("📝 Note saved.")

@pytest.mark.asyncio
async def test_list_notes_empty(mock_update, mock_context):
    """Test the /notes handler when there are no saved notes.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    with patch('database.get_notes', return_value=[]):
        await list_notes(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_with("No notes saved.")

@pytest.mark.asyncio
async def test_list_notes_with_data(mock_update, mock_context):
    """Test the /notes handler when there are saved notes.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    with patch('database.get_notes', return_value=[{'content': 'note 1'}]):
        await list_notes(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        assert "note 1" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_task_cmd_no_args(mock_update, mock_context):
    """Test the /task handler with no arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = []
    await task_cmd(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("Usage: /task <content>")

@pytest.mark.asyncio
async def test_task_cmd_success(mock_update, mock_context):
    """Test the /task handler with valid arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["Task 1"]
    with patch('database.add_task') as mock_add_task:
        await task_cmd(mock_update, mock_context)
        mock_add_task.assert_called_with("Task 1")
        mock_update.message.reply_text.assert_called_with("🗓 Task added.")

@pytest.mark.asyncio
async def test_list_tasks_empty(mock_update, mock_context):
    """Test the /tasks handler when there are no open tasks.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    with patch('database.get_tasks', return_value=[]):
        await list_tasks(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_with("✅ All tasks complete.")

@pytest.mark.asyncio
async def test_list_tasks_with_data(mock_update, mock_context):
    """Test the /tasks handler when there are open tasks.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    with patch('database.get_tasks', return_value=[{'id': 1, 'text': 'task 1', 'created_at': '2023-01-01 10:00:00'}]):
        await list_tasks(mock_update, mock_context)
        assert "task 1" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_complete_task_cmd_no_args(mock_update, mock_context):
    """Test the /done handler with no arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = []
    await complete_task_cmd(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("Usage: /done <task_id>")

@pytest.mark.asyncio
async def test_complete_task_cmd_success(mock_update, mock_context):
    """Test the /done handler with a valid task ID.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["1"]
    with patch('database.complete_task') as mock_complete_task:
        await complete_task_cmd(mock_update, mock_context)
        mock_complete_task.assert_called_with(1)
        mock_update.message.reply_text.assert_called_with("✅ Task marked as done.")

@pytest.mark.asyncio
async def test_complete_task_cmd_invalid(mock_update, mock_context):
    """Test the /done handler with an invalid task ID.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["abc"]
    await complete_task_cmd(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("❌ Invalid ID.")

@pytest.mark.asyncio
async def test_delete_task_cmd_no_args(mock_update, mock_context):
    """Test the /delete handler with no arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = []
    await delete_task_cmd(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("Usage: /delete <task_id>")

@pytest.mark.asyncio
async def test_delete_task_cmd_success(mock_update, mock_context):
    """Test the /delete handler with a valid task ID.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["1"]
    with patch('database.delete_task') as mock_delete_task:
        await delete_task_cmd(mock_update, mock_context)
        mock_delete_task.assert_called_with(1)
        mock_update.message.reply_text.assert_called_with("🗑 Task deleted.")

@pytest.mark.asyncio
async def test_delete_task_cmd_error(mock_update, mock_context):
    """Test the /delete handler when a database error occurs.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["1"]
    with patch('database.delete_task', side_effect=Exception("DB Error")):
        await delete_task_cmd(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_with("❌ Error deleting task.")

@pytest.mark.asyncio
async def test_remind_cmd_no_args(mock_update, mock_context):
    """Test the /remind handler with no arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = []
    await remind_cmd(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("Usage: /remind 10 Remind me about milk")

@pytest.mark.asyncio
async def test_remind_cmd_success(mock_update, mock_context):
    """Test the /remind handler with valid arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["10", "Buy", "milk"]
    with patch('handlers.schedule_reminder') as mock_schedule:
        await remind_cmd(mock_update, mock_context)
        mock_schedule.assert_called_once()
        mock_update.message.reply_text.assert_called_with("⏳ Reminder set status: OK (In 10 minutes)")

@pytest.mark.asyncio
async def test_remind_cmd_invalid_minutes(mock_update, mock_context):
    """Test the /remind handler with an invalid minutes argument.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["abc", "Buy", "milk"]
    await remind_cmd(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("❌ Minutes must be an integer.")

@pytest.mark.asyncio
async def test_search_cmd_no_args(mock_update, mock_context):
    """Test the /search handler with no arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = []
    await search_cmd(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("Usage: /search <query>")

@pytest.mark.asyncio
async def test_search_cmd_success(mock_update, mock_context):
    """Test the /search handler with valid query.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["python"]
    mock_res_text = MagicMock()
    mock_res_text.message_id = 123
    mock_update.message.reply_text = AsyncMock(return_value=mock_res_text)

    with patch('handlers.quick_search', return_value="Search results") as mock_search:
        with patch('handlers.llm_service.summarize', return_value="Summary") as mock_summarize:
            await search_cmd(mock_update, mock_context)
            mock_search.assert_called_with("python")
            mock_summarize.assert_called_with("Search results")
            mock_context.bot.edit_message_text.assert_called_once()
            assert "Summary" in mock_context.bot.edit_message_text.call_args[0][0]

@pytest.mark.asyncio
async def test_memory_cmd_no_args(mock_update, mock_context):
    """Test the /memory handler with insufficient arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["key"]
    await memory_cmd(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_with("Usage: /memory nickname usama")

@pytest.mark.asyncio
async def test_memory_cmd_success(mock_update, mock_context):
    """Test the /memory handler with valid arguments.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_context.args = ["name", "Jules"]
    with patch('database.set_memory') as mock_set_memory:
        await memory_cmd(mock_update, mock_context)
        mock_set_memory.assert_called_with("name", "Jules")
        mock_update.message.reply_text.assert_called_with("🧠 Memory updated: name = Jules")

@pytest.mark.asyncio
async def test_list_memories_empty(mock_update, mock_context):
    """Test the /memories handler when there are no stored memories.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    with patch('database.get_memory', return_value=[]):
        await list_memories(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_with("I memory nothing special.")

@pytest.mark.asyncio
async def test_list_memories_with_data(mock_update, mock_context):
    """Test the /memories handler when there are stored memories.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    with patch('database.get_memory', return_value=[{'key': 'name', 'value': 'Jules'}]):
        await list_memories(mock_update, mock_context)
        assert "name: Jules" in mock_update.message.reply_text.call_args[0][0]

@pytest.mark.asyncio
async def test_chat_handler(mock_update, mock_context):
    """Test the general chat handler with text input.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_update.message.text = "Hello AI"
    with patch('handlers.llm_service.generate', return_value="AI Response") as mock_gen:
        await chat_handler(mock_update, mock_context)
        mock_gen.assert_called_with("Hello AI")
        mock_update.message.reply_text.assert_called_with("AI Response")

@pytest.mark.asyncio
async def test_chat_handler_no_text(mock_update, mock_context):
    """Test the general chat handler with no text input.

    Args:
        mock_update: Mocked Telegram Update object.
        mock_context: Mocked Telegram Context object.
    """
    mock_update.message.text = None
    await chat_handler(mock_update, mock_context)
    # Should do nothing
