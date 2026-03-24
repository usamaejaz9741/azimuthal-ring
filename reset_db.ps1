# Restart-Database.ps1
# This script stops the bot, deletes the database files, and re-initializes it.

$DB_NAME = "assistant.db"

# 1. Stop the bot processing if it's running
Write-Host "Stopping any running 'bot.py' processes..." -ForegroundColor Yellow
$proc = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*python*bot.py*" }
if ($proc) {
    Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
    Write-Host "Bot process $($proc.ProcessId) stopped." -ForegroundColor Green
} else {
    Write-Host "No bot process found." -ForegroundColor DarkGray
}

# 2. Delete the database files
Write-Host "Deleting database files ($DB_NAME)..." -ForegroundColor Yellow
$files = Get-ChildItem -Path "$DB_NAME", "$DB_NAME-shm", "$DB_NAME-wal" -ErrorAction SilentlyContinue
if ($files) {
    $files | Remove-Item -Force
    Write-Host "Deleted $($files.Count) database files." -ForegroundColor Green
} else {
    Write-Host "No database files found to delete." -ForegroundColor DarkGray
}

# 3. Re-initialize (optional but good to confirm)
Write-Host "Running re-initialization..." -ForegroundColor Cyan
python -c "from database import init_db; init_db(); print('Database re-initialized.')"

Write-Host "---"
Write-Host "Database reset complete. You can now start the bot again with 'python bot.py'." -ForegroundColor Cyan
