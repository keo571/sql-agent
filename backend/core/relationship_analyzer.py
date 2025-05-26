# sql_agent/core/relationship_analyzer.py
from sqlalchemy import inspect
from ..utils.logger import get_logger
from backend.database.connection import get_database_engine

logger = get_logger(__name__)

class RelationshipAnalyzer:
    def __init__(self, schema_manager):
        self.schema_manager = schema_manager
        self.engine = get_database_engine()
    
    def analyze_relationships(self, table_name):
        """Analyze relationships for a specific table"""
        inspector = inspect(self.engine)
        relationships = []
        
        # Get primary key information
        pk_columns = inspector.get_pk_constraint(table_name)['constrained_columns']
        for pk_col in pk_columns:
            relationships.append({
                'source': f"{table_name}.{pk_col}",
                'target': f"{table_name}.{pk_col}",
                'relationship_type': 'primary_key',
                'description': f"Primary Key: {pk_col}"
            })
        
        # Get foreign key information
        foreign_keys = inspector.get_foreign_keys(table_name)
        for fk in foreign_keys:
            source_col = fk['constrained_columns'][0]
            target_table = fk['referred_table']
            target_col = fk['referred_columns'][0]
            relationships.append({
                'source': f"{table_name}.{source_col}",
                'target': f"{target_table}.{target_col}",
                'relationship_type': 'foreign_key',
                'description': f"Foreign Key: {source_col} -> {target_table}.{target_col}"
            })
        
        return relationships