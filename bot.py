"""Main entry point for the Local AI Telegram Assistant.

This module initializes the database, builds the Telegram application,
registers command and message handlers, and starts the background scheduler
and the bot's polling loop.
"""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN
import database
import handlers
import scheduler


def main():
    """Main function to initialize and run the Telegram bot.

    This function performs the following steps:
    1. Initializes the SQLite database.
    2. Builds the Telegram application using the provided token.
    3. Registers all command and message handlers.
    4. Initializes the background scheduler.
    5. Starts the bot in polling mode.

    Args:
        None

    Returns:
        None
    """
    # 1. Initialize DB
    print("Initializing Database...")
    database.init_db()

    # 2. Build Bot
    print("Building Telegram application...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # 3. Add Handlers
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("help", handlers.start))
    app.add_handler(CommandHandler("note", handlers.note_cmd))
    app.add_handler(CommandHandler("notes", handlers.list_notes))
    app.add_handler(CommandHandler("task", handlers.task_cmd))
    app.add_handler(CommandHandler("tasks", handlers.list_tasks))
    app.add_handler(CommandHandler("done", handlers.complete_task_cmd))
    app.add_handler(CommandHandler("delete", handlers.delete_task_cmd))
    app.add_handler(CommandHandler("remind", handlers.remind_cmd))
    app.add_handler(CommandHandler("search", handlers.search_cmd))
    app.add_handler(CommandHandler("memory", handlers.memory_cmd))
    app.add_handler(CommandHandler("memories", handlers.list_memories))
    app.add_handler(CommandHandler("forget", handlers.forget_cmd))

    # Fallback to chat
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.chat_handler))

    # 4. Initialize Scheduler
    print("Starting Scheduler...")
    scheduler.init_scheduler(app.bot)

    # 5. Run loop
    print("Running Local Assistant Polling loop...")
    app.run_polling()

if __name__ == "__main__":
    main()
