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

# Security: Only allow this user ID to interact with the bot
# Get your ID from @userinfobot or similar
AUTHORIZED_USER_ID = os.getenv("AUTHORIZED_USER_ID")
if AUTHORIZED_USER_ID and AUTHORIZED_USER_ID.strip():
    try:
        AUTHORIZED_USER_ID = int(AUTHORIZED_USER_ID)
    except ValueError:
        print("Warning: AUTHORIZED_USER_ID must be an integer. Security restriction disabled.")
        AUTHORIZED_USER_ID = None

# Absolute path for the database file (SQLite specific)
DB_PATH = DATABASE_URL.replace("sqlite:///", "")
