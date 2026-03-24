from telegram import Update
from telegram.ext import ContextTypes
import database
from llm import llm_service
from scheduler import schedule_reminder
from search import quick_search
from utils import get_help_text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_help_text(), parse_mode='Markdown')

async def note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /note <content>")
    text = " ".join(context.args)
    database.add_note(text)
    await update.message.reply_text("📝 Note saved.")

async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notes = database.get_notes()
    if not notes:
        return await update.message.reply_text("No notes saved.")
    msg = "\n".join([f"• {n['content']}" for n in notes])
    await update.message.reply_text(f"Recent Notes:\n{msg}")

async def task_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /task <content>")
    text = " ".join(context.args)
    database.add_task(text)
    await update.message.reply_text("🗓 Task added.")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = database.get_tasks()
    if not tasks:
        return await update.message.reply_text("✅ All tasks complete.")
    msg = "\n".join([f"{t['id']}. {t['text']} (Created: {t['created_at'].split()[0]})" for t in tasks])
    await update.message.reply_text(f"Your Pending Tasks:\n{msg}")

async def complete_task_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /done <task_id>")
    try:
        database.complete_task(int(context.args[0]))
        await update.message.reply_text("✅ Task marked as done.")
    except:
        await update.message.reply_text("❌ Invalid ID.")

async def delete_task_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /delete <task_id>")
    try:
        database.delete_task(int(context.args[0]))
        await update.message.reply_text("🗑 Task deleted.")
    except:
        await update.message.reply_text("❌ Error deleting task.")

async def remind_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /remind 10 Remind me about milk")
    
    try:
        minutes = int(context.args[0])
        msg = " ".join(context.args[1:])
        schedule_reminder(context.application, update.effective_chat.id, msg, minutes * 60)
        await update.message.reply_text(f"⏳ Reminder set status: OK (In {minutes} minutes)")
    except ValueError:
        await update.message.reply_text("❌ Minutes must be an integer.")

async def search_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /search <query>")
    
    query = " ".join(context.args)
    res_text = await update.message.reply_text(f"🔍 Searching for: {query}...")
    
    results = quick_search(query)
    # Use LLM to summarize results
    summary = llm_service.summarize(results)
    
    await context.bot.edit_message_text(
        f"🌐 Web Summary for *{query}*:\n\n{summary}\n\n_Source summary using local AI_",
        chat_id=update.effective_chat.id,
        message_id=res_text.message_id,
        parse_mode='Markdown'
    )

async def memory_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /memory nickname usama")
    key = context.args[0]
    val = " ".join(context.args[1:])
    database.set_memory(key, val)
    await update.message.reply_text(f"🧠 Memory updated: {key} = {val}")

async def list_memories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memories = database.get_memory()
    if not memories:
        return await update.message.reply_text("I memory nothing special.")
    msg = "\n".join([f"{m['key']}: {m['value']}" for m in memories])
    await update.message.reply_text(f"Knowledge I have about you:\n{msg}")

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pass to LLM
    text = update.message.text
    if text:
        # Check if the text is short enough to be a task without command 
        # (optional deterministic logic)
        response = llm_service.generate(text)
        await update.message.reply_text(response)
