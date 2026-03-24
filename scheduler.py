"""Scheduler module for the Local AI Telegram Assistant.

This module handles background job scheduling using APScheduler, primarily
for managing persistent reminders that are stored in the SQLite database.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import datetime
import os
import asyncio
from config import DATABASE_URL


# Path for jobs storage - keeping separate from main DB to avoid multi-thread contention
jobstore_path = DATABASE_URL # Can use same SQLite for APScheduler with JobStore

scheduler = BackgroundScheduler(
    jobstores={'default': SQLAlchemyJobStore(url=DATABASE_URL)}
)

_bot_instance = None
_loop = None


def init_scheduler(bot_instance):
    """Initialize the background scheduler with a bot instance.

    Args:
        bot_instance: The python-telegram-bot instance used to send messages.

    Returns:
        None
    """
    global _bot_instance, _loop
    _bot_instance = bot_instance
    try:
        _loop = asyncio.get_running_loop()
    except RuntimeError:
        _loop = None

    if not scheduler.running:
        scheduler.start()


async def send_reminder_async(bot, chat_id, message):
    """Asynchronously send a reminder message to a specific chat.

    Args:
        bot: The bot instance to use for sending the message.
        chat_id (int/str): The unique identifier for the target chat.
        message (str): The reminder text to be sent.

    Returns:
        None
    """
    await bot.send_message(chat_id=chat_id, text=f"🔔 REMINDER: {message}")


def trigger_reminder(chat_id, message):
    """Function called by the scheduler when a reminder's time is reached.

    This function uses asyncio.run_coroutine_threadsafe to execute the
    asynchronous send_reminder_async function on the main event loop.

    Args:
        chat_id (int/str): The unique identifier for the target chat.
        message (str): The reminder text to be sent.

    Returns:
        None
    """
    if _bot_instance is None:
        print("Error: Bot instance not initialized in scheduler.")
        return

    if _loop is None:
        print("Error: Event loop not initialized in scheduler.")
        return

    asyncio.run_coroutine_threadsafe(
        send_reminder_async(_bot_instance, chat_id, message),
        _loop
    )


def schedule_reminder(bot_app, chat_id, message, delay_seconds):
    """Schedule a new reminder to be triggered after a delay.

    Args:
        bot_app: The Telegram application instance.
        chat_id (int/str): The unique identifier for the target chat.
        message (str): The reminder text.
        delay_seconds (int): The number of seconds to wait before triggering.

    Returns:
        None
    """
    # Ensure the bot instance and loop are stored (for when it might not have been via init_scheduler)
    global _bot_instance, _loop
    if _bot_instance is None:
        _bot_instance = bot_app.bot
    if _loop is None:
        try:
            _loop = asyncio.get_running_loop()
        except RuntimeError:
            _loop = None

    run_date = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
    
    scheduler.add_job(
        trigger_reminder,
        'date',
        run_date=run_date,
        args=[chat_id, message]
    )


def start_scheduler():
    """Start the background scheduler if it is not already running.

    Returns:
        None
    """
    if not scheduler.running:
        scheduler.start()


def stop_scheduler():
    """Shut down the background scheduler if it is currently running.

    Returns:
        None
    """
    if scheduler.running:
        scheduler.shutdown()
