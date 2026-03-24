from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import datetime
import os
from config import DATABASE_URL

# Path for jobs storage - keeping separate from main DB to avoid multi-thread contention
jobstore_path = DATABASE_URL # Can use same SQLite for APScheduler with JobStore

scheduler = BackgroundScheduler(
    jobstores={'default': SQLAlchemyJobStore(url=DATABASE_URL)}
)

async def send_reminder_async(bot, chat_id, message):
    await bot.send_message(chat_id=chat_id, text=f"🔔 REMINDER: {message}")

def schedule_reminder(bot_app, chat_id, message, delay_seconds):
    run_date = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
    
    # Needs to be a function that the scheduler can call
    # Since APScheduler is synchronous, we wrap the async call
    import asyncio
    def trigger():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_reminder_async(bot_app.bot, chat_id, message))

    scheduler.add_job(
        trigger,
        'date',
        run_date=run_date
    )

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
