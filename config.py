"""Configuration module for the Local AI Telegram Assistant.

This module loads environment variables and defines constants used throughout
the application, such as API tokens, model paths, and database URLs.
"""

import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MODEL_PATH = os.getenv("MODEL_PATH", "models/qwen2.5-0.5b-instruct-q4_k_m.gguf")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///assistant.db")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Absolute path for the database file (SQLite specific)
DB_PATH = DATABASE_URL.replace("sqlite:///", "")
