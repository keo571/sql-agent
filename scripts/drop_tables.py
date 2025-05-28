# scripts/drop_tables.py
from sqlalchemy import MetaData, Table, text
from backend.database.connection import get_database_engine
from backend.core.schema_manager import SchemaManager
import os

def drop_all_tables():
    """Drop all tables from the database and clean up schema metadata"""
    # Get the main database engine
    engine = get_database_engine()
    
    # Create schema manager
    schema_manager = SchemaManager()
    
    # Clean up main database
    with engine.connect() as conn:
        # First, disable foreign key constraints temporarily
        conn.execute(text("PRAGMA foreign_keys = OFF"))
        
        # Get all table names
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"))
        tables = [row[0] for row in result]
        
        for table_name in tables:
            try:
                # Drop the table if it exists
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                print(f"Successfully dropped table: {table_name}")
                
                # Clean up any remaining indexes
                conn.execute(text(f"DROP INDEX IF EXISTS idx_{table_name}_id"))
                print(f"Cleaned up indexes for: {table_name}")
                
            except Exception as e:
                print(f"Error dropping table {table_name}: {str(e)}")
        
        # Re-enable foreign key constraints
        conn.execute(text("PRAGMA foreign_keys = ON"))
        
        # Try to clean up sqlite_sequence if it exists
        try:
            conn.execute(text("DELETE FROM sqlite_sequence"))
            print("Cleaned up sqlite_sequence table")
        except Exception as e:
            print("Note: sqlite_sequence table not found or already clean")
        
        # Commit all changes before VACUUM
        conn.commit()
        
        # Vacuum the database to reclaim space (outside transaction)
        conn.execute(text("VACUUM"))
        print("Main database vacuumed and cleaned up!")
    
    # Clean up schema metadata
    with schema_manager.schema_engine.connect() as conn:
        # Remove all schema metadata
        conn.execute(text("DELETE FROM table_schemas"))
        print("Removed all schema metadata")
        
        # Commit changes before VACUUM
        conn.commit()
        
        # Vacuum schema.db (outside transaction)
        conn.execute(text("VACUUM"))
        print("Schema metadata cleaned up!")

def drop_specific_tables(tables_to_drop):
    """Drop specific tables from the database and clean up their schema metadata"""
    # Get the main database engine
    engine = get_database_engine()
    
    # Create schema manager
    schema_manager = SchemaManager()
    
    # Clean up main database
    with engine.connect() as conn:
        # First, disable foreign key constraints temporarily
        conn.execute(text("PRAGMA foreign_keys = OFF"))
        
        for table_name in tables_to_drop:
            try:
                # Drop the table if it exists
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                print(f"Successfully dropped table: {table_name}")
                
                # Clean up any remaining indexes
                conn.execute(text(f"DROP INDEX IF EXISTS idx_{table_name}_id"))
                print(f"Cleaned up indexes for: {table_name}")
                
            except Exception as e:
                print(f"Error dropping table {table_name}: {str(e)}")
        
        # Re-enable foreign key constraints
        conn.execute(text("PRAGMA foreign_keys = ON"))
        
        # Try to clean up sqlite_sequence if it exists
        try:
            conn.execute(text(f"DELETE FROM sqlite_sequence WHERE name IN ({','.join(['?'] * len(tables_to_drop))})", tables_to_drop))
            print("Cleaned up sqlite_sequence table")
        except Exception as e:
            print("Note: sqlite_sequence table not found or already clean")
        
        # Commit all changes before VACUUM
        conn.commit()
        
        # Vacuum the database to reclaim space (outside transaction)
        conn.execute(text("VACUUM"))
        print("Main database vacuumed and cleaned up!")
    
    # Clean up schema metadata
    with schema_manager.schema_engine.connect() as conn:
        # Remove schema metadata for dropped tables
        for table_name in tables_to_drop:
            try:
                conn.execute(text(f"DELETE FROM table_schemas WHERE table_name = '{table_name}'"))
                print(f"Removed schema metadata for: {table_name}")
            except Exception as e:
                print(f"Error removing schema metadata for {table_name}: {str(e)}")
        
        # Commit changes before VACUUM
        conn.commit()
        
        # Vacuum schema.db (outside transaction)
        conn.execute(text("VACUUM"))
        print("Schema metadata cleaned up!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        drop_all_tables()
        print("Finished dropping all tables and their schema metadata!")
    else:
        # Define the tables to drop
        tables_to_drop = ['customers', 'receipts', 'items']
        drop_specific_tables(tables_to_drop)
        print("Finished dropping specified tables and their schema metadata!") 