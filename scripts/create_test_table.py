# scripts/create_test_table.py
import os
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, ForeignKey
from backend.database.connection import get_database_engine

def create_test_table():
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    engine = get_database_engine()
    metadata = MetaData()
    
    # Create customers table
    customers = Table(
        'customers',
        metadata,
        Column('customer_id', Integer, primary_key=True),
        Column('name', String(32)),
        Column('email', String(64))
    )
    
    # Create items table
    items = Table(
        'items',
        metadata,
        Column('item_id', Integer, primary_key=True),
        Column('name', String(32)),
        Column('price', Float)
    )
    
    # Create receipts table with foreign keys
    receipts = Table(
        'receipts',
        metadata,
        Column('receipt_id', Integer, primary_key=True),
        Column('customer_id', Integer, ForeignKey('customers.customer_id')),
        Column('item_id', Integer, ForeignKey('items.item_id')),
        Column('quantity', Integer),
        Column('tip', Float)
    )
    
    # Create the tables
    metadata.create_all(engine)
    
    # Insert test data
    with engine.connect() as conn:
        # Insert customers
        conn.execute(customers.insert(), [
            {'name': 'Alice', 'email': 'alice@example.com'},
            {'name': 'Bob', 'email': 'bob@example.com'},
            {'name': 'Charlie', 'email': 'charlie@example.com'},
            {'name': 'Diana', 'email': 'diana@example.com'}
        ])
        
        # Insert items
        conn.execute(items.insert(), [
            {'name': 'Coffee', 'price': 5.50},
            {'name': 'Sandwich', 'price': 20.00},
            {'name': 'Pizza', 'price': 35.75},
            {'name': 'Soda', 'price': 10.00},
            {'name': 'Salad', 'price': 15.25},
            {'name': 'Steak', 'price': 45.00},
            {'name': 'Wine', 'price': 15.00}
        ])
        
        # Insert receipts
        conn.execute(receipts.insert(), [
            {'customer_id': 1, 'item_id': 1, 'quantity': 1, 'tip': 5.00},  # Alice's coffee
            {'customer_id': 1, 'item_id': 2, 'quantity': 1, 'tip': 5.00},  # Alice's sandwich
            {'customer_id': 2, 'item_id': 3, 'quantity': 1, 'tip': 10.00}, # Bob's pizza
            {'customer_id': 2, 'item_id': 4, 'quantity': 1, 'tip': 10.00}, # Bob's soda
            {'customer_id': 3, 'item_id': 5, 'quantity': 1, 'tip': 3.00},  # Charlie's salad
            {'customer_id': 4, 'item_id': 6, 'quantity': 1, 'tip': 15.00}, # Diana's steak
            {'customer_id': 4, 'item_id': 7, 'quantity': 1, 'tip': 15.00}  # Diana's wine
        ])
        
        conn.commit()

if __name__ == "__main__":
    create_test_table()
    print("Test tables created with sample data!")