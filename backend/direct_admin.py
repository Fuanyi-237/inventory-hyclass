import sqlite3
import sys
from password_utils import get_password_hash

def create_admin():
    try:
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            is_active BOOLEAN NOT NULL DEFAULT 1,
            is_superuser BOOLEAN NOT NULL DEFAULT 0
        )
        ''')
        
        # Create admin user if it doesn't exist
        cursor.execute("SELECT * FROM users WHERE email = 'admin@inventory.com'")
        if not cursor.fetchone():
            hashed_password = get_password_hash("admin123")
            cursor.execute('''
            INSERT INTO users (username, email, full_name, hashed_password, role, is_active, is_superuser)
            VALUES (?, ?, ?, ?, 'superadmin', 1, 1)
            ''', ("admin", "admin@inventory.com", "Admin User", hashed_password))
            conn.commit()
            print("✅ Admin user created successfully!")
        else:
            print("✅ Admin user already exists!")
            
        # Print user info
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("\nUsers in database:")
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[5]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_admin()
