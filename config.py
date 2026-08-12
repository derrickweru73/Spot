config_py = '''"""Spot configuration and settings."""

import os

# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, 'spot.db')
PHOTOS_DIR = os.path.join(BASE_DIR, 'photos')
BACKUPS_DIR = os.path.join(BASE_DIR, 'backups')
CONFIG_FILE = os.path.join(BASE_DIR, 'spot_config.ini')

# Ensure directories exist
for d in [PHOTOS_DIR, BACKUPS_DIR]:
    os.makedirs(d, exist_ok=True)

# ============================================================
# APP SETTINGS
# ============================================================

APP_NAME = "Spot"
APP_VERSION = "2.0"
APP_WIDTH = 1200
APP_HEIGHT = 720
APP_MIN_WIDTH = 900
APP_MIN_HEIGHT = 600

# ============================================================
# NOTIFICATION SETTINGS
# ============================================================

TOAST_DURATION = 3000  # milliseconds
CHECK_OVERDUE_INTERVAL = 60000  # check every 60 seconds

# ============================================================
# SEARCH SETTINGS
# ============================================================

SEARCH_DEBOUNCE_MS = 300

# ============================================================
# BACKUP SETTINGS
# ============================================================

MAX_BACKUPS = 10
BACKUP_DATE_FORMAT = "%Y%m%d_%H%M%S"

# ============================================================
# PIN LOCK SETTINGS
# ============================================================

PIN_MAX_ATTEMPTS = 3
PIN_LENGTH = 4
'''

with open('/mnt/agents/output/spot/config.py', 'w') as f:
    f.write(config_py)

print("config.py written")