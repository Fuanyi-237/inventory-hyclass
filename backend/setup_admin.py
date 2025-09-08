import sqlite3
from getpass import getpass
from hashlib import sha256

def get_password_hash(password: str) -> str:
    """Generate a simple SHA256 hash for the password."""
    return sha256(password.encode('utf-8')).hexdigest()

def setup_database():
    conn = None
    try:
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
        
        conn.commit()
        print("✅ Database setup complete")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def create_superuser():
    print("\nCreate Super Admin Account")
    print("=======================")
    
    while True:
        email = input("Email: ").strip()
        if "@" in email and "." in email:
            break
        print("Please enter a valid email address.")
    
    full_name = input("Full Name: ").strip()
    
    while True:
        password = getpass("Password (min 8 characters): ")
        if len(password) >= 8:
            if password == getpass("Confirm Password: "):
                break
            print("Passwords do not match. Please try again.")
        else:
            print("Password must be at least 8 characters long.")
    
    hashed_password = get_password_hash(password)
    
    try:
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            print(f"\n❌ User with email '{email}' already exists.")
            return False
        
        # Create superuser
        cursor.execute('''
        INSERT INTO users (email, hashed_password, full_name, is_active, is_superuser)
        VALUES (?, ?, ?, 1, 1)
        ''', (email, hashed_password, full_name))
        
        conn.commit()
        print(f"\n✅ Super admin account created successfully for {email}")
        return True
        
    except sqlite3.Error as e:
        print(f"\n❌ Error creating user: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Setting up database and creating super admin user...")
    if setup_database():
        create_superuser()
