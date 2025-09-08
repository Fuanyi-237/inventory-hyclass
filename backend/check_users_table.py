import sqlite3

def check_users_table():
    try:
        conn = sqlite3.connect('inventory_updated.db')
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ 'users' table does not exist in the database!")
            return
            
        # Get table info
        print("✅ 'users' table exists. Here's its structure:")
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("\nColumns in 'users' table:")
        for col in columns:
            col_id, name, col_type, notnull, default_val, pk = col
            print(f"- {name}: {col_type} {'(PRIMARY KEY)' if pk else ''} {'(NOT NULL)' if notnull else ''} {f'DEFAULT {default_val}' if default_val is not None else ''}")
        
        # Check if any users exist
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"\nNumber of users in the database: {count}")
        
        # Show first few users if any exist
        if count > 0:
            print("\nFirst 5 users:")
            cursor.execute("SELECT id, email, full_name, is_superuser, is_active FROM users LIMIT 5")
            for user in cursor.fetchall():
                print(f"ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Superuser: {bool(user[3])}, Active: {bool(user[4])}")
                
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_users_table()
