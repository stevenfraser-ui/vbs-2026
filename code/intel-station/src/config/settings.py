import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_PATH = PROJECT_ROOT / os.getenv("ASSETS_PATH", "assets")
KB_PATH = PROJECT_ROOT / os.getenv("KB_PATH", "knowledge_base")
SKILLS_PATH = PROJECT_ROOT / os.getenv("SKILLS_PATH", "skills")
DB_PATH = PROJECT_ROOT / os.getenv("DB_PATH", "data/intel_station.db")

# Ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://192.168.4.104:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# Admin
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "imf2026")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# App
APP_TITLE = "IMF Intelligence Terminal"
MAX_CHAT_HISTORY = 50
HINT_THRESHOLD = 3  # failed attempts before AI gives a hint
