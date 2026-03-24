# 🤖 Local-First AI Telegram Assistant

A brutally practical, lightweight, and local-first personal assistant. This bot is designed to run entirely on your own hardware, ensuring privacy and zero operational costs for the AI.

## 🌟 Features
- **Local LLM**: Uses Qwen2.5-0.5B-GGUF for private, zero-cost conversation and text processing.
- **SQLite Storage**: Persistent management of notes, tasks, and personal "memories".
- **Web Search**: Privacy-conscious web search via DuckDuckGo with AI-generated summaries.
- **Persistent Reminders**: Background-scheduled reminders that survive bot restarts.
- **Ultra-Lightweight**: Optimized to run on very weak hardware (CPU-only, <400MB RAM).

## ⚙️ Initial Setup

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- A Telegram Bot Token (obtainable from [@BotFather](https://t.me/BotFather)).

### 2. Installation
1. Clone the repository to your local machine.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Environment Configuration
1. Copy the `.env.example` file to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure the following variables:
   - `TELEGRAM_TOKEN`: **(Required)** Your Telegram Bot Token from @BotFather.
   - `AUTHORIZED_USER_ID`: **(Highly Recommended)** Your Telegram User ID (get it from @userinfobot) to restrict the bot to your use only. If left empty, anyone can use the bot.
   - `MODEL_PATH`: Path to your GGUF model file (default: `models/qwen2.5-0.5b-instruct-q4_k_m.gguf`).
   - `DATABASE_URL`: SQLite database connection string (default: `sqlite:///assistant.db`).
   - `TIMEZONE`: Your local timezone (default: `UTC`).
   - `LOG_LEVEL`: Logging verbosity (default: `INFO`).

### 4. Prepare the AI Model
1. Create a directory named `models` in the project root.
2. Download the `qwen2.5-0.5b-instruct-q4_k_m.gguf` model (or similar) from HuggingFace.
3. Place the downloaded `.gguf` file into the `models/` directory.

### 5. Database Initialization
The bot uses SQLite and will automatically create the necessary database file (`assistant.db`) and tables on its first run.

## 🚀 Running the Bot
To start your assistant, simply run:
```bash
python bot.py
```

## 📋 Available Commands
- `/note <text>`: Save a quick note.
- `/notes`: List your 10 most recent notes.
- `/task <text>`: Add a new item to your to-do list.
- `/tasks`: Show all pending tasks.
- `/done <id>`: Mark a task as completed.
- `/delete <id>`: Remove a task permanently.
- `/remind <min> <text>`: Set a reminder (e.g., `/remind 10 Check oven`).
- `/search <query>`: Search the web and get an AI-summarized result.
- `/memory <key> <val>`: Tell the bot a fact about yourself (e.g., `/memory birthday May 5th`).
- `/memories`: List everything the bot knows about you.
- **Chat**: Just send a regular message to have a conversation with the AI!

## 🏗️ Architecture Overview
The project is structured for simplicity and modularity:
- `bot.py`: The main entry point that wires everything together.
- `handlers.py`: Contains the logic for responding to Telegram commands and messages.
- `database.py`: Manages SQLite interactions for persistent storage.
- `llm.py`: Wraps `llama-cpp-python` for local AI inference.
- `scheduler.py`: Uses `APScheduler` for managing background reminder tasks.
- `search.py`: Handles web searching via DuckDuckGo.
- `utils.py`: Contains shared helper functions.

## 🛠️ Developer Guide

### Code Style and Documentation
This project adheres to the **Google Style Python Docstrings**. Every public function, method, and class must have a complete docstring that describes:
- The purpose or main action of the code.
- Descriptions for every parameter/argument.
- Descriptions for the return value.

Example:
```python
def add_note(content: str):
    """Add a new note to the database.

    Args:
        content (str): The text content of the note to be added.

    Returns:
        None
    """
    # ... implementation ...
```

### Running Tests
The project uses `pytest` for testing, along with `pytest-asyncio` for asynchronous handlers and `pytest-cov` for coverage reports.

To run the full suite:
```bash
python -m pytest
```

To run with coverage:
```bash
python -m pytest --cov=. --cov-report=term-missing
```

### Project Structure
- `bot.py`: Main entry point. Wires Telegram handlers and starts polling.
- `handlers.py`: Asynchronous command and message handlers.
- `database.py`: SQLite abstraction layer for notes, tasks, and memory.
- `llm.py`: Singleton service for local AI inference using `llama-cpp-python`.
- `scheduler.py`: Background job management for persistent reminders.
- `search.py`: Web search integration via DuckDuckGo.
- `utils.py`: Shared utilities and security decorators.

### Contributing
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. **Ensure full docstring coverage** following the project's documentation standards.
4. Run tests to ensure no regressions and verify functionality.
5. Submit a pull request!

## 📜 Technical Choices
- **Qwen2.5-0.5B**: Chosen for its incredible performance-to-size ratio, requiring only ~350MB of RAM.
- **llama-cpp-python**: Provides efficient C++ bindings for running GGUF models on CPUs.
- **APScheduler**: A robust library for scheduling background jobs with SQLAlchemy persistence.
- **DuckDuckGo**: Allows for web search without the need for API keys or complex setups.
