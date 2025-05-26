from typing import Any, Dict, List
from sqlalchemy import text
from ..database.connection import get_database_engine


class DatabaseEngine:
    def __init__(self, schema_manager):
        self.schema_manager = schema_manager
        self.engine = get_database_engine()

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results as a list of dictionaries."""
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            columns = result.keys()
            results = [dict(zip(columns, row)) for row in result.fetchall()]
            return results