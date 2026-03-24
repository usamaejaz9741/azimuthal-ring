import os
import sys
import subprocess
from config import DB_PATH
from database import init_db

def stop_bot_instances():
    """Find and terminate any running bot.py processes to release database locks."""
    print("Stopping any running processes that might be locking the database...")
    try:
        if sys.platform == "win32":
            # Targeted kill for bot instances via taskkill for force
            subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/FI", "WINDOWTITLE eq bot.py*", "/T"], capture_output=True)
            subprocess.run(["taskkill", "/F", "/IM", "python3.exe", "/T"], capture_output=True)
            subprocess.run(["taskkill", "/F", "/IM", "python3.13.exe", "/T"], capture_output=True)
            
            # General PowerShell backup for anything else matching 'bot.py'
            cmd = 'Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*python*bot.py*" } | Stop-Process -Force -ErrorAction SilentlyContinue'
            subprocess.run(["powershell.exe", "-Command", cmd], capture_output=True, shell=True)
        else:
            # Simple pkill for Unix-like systems
            subprocess.run(["pkill", "-f", "bot.py"], capture_output=True)
        print("Bot instances stopped (if any were running).")
    except Exception as e:
        print(f"Warning: Could not stop bot instances automatically: {e}")

def reset_database():
    """Wipe the existing SQLite database and re-initialize it from schema.sql."""
    # Stop the bot first to release file handles
    stop_bot_instances()
    
    print(f"Target database path: {DB_PATH}")
    
    # List of files to remove (including SQLite journal files)
    files_to_remove = [
        DB_PATH,
        f"{DB_PATH}-shm",
        f"{DB_PATH}-wal"
    ]
    
    removed_count = 0
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed: {file_path}")
                removed_count += 1
            except PermissionError:
                print(f"Error: Could not remove {file_path}. Is the bot still running?")
                sys.exit(1)
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
                sys.exit(1)

    if removed_count == 0:
        print("No existing database files found to remove.")
    
    print("Initializing fresh database...")
    try:
        init_db()
        print("Done! Database has been reset and re-initialized.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Optional: Add a confirmation prompt if run manually
    confirm = input("This will PERMANENTLY delete all notes, tasks, and memory. Proceed? (y/n): ")
    if confirm.lower() == 'y':
        reset_database()
    else:
        print("Reset cancelled.")
