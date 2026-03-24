import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import scheduler
from scheduler import init_scheduler, schedule_reminder, start_scheduler, stop_scheduler, trigger_reminder, send_reminder_async
from asyncio import AbstractEventLoop

@pytest.fixture(autouse=True)
def reset_scheduler_state():
    scheduler._bot_instance = None
    # Mock the actual scheduler instance in the module
    with patch('scheduler.scheduler') as mock_sched:
        mock_sched.running = False
        yield mock_sched

@pytest.mark.asyncio
async def test_send_reminder_async():
    mock_bot = AsyncMock()
    await send_reminder_async(mock_bot, 12345, "Test msg")
    mock_bot.send_message.assert_called_with(chat_id=12345, text="🔔 REMINDER: Test msg")

def test_init_scheduler(reset_scheduler_state):
    mock_bot = MagicMock()
    init_scheduler(mock_bot)
    assert scheduler._bot_instance == mock_bot
    reset_scheduler_state.start.assert_called_once()

def test_schedule_reminder(reset_scheduler_state):
    mock_app = MagicMock()
    mock_app.bot = MagicMock()

    schedule_reminder(mock_app, 12345, "Remind me", 60)

    assert scheduler._bot_instance == mock_app.bot
    reset_scheduler_state.add_job.assert_called_once()
    # It's called as scheduler.add_job(trigger_reminder, 'date', run_date=..., args=[...])
    args, kwargs = reset_scheduler_state.add_job.call_args
    assert args[0] == trigger_reminder
    assert args[1] == 'date'
    assert kwargs['args'] == [12345, "Remind me"]

def test_start_stop_scheduler(reset_scheduler_state):
    reset_scheduler_state.running = False
    start_scheduler()
    reset_scheduler_state.start.assert_called_once()

    reset_scheduler_state.running = True
    stop_scheduler()
    reset_scheduler_state.shutdown.assert_called_once()

def test_trigger_reminder_no_bot():
    with patch('builtins.print') as mock_print:
        trigger_reminder(12345, "msg")
        mock_print.assert_called_with("Error: Bot instance not initialized in scheduler.")

def test_trigger_reminder_success():
    mock_bot = MagicMock()
    scheduler._bot_instance = mock_bot

    # We need to mock asyncio completely to avoid event loop issues in tests
    with patch('scheduler.asyncio.new_event_loop') as mock_new_loop:
        mock_loop = MagicMock(spec=AbstractEventLoop)
        mock_new_loop.return_value = mock_loop

        with patch('scheduler.asyncio.set_event_loop'):
            trigger_reminder(12345, "msg")
            mock_loop.run_until_complete.assert_called_once()
            mock_loop.close.assert_called_once()
