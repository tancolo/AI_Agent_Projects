import os
from datetime import datetime
from pathlib import Path

def log_message(message: str, level: str = "INFO", log_file: Path = Path("archiver_log.txt")) -> None:
    """Log a message to console and log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def ensure_directory(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
    # Don't log every directory creation to avoid spam, or log deeply if needed
