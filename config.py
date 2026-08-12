"""Spot configuration."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'spot.db')
PHOTOS_DIR = os.path.join(BASE_DIR, 'photos')
BACKUPS_DIR = os.path.join(BASE_DIR, 'backups')
CONFIG_FILE = os.path.join(BASE_DIR, 'spot_config.ini')

for d in [PHOTOS_DIR, BACKUPS_DIR]:
    os.makedirs(d, exist_ok=True)

APP_NAME = "Spot"
APP_VERSION = "2.0"
APP_WIDTH = 1200
APP_HEIGHT = 720
APP_MIN_WIDTH = 900
APP_MIN_HEIGHT = 600

TOAST_DURATION = 3000
CHECK_OVERDUE_INTERVAL = 60000
SEARCH_DEBOUNCE_MS = 300
MAX_BACKUPS = 10
BACKUP_DATE_FORMAT = "%Y%m%d_%H%M%S"
PIN_MAX_ATTEMPTS = 3
PIN_LENGTH = 4