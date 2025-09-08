import sqlite3

def setup_database():
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
        )''')
        
        # Check if admin exists
        cursor.execute("SELECT * FROM users WHERE is_superuser = 1")
        admin = cursor.fetchone()
        
        if admin:
            print("\n✅ Admin user already exists:")
            print(f"ID: {admin[0]}")
            print(f"Email: {admin[1]}")
            print(f"Name: {admin[3]}")
            return
            
        # Create default admin if none exists
        print("\nCreating default admin user...")
        cursor.execute('''
        INSERT INTO users (email, hashed_password, full_name, is_active, is_superuser)
        VALUES (?, ?, ?, 1, 1)
        ''', ('admin@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'Admin User'))
        
        conn.commit()
        print("✅ Default admin user created!")
        print("Email: admin@example.com")
        print("Password: password")
        print("\n⚠️ Please change the default password immediately after login!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Setting up admin user...")
    setup_database()
