import sqlite3

def fix_database():
    print("Fixing database schema...")
    
    try:
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Get the current schema of users table
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add missing columns if they don't exist
        if 'username' not in columns:
            print("Adding 'username' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
        
        if 'role' not in columns:
            print("Adding 'role' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        
        # Create or update the admin user
        cursor.execute("""
        INSERT OR REPLACE INTO users 
        (id, email, username, full_name, hashed_password, is_active, is_superuser, role)
        VALUES (1, 'expert@gmail.com', 'expert', 'IT Expert', 
                '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 
                1, 1, 'superadmin')
        """)
        
        conn.commit()
        print("✅ Database schema fixed and admin user created!")
        print("You can now log in with:")
        print("Email: expert@gmail.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_database()
