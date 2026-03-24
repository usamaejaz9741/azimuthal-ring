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

def init_scheduler(bot_instance):
    global _bot_instance
    _bot_instance = bot_instance
    if not scheduler.running:
        scheduler.start()

async def send_reminder_async(bot, chat_id, message):
    await bot.send_message(chat_id=chat_id, text=f"🔔 REMINDER: {message}")

def trigger_reminder(chat_id, message):
    if _bot_instance is None:
        print("Error: Bot instance not initialized in scheduler.")
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(send_reminder_async(_bot_instance, chat_id, message))
    finally:
        loop.close()

def schedule_reminder(bot_app, chat_id, message, delay_seconds):
    # Ensure the bot instance is stored (for when it might not have been via init_scheduler)
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = bot_app.bot

    run_date = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
    
    scheduler.add_job(
        trigger_reminder,
        'date',
        run_date=run_date,
        args=[chat_id, message]
    )

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
