from sqlalchemy import text, Engine
from ..utils.logger import get_logger

logger = get_logger(__name__)

def sql_engine(query: str, engine: Engine) -> str:
    """
    Execute SQL queries on the database. Returns a string representation of the result.
    The database schema is managed by SchemaManager.

    Args:
        query: The SQL query to execute. This should be valid SQL syntax.
        engine: SQLAlchemy engine instance
    """
    output = []
    try:
        with engine.connect() as con:
            result = con.execute(text(query))
            columns = result.keys()
            for row in result:
                output.append(dict(zip(columns, row)))
        return str(output)
    except Exception as e:
        logger.error(f"SQL query execution failed: {str(e)}")
        return f"Error executing query: {str(e)}"