# sql_agent/core/schema_manager.py
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, JSON, inspect
from datetime import datetime
from pathlib import Path
from ..utils.logger import get_logger
from ..database.connection import get_database_engine

logger = get_logger(__name__)

class SchemaManager:
    def __init__(self, schema_db_url=None):
        if schema_db_url is None:
            # Use data/schema.db as default
            data_dir = Path(__file__).parent.parent.parent / 'data'
            data_dir.mkdir(exist_ok=True)
            schema_db_url = f"sqlite:///{data_dir}/schema.db"
        
        self.schema_engine = create_engine(schema_db_url)
        self.metadata = MetaData()

        # Create schema metadata table with relationship information
        self.schema_table = Table(
            'table_schemas',
            self.metadata,
            Column('table_name', String, primary_key=True),
            Column('schema', JSON),  # Store schema as JSON
            Column('relationships', JSON),  # Store relationships as JSON
            Column('last_updated', String),
            Column('description', String)
        )
        
        self.metadata.create_all(self.schema_engine)
    
    def load_schema(self, table_name):
        """Load schema information for a table"""
        # Use the main database engine to inspect tables
        engine = get_database_engine()
        inspector = inspect(engine)
        
        columns = []
        for column in inspector.get_columns(table_name):
            col_info = {
                'name': column['name'],
                'type': str(column['type']),
                'nullable': column.get('nullable', True),
                'primary_key': column.get('primary_key', False)
            }
            columns.append(col_info)
        
        # Get foreign key information
        foreign_keys = []
        for fk in inspector.get_foreign_keys(table_name):
            foreign_keys.append({
                'constrained_columns': fk['constrained_columns'],
                'referred_table': fk['referred_table'],
                'referred_columns': fk['referred_columns']
            })
        
        # Update schema in metadata database
        self.update_schema(table_name, columns, foreign_keys)
    
    def update_schema(self, table_name, columns, relationships=None, description=""):
        """Update or insert schema information for a table"""
        with self.schema_engine.connect() as conn:
            # Check if record exists
            result = conn.execute(
                self.schema_table.select().where(
                    self.schema_table.c.table_name == table_name
                )
            ).first()
            
            schema_data = {
                'columns': columns,
                'foreign_keys': relationships or []
            }
            
            if result:
                # Update existing record
                conn.execute(
                    self.schema_table.update()
                    .where(self.schema_table.c.table_name == table_name)
                    .values(
                        schema=schema_data,
                        relationships=relationships or [],
                        last_updated=datetime.now().isoformat(),
                        description=description
                    )
                )
            else:
                # Insert new record
                conn.execute(
                    self.schema_table.insert().values(
                        table_name=table_name,
                        schema=schema_data,
                        relationships=relationships or [],
                        last_updated=datetime.now().isoformat(),
                        description=description
                    )
                )
            conn.commit()
    
    def get_schema(self, table_name):
        """Retrieve schema for a specific table"""
        with self.schema_engine.connect() as conn:
            result = conn.execute(
                self.schema_table.select().where(
                    self.schema_table.c.table_name == table_name
                )
            ).first()
            return result.schema if result else None
    
    def get_all_schemas(self):
        """Retrieve schemas for all tables"""
        schemas = {}
        with self.schema_engine.connect() as conn:
            results = conn.execute(self.schema_table.select()).fetchall()
            for result in results:
                schemas[result.table_name] = result.schema
        return schemas