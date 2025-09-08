import sqlite3

def verify_setup():
    print("Verifying database setup...")
    
    try:
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ Users table does not exist!")
            return
            
        print("✅ Users table exists")
        
        # Check columns in users table
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        print("\nColumns in users table:")
        for col in columns:
            print(f"- {col}")
            
        # Check admin user
        cursor.execute("SELECT * FROM users WHERE email = 'admin@inventory.com'")
        admin = cursor.fetchone()
        
        if admin:
            print("\n✅ Admin user found:")
            print(f"ID: {admin[0]}")
            print(f"Username: {admin[1]}")
            print(f"Email: {admin[2]}")
            print(f"Role: {admin[5]}")
            print(f"Is Active: {bool(admin[6])}")
            print(f"Is Superuser: {bool(admin[7])}")
            
            # Verify password
            from password_utils import verify_password
            if verify_password("admin123", admin[4]):
                print("✅ Password 'admin123' is correct!")
            else:
                print("❌ Password verification failed!")
        else:
            print("\n❌ Admin user not found!")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verify_setup()
