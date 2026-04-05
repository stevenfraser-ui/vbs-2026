import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_PATH = PROJECT_ROOT / os.getenv("ASSETS_PATH", "assets")
INTEL_PATH = PROJECT_ROOT / "intel"
DB_PATH = PROJECT_ROOT / os.getenv("DB_PATH", "data/intel_station.db")

# Admin
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "imf2026")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# App
APP_TITLE = "IMF Intelligence Terminal"
