from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN
import database
import handlers
import scheduler

def main():
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

    # Fallback to chat
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handlers.chat_handler))

    # 4. Run loop
    print("Running Local Assistant Polling loop...")
    app.run_polling()

if __name__ == "__main__":
    main()
