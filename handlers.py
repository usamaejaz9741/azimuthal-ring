"""Handler module for the Local AI Telegram Assistant.

This module contains the asynchronous functions that handle various Telegram
commands and messages, including note taking, task management, reminders,
web search, and AI-powered chat.
"""

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
import database
from llm import llm_service
from scheduler import schedule_reminder
from search import quick_search
from utils import get_help_text, restricted


@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start and /help commands.

    Displays the help text to the user.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    await update.message.reply_text(get_help_text(), parse_mode='Markdown')


@restricted
async def note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /note command.

    Saves a new note to the database.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    if not context.args:
        return await update.message.reply_text("Usage: /note <content>")
    text = " ".join(context.args)
    database.add_note(text)
    await update.message.reply_text("📝 Note saved.")


@restricted
async def list_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /notes command.

    Lists the 10 most recent notes from the database.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    notes = database.get_notes()
    if not notes:
        return await update.message.reply_text("No notes saved.")
    msg = "\n".join([f"• {n['content']}" for n in notes])
    await update.message.reply_text(f"Recent Notes:\n{msg}")


@restricted
async def task_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /task command.

    Adds a new task to the to-do list in the database.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    if not context.args:
        return await update.message.reply_text("Usage: /task <content>")
    text = " ".join(context.args)
    database.add_task(text)
    await update.message.reply_text("🗓 Task added.")


@restricted
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /tasks command.

    Lists all open tasks from the database.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    tasks = database.get_tasks()
    if not tasks:
        return await update.message.reply_text("✅ All tasks complete.")
    msg = "\n".join([f"{t['id']}. {t['text']} (Created: {t['created_at'].split()[0]})" for t in tasks])
    await update.message.reply_text(f"Your Pending Tasks:\n{msg}")


@restricted
async def complete_task_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /done command.

    Marks a specific task as completed in the database.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    if not context.args:
        return await update.message.reply_text("Usage: /done <task_id>")
    try:
        success = database.complete_task(int(context.args[0]))
        if success:
            await update.message.reply_text("✅ Task marked as done.")
        else:
            await update.message.reply_text("❌ Task not found or already completed.")
    except (ValueError, IndexError):
        await update.message.reply_text("❌ Invalid ID.")


@restricted
async def delete_task_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /delete command.

    Deletes a specific task from the database.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    if not context.args:
        return await update.message.reply_text("Usage: /delete <task_id>")
    try:
        success = database.delete_task(int(context.args[0]))
        if success:
            await update.message.reply_text("🗑 Task deleted.")
        else:
            await update.message.reply_text("❌ Task not found.")
    except (ValueError, IndexError):
        await update.message.reply_text("❌ Invalid ID.")


@restricted
async def remind_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /remind command.

    Schedules a reminder to be sent after a specified number of minutes.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /remind 10 Remind me about milk")
    
    try:
        minutes = int(context.args[0])
        msg = " ".join(context.args[1:])
        schedule_reminder(context.application, update.effective_chat.id, msg, minutes * 60)
        await update.message.reply_text(f"⏳ Reminder set status: OK (In {minutes} minutes)")
    except ValueError:
        await update.message.reply_text("❌ Minutes must be an integer.")


@restricted
async def search_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /search command.

    Performs a web search and uses the local AI to summarize the results.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    if not context.args:
        return await update.message.reply_text("Usage: /search <query>")
    
    query = " ".join(context.args)
    res_text = await update.message.reply_text(f"🔍 Searching for: {query}...")
    
    results = quick_search(query)
    
    # If no results were found, inform the user directly and skip LLM
    if results.startswith("No results found") or results.startswith("Web search is currently"):
        return await context.bot.edit_message_text(
            f"❌ *{query}*: {results}",
            chat_id=update.effective_chat.id,
            message_id=res_text.message_id,
            parse_mode='Markdown'
        )

    # Use LLM to summarize results
    summary = llm_service.summarize(results)
    
    await context.bot.edit_message_text(
        f"🐱 *Choji's Summary* for *{query}*:\n\n{summary}\n\n_Analyzed locally by your buddy Choji_",
        chat_id=update.effective_chat.id,
        message_id=res_text.message_id,
        parse_mode='Markdown'
    )


@restricted
async def memory_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /memory command.

    Saves a fact about the user in the database.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /memory nickname usama")
    key = context.args[0]
    val = " ".join(context.args[1:])
    database.set_memory(key, val)
    await update.message.reply_text(f"🧠 Memory updated: {key} = {val}")


@restricted
async def list_memories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /memories command.

    Lists all stored facts about the user from the database.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    memories = database.get_memory()
    if not memories:
        return await update.message.reply_text("I memory nothing special.")
    msg = "\n".join([f"{m['key']}: {m['value']}" for m in memories])
    await update.message.reply_text(f"Knowledge I have about you:\n{msg}")


@restricted
async def forget_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /forget command.

    Deletes a specific user fact from the memory database.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    if not context.args:
        return await update.message.reply_text("Usage: /forget <key>")
    key = context.args[0]
    success = database.delete_memory(key)
    if success:
        await update.message.reply_text(f"🗑 Memory deleted: {key}")
    else:
        await update.message.reply_text(f"❌ Key '{key}' not found in memory.")


@restricted
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general text messages for AI chat.

    Processes non-command text messages using the local AI service.

    Args:
        update (Update): The update object containing information about the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the handler.

    Returns:
        None
    """
    # Pass to LLM with memory context
    text = update.message.text
    if text:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        
        # 1. Fetch memories from DB
        memories = database.get_memory()
        memory_str = ""
        if memories:
            memory_list = [f"{m['key']}: {m['value']}" for m in memories]
            memory_str = "USER INFORMATION:\n" + "\n".join(memory_list)
        
        # 2. Pass to LLM with context
        response = llm_service.generate(text, context=memory_str)
        await update.message.reply_text(response)
