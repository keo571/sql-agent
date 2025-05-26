# sql_agent/database/connection.py
from sqlalchemy import create_engine
from ..config.settings import get_settings

def get_database_engine():
    settings = get_settings()
    return create_engine(settings.DATABASE_URL)