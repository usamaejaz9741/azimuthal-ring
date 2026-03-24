import pytest
import os
import sqlite3
import time
from database import init_db, add_note, get_notes, add_task, get_tasks, complete_task, delete_task, set_memory, get_memory
import database
import config

@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "test_assistant.db"
    # Overwrite DB_PATH in BOTH config and database modules
    original_path = config.DB_PATH
    config.DB_PATH = str(db_file)
    database.DB_PATH = str(db_file)

    init_db()
    yield str(db_file)

    if os.path.exists(db_file):
        os.remove(db_file)
    # Restore (optional but good practice)
    config.DB_PATH = original_path
    database.DB_PATH = original_path

def test_notes(test_db):
    add_note("Test note 1")
    time.sleep(1.1)
    add_note("Test note 2")
    notes = get_notes()
    assert len(notes) == 2
    assert notes[0]['content'] == "Test note 2"
    assert notes[1]['content'] == "Test note 1"

def test_tasks(test_db):
    add_task("Task 1")
    add_task("Task 2")
    tasks = get_tasks()
    assert len(tasks) == 2

    task_id = tasks[0]['id']
    complete_task(task_id)

    tasks_after = get_tasks()
    assert len(tasks_after) == 1

    delete_task(tasks_after[0]['id'])
    assert len(get_tasks()) == 0

def test_memory(test_db):
    set_memory("name", "Jules")
    set_memory("city", "Paris")
    set_memory("name", "Julian") # Test REPLACE

    memories = get_memory()
    mem_dict = {m['key']: m['value'] for m in memories}
    assert mem_dict["name"] == "Julian"
    assert mem_dict["city"] == "Paris"
