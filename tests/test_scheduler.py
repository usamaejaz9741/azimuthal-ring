"""Tests for the scheduler.py module.

This module contains unit tests for background job scheduling and reminder functions.
"""

import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
import scheduler
from scheduler import init_scheduler, schedule_reminder, start_scheduler, stop_scheduler, trigger_reminder, send_reminder_async
from asyncio import AbstractEventLoop


@pytest.fixture(autouse=True)
def reset_scheduler_state():
    """Fixture to reset the scheduler state and mock the scheduler instance.

    Yields:
        MagicMock: A mocked APScheduler instance.
    """
    scheduler._bot_instance = None
    scheduler._loop = None
    # Mock the actual scheduler instance in the module
    with patch('scheduler.scheduler') as mock_sched:
        mock_sched.running = False
        yield mock_sched

@pytest.mark.asyncio
async def test_send_reminder_async():
    """Test the asynchronous send_reminder_async function."""
    mock_bot = AsyncMock()
    await send_reminder_async(mock_bot, 12345, "Test msg")
    mock_bot.send_message.assert_called_with(chat_id=12345, text="🔔 REMINDER: Test msg")

@pytest.mark.asyncio
async def test_init_scheduler(reset_scheduler_state):
    """Test the init_scheduler function.

    Args:
        reset_scheduler_state: Mocked scheduler fixture.
    """
    mock_bot = MagicMock()
    init_scheduler(mock_bot)
    assert scheduler._bot_instance == mock_bot
    assert scheduler._loop == asyncio.get_running_loop()
    reset_scheduler_state.start.assert_called_once()

@pytest.mark.asyncio
async def test_init_scheduler_no_loop(reset_scheduler_state):
    """Test init_scheduler when no event loop is running."""
    mock_bot = MagicMock()
    with patch('asyncio.get_running_loop', side_effect=RuntimeError("No loop")):
        init_scheduler(mock_bot)
        assert scheduler._loop is None

@pytest.mark.asyncio
async def test_schedule_reminder(reset_scheduler_state):
    """Test the schedule_reminder function.

    Args:
        reset_scheduler_state: Mocked scheduler fixture.
    """
    mock_app = MagicMock()
    mock_app.bot = MagicMock()

    schedule_reminder(mock_app, 12345, "Remind me", 60)

    assert scheduler._bot_instance == mock_app.bot
    assert scheduler._loop == asyncio.get_running_loop()
    reset_scheduler_state.add_job.assert_called_once()
    # It's called as scheduler.add_job(trigger_reminder, 'date', run_date=..., args=[...])
    args, kwargs = reset_scheduler_state.add_job.call_args
    assert args[0] == trigger_reminder
    assert args[1] == 'date'
    assert kwargs['args'] == [12345, "Remind me"]

@pytest.mark.asyncio
async def test_schedule_reminder_no_loop(reset_scheduler_state):
    """Test schedule_reminder when no event loop is running."""
    mock_app = MagicMock()
    mock_app.bot = MagicMock()
    with patch('asyncio.get_running_loop', side_effect=RuntimeError("No loop")):
        schedule_reminder(mock_app, 12345, "Remind me", 60)
        assert scheduler._loop is None

def test_start_stop_scheduler(reset_scheduler_state):
    """Test start_scheduler and stop_scheduler functions.

    Args:
        reset_scheduler_state: Mocked scheduler fixture.
    """
    reset_scheduler_state.running = False
    start_scheduler()
    reset_scheduler_state.start.assert_called_once()

    reset_scheduler_state.running = True
    stop_scheduler()
    reset_scheduler_state.shutdown.assert_called_once()

def test_trigger_reminder_no_bot():
    """Test trigger_reminder when the bot instance is not initialized."""
    with patch('builtins.print') as mock_print:
        trigger_reminder(12345, "msg")
        mock_print.assert_called_with("Error: Bot instance not initialized in scheduler.")

def test_trigger_reminder_success():
    """Test trigger_reminder when it successfully schedules a reminder."""
    mock_bot = MagicMock()
    scheduler._bot_instance = mock_bot
    mock_loop = MagicMock()
    scheduler._loop = mock_loop

    with patch('scheduler.asyncio.run_coroutine_threadsafe') as mock_run_threadsafe:
        trigger_reminder(12345, "msg")
        mock_run_threadsafe.assert_called_once()
        # The first argument is the coroutine (result of send_reminder_async)
        # The second is the loop
        args, kwargs = mock_run_threadsafe.call_args
        assert args[1] == mock_loop

def test_trigger_reminder_no_loop():
    """Test trigger_reminder when the event loop is not initialized."""
    mock_bot = MagicMock()
    scheduler._bot_instance = mock_bot
    scheduler._loop = None
    with patch('builtins.print') as mock_print:
        trigger_reminder(12345, "msg")
        mock_print.assert_called_with("Error: Event loop not initialized in scheduler.")
