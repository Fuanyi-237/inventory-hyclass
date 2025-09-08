import sqlite3
from password_utils import get_password_hash

def setup_database():
    print("Setting up database with correct schema...")
    
    try:
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Drop existing tables if they exist
        cursor.executescript("""
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS items;
        DROP TABLE IF EXISTS categories;
        DROP TABLE IF EXISTS transactions;
        DROP TABLE IF EXISTS notifications;
        """)
        
        # Create users table with correct schema
        cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            is_active BOOLEAN NOT NULL DEFAULT 1,
            is_superuser BOOLEAN NOT NULL DEFAULT 0
        )
        """)
        
        # Create other tables...
        
        # Create admin user
        hashed_password = get_password_hash("admin123")
        cursor.execute("""
        INSERT INTO users (username, email, full_name, hashed_password, role, is_active, is_superuser)
        VALUES (?, ?, ?, ?, 'superadmin', 1, 1)
        """, ("admin", "admin@inventory.com", "Admin User", hashed_password))
        
        conn.commit()
        print("\n✅ Database setup complete!")
        print("Admin user created:")
        print("Email: admin@inventory.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"\n❌ Error setting up database: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    setup_database()
