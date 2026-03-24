# 🤖 Local-First AI Telegram Assistant

A brutally practical, lightweight, and local-first personal assistant.

## Features
- **Local LLM**: Uses Qwen2.5-0.5B-GGUF for zero-cost, private conversation.
- **SQLite Storage**: Persistent notes, tasks, and memory.
- **Web Search**: Dynamic summaries via DuckDuckGo (privacy-conscious).
- **Reminders**: SQLite-persisted reminders.
- **CPU-Only**: Optimized for very weak hardware and limited RAM.

## ⚙️ Initial Setup

1. **Install Python 3.10+**.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Setup**:
   - Copy `.env.example` to `.env`.
   - Add your Telegram Bot Token from `@BotFather`.
4. **Prepare the Model**:
   - Create a folder called `models`.
   - Download `qwen2.5-0.5b-instruct-q4_k_m.gguf` from HuggingFace.
   - Place it in the `models/` directory.
5. **Initialize Database**:
   - Just run the bot; it will auto-create the tables.

## 🚀 Running
```bash
python bot.py
```

## 📋 Commands
- `/note <text>`: Quick item capture.
- `/task <text>`: Add to your to-do list.
- `/tasks`: List open tasks.
- `/done <id>`: Mark task as finished.
- `/remind 10 Buy groceries`: Remind you in X minutes.
- `/search <query>`: Web search and AI summarization.
- `/memory name John`: Tell the bot something about you.
- `/memories`: List all stored memories.

## 🏗️ Technical Choices
- **Qwen2.5-0.5B**: Only ~350MB of RAM. Very fast on plain CPUs.
- **llama-cpp-python**: Direct C++ bindings for performance.
- **APScheduler**: Simple background job management.
- **DuckDuckGo**: Free, scraper-based search with no API keys.
