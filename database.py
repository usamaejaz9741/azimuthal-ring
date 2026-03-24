"""Database management module for the Local AI Telegram Assistant.

This module provides helper functions to interact with the SQLite database,
including initializing tables, and performing CRUD operations for notes,
tasks, and memories.
"""

import sqlite3
import os
from config import DB_PATH


def get_db():
    """Establish a connection to the SQLite database with synchronous tuning.

    Returns:
        sqlite3.Connection: A SQLite connection object with Row factory set.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Optimization: Use NORMAL synchronous mode to speed up writes
    # Note: journal_mode=WAL is set once in init_db() as it is persistent.
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_db():
    """Initialize the SQLite database using the schema.sql file.

    This function reads the SQL commands from schema.sql and executes them
    on the current database to create the necessary tables.
    """
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    conn = get_db()
    # Optimization: Enable WAL mode once during initialization (persistent)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(schema)
    conn.commit()
    conn.close()


def add_note(content: str):
    """Add a new note to the database.

    Args:
        content (str): The text content of the note to be added.
    """
    conn = get_db()
    conn.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()


def get_notes():
    """Retrieve the 10 most recent notes from the database.

    Returns:
        list[sqlite3.Row]: A list of rows containing the note information.
    """
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes ORDER BY created_at DESC LIMIT 10").fetchall()
    conn.close()
    return notes


def add_task(text: str):
    """Add a new task to the to-do list in the database.

    Args:
        text (str): The text description of the task.
    """
    conn = get_db()
    conn.execute("INSERT INTO tasks (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()


def get_tasks():
    """Retrieve all open tasks from the database.

    Returns:
        list[sqlite3.Row]: A list of rows containing open tasks.
    """
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks WHERE status = 'open'").fetchall()
    conn.close()
    return tasks


def complete_task(task_id: int):
    """Mark a specific task as completed in the database.

    Args:
        task_id (int): The unique ID of the task to be marked as done.

    Returns:
        bool: True if a task was updated, False otherwise.
    """
    conn = get_db()
    cursor = conn.execute("UPDATE tasks SET status = 'done' WHERE id = ? AND status = 'open'", (task_id,))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def delete_task(task_id: int):
    """Permanently delete a specific task from the database.

    Args:
        task_id (int): The unique ID of the task to be deleted.

    Returns:
        bool: True if a task was deleted, False otherwise.
    """
    conn = get_db()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def set_memory(key: str, value: str):
    """Add or update a key-value pair in the memory storage.

    Args:
        key (str): The key representing the fact's name.
        value (str): The value containing the fact's details.
    """
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def get_memory():
    """Retrieve all stored memories from the database.

    Returns:
        list[sqlite3.Row]: A list of rows containing all key-value memories.
    """
    conn = get_db()
    memories = conn.execute("SELECT * FROM memory").fetchall()
    conn.close()
    return memories
