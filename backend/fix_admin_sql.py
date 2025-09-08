import sqlite3
from password_utils import get_password_hash

def fix_admin_user():
    conn = None
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='users'
        """)
        if not cursor.fetchone():
            print("❌ Error: 'users' table does not exist!")
            return
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if not admin:
            print("Admin user not found. Creating admin user...")
            hashed_password = get_password_hash("admin123")
            cursor.execute("""
            INSERT INTO users (username, email, full_name, hashed_password, role, is_active, is_superuser)
            VALUES (?, ?, ?, ?, 'superadmin', 1, 1)
            """, ("admin", "admin@inventory.com", "Admin User", hashed_password))
            conn.commit()
            print("✅ Admin user created successfully!")
        else:
            print("✅ Admin user found in database.")
            print(f"ID: {admin[0]}, Username: {admin[1]}, Email: {admin[2]}")
            
            # Verify password
            from password_utils import verify_password
            if not verify_password("admin123", admin[4]):  # hashed_password is at index 4
                print("❌ Password verification failed. Updating password...")
                hashed_password = get_password_hash("admin123")
                cursor.execute("""
                UPDATE users 
                SET hashed_password = ? 
                WHERE username = 'admin'
                """, (hashed_password,))
                conn.commit()
                print("✅ Password updated to 'admin123'")
            else:
                print("✅ Password is correct.")
        
        # Print all users for verification
        print("\nAll users in database:")
        cursor.execute("SELECT id, username, email, role FROM users")
        for user in cursor.fetchall():
            print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    fix_admin_user()
