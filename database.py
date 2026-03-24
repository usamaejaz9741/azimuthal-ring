import sqlite3
import os
from config import DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    conn = get_db()
    conn.executescript(schema)
    conn.commit()
    conn.close()

def add_note(content: str):
    conn = get_db()
    conn.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

def get_notes():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes ORDER BY created_at DESC LIMIT 10").fetchall()
    conn.close()
    return notes

def add_task(text: str):
    conn = get_db()
    conn.execute("INSERT INTO tasks (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def get_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks WHERE status = 'open'").fetchall()
    conn.close()
    return tasks

def complete_task(task_id: int):
    conn = get_db()
    conn.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id: int):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def set_memory(key: str, value: str):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_memory():
    conn = get_db()
    memories = conn.execute("SELECT * FROM memory").fetchall()
    conn.close()
    return memories
