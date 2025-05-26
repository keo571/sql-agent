# sql_agent/config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

class Settings:
    DATABASE_URL = f"sqlite:///{PROJECT_ROOT}/data/test.db"
    SCHEMA_DB_URL = f"sqlite:///{PROJECT_ROOT}/data/schema.db"
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def get_settings():
    return Settings()