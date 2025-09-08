import sqlite3
from getpass import getpass
from hashlib import sha256

def get_password_hash(password):
    """Simple password hashing function"""
    return sha256(password.encode('utf-8')).hexdigest()

def main():
    print("Super Admin Account Creation")
    print("===========================")
    
    # Get user input
    email = input("Enter email: ")
    full_name = input("Enter full name: ")
    password = getpass("Enter password: ")
    confirm = getpass("Confirm password: ")
    
    if password != confirm:
        print("Error: Passwords do not match!")
        return
    
    # Hash the password
    hashed_password = get_password_hash(password)
    
    try:
        # Connect to SQLite database (creates it if it doesn't exist)
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT,
            is_active INTEGER DEFAULT 1,
            is_superuser INTEGER DEFAULT 0
        )
        ''')
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone() is not None:
            print(f"Error: User with email '{email}' already exists!")
            return
        
        # Insert new superadmin user
        cursor.execute('''
        INSERT INTO users (email, hashed_password, full_name, is_active, is_superuser)
        VALUES (?, ?, ?, 1, 1)
        ''', (email, hashed_password, full_name))
        
        # Commit changes and close connection
        conn.commit()
        print(f"\n✅ Super admin account created successfully!")
        print(f"Email: {email}")
        print(f"Name: {full_name}")
        
    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
