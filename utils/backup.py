"""Database backup and restore."""

import os
import shutil
from datetime import datetime
from config import DB_PATH, BACKUPS_DIR, MAX_BACKUPS, BACKUP_DATE_FORMAT


def create_backup() -> str:
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Database not found.")
    timestamp = datetime.now().strftime(BACKUP_DATE_FORMAT)
    backup_name = f"spot_backup_{timestamp}.db"
    backup_path = os.path.join(BACKUPS_DIR, backup_name)
    shutil.copy2(DB_PATH, backup_path)
    _cleanup_old_backups()
    return backup_path


def restore_backup(backup_path: str) -> None:
    if not os.path.exists(backup_path):
        raise FileNotFoundError("Backup file not found.")
    if os.path.exists(DB_PATH):
        safety_name = f"spot_pre_restore_{datetime.now().strftime(BACKUP_DATE_FORMAT)}.db"
        safety_path = os.path.join(BACKUPS_DIR, safety_name)
        shutil.copy2(DB_PATH, safety_path)
    shutil.copy2(backup_path, DB_PATH)


def list_backups() -> list[dict]:
    if not os.path.exists(BACKUPS_DIR):
        return []
    backups = []
    for filename in sorted(os.listdir(BACKUPS_DIR), reverse=True):
        if filename.startswith("spot_backup_") and filename.endswith(".db"):
            path = os.path.join(BACKUPS_DIR, filename)
            size = os.path.getsize(path)
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            backups.append({
                "filename": filename,
                "path": path,
                "size_kb": round(size / 1024, 2),
                "created": mtime.strftime("%Y-%m-%d %H:%M"),
            })
    return backups


def delete_backup(backup_path: str) -> None:
    if os.path.exists(backup_path):
        os.remove(backup_path)


def _cleanup_old_backups():
    backups = list_backups()
    if len(backups) > MAX_BACKUPS:
        for old in backups[MAX_BACKUPS:]:
            delete_backup(old["path"])