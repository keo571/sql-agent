1# sql_agent/database/models.py
from sqlalchemy import MetaData, Table, Column, String, Integer, JSON

def create_schema_metadata():
    metadata = MetaData()
    
    Table(
        'table_schemas',
        metadata,
        Column('table_name', String, primary_key=True),
        Column('schema', JSON),
        Column('relationships', JSON),
        Column('last_updated', String),
        Column('description', String)
    )
    
    return metadata