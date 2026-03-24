import pytest
import asyncio
import threading
from telegram import Bot
from scheduler import trigger_reminder, send_reminder_async
import scheduler
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_trigger_reminder_loop_fix():
    """Verify that trigger_reminder no longer raises RuntimeError when called from a thread.

    Args:
        None

    Returns:
        None
    """
    # 1. Mock Bot
    bot = AsyncMock(spec=Bot)
    scheduler._bot_instance = bot
    # Set the loop to the current running loop
    scheduler._loop = asyncio.get_running_loop()

    error_captured = []

    def target():
        try:
            # 2. Call trigger_reminder from a different thread
            trigger_reminder(12345, "test")
        except Exception as e:
            error_captured.append(e)

    thread = threading.Thread(target=target)
    thread.start()
    thread.join()

    # 3. Verify no error was raised
    assert len(error_captured) == 0

    # 4. Give some time for the coroutine to be processed in the main loop
    await asyncio.sleep(0.1)

    # 5. Verify the bot's send_message was called
    bot.send_message.assert_called()
