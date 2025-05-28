# scripts/create_test_tables.py
from sqlalchemy import create_engine, text
from backend.database.connection import get_database_engine

def create_test_tables():
    engine = get_database_engine()
    
    with engine.connect() as conn:
        # Create VIP table
        conn.execute(text("""
            CREATE TABLE vip (
                vip_id INTEGER NOT NULL,
                vip_address VARCHAR(100) NOT NULL,
                port INTEGER NOT NULL,
                PRIMARY KEY (vip_id)
            )
        """))
        
        # Create load balancer table
        conn.execute(text("""
            CREATE TABLE load_balancer (
                device_id INTEGER NOT NULL,
                device_name VARCHAR(100) NOT NULL,
                location VARCHAR(100) NOT NULL,
                vip_id INTEGER,
                PRIMARY KEY (device_id),
                FOREIGN KEY(vip_id) REFERENCES vip (vip_id)
            )
        """))
        
        # Create VIP member table
        conn.execute(text("""
            CREATE TABLE vip_member (
                member_id INTEGER NOT NULL,
                vip_id INTEGER NOT NULL,
                member_address VARCHAR(100) NOT NULL,
                port INTEGER NOT NULL,
                PRIMARY KEY (member_id),
                FOREIGN KEY(vip_id) REFERENCES vip (vip_id)
            )
        """))
        
        # Insert sample data
        conn.execute(text("""
            INSERT INTO vip (vip_id, vip_address, port) VALUES
            (1, '10.0.0.1', 80),
            (2, '10.0.0.2', 443),
            (3, '10.0.0.3', 8080)
        """))
        
        conn.execute(text("""
            INSERT INTO load_balancer (device_id, device_name, location, vip_id) VALUES
            (1, 'lb-prod-1', 'US-East', 1),
            (2, 'lb-prod-2', 'US-West', 2),
            (3, 'lb-prod-3', 'US-East', 3)
        """))
        
        conn.execute(text("""
            INSERT INTO vip_member (member_id, vip_id, member_address, port) VALUES
            (1, 1, '192.168.1.1', 80),
            (2, 1, '192.168.1.2', 80),
            (3, 2, '192.168.1.3', 443),
            (4, 3, '192.168.1.4', 8080)
        """))
        
        # Commit changes
        conn.commit()
        
        print("Successfully created test tables and sample data")

if __name__ == "__main__":
    create_test_tables() 